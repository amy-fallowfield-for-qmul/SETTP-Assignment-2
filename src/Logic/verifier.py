from typing import Any
from datetime import date
from Common.singleton import SingletonMeta
from Logic.attributeValidator import Validator
from Logic.suspensionAnalyser import SuspensionAnalyser
from Logic.exceptionLogger import record_failures
from Logic.requestContext import RequestContext
from Logic.identityClaim import IdentityClaim
from Logic.period import Period
from Data.DigitalID.digitalIDRepository import DigitalIDRepository
from Data.DigitalID.digitalID import Status
from Data.Logging.logRepository import LogRepository
from Data.Logging.log import Log, Action

class Verifier(metaclass=SingletonMeta):
    """Singleton verifier for Digital ID verification operations"""

    def __init__(self) -> None:
        self.VALIDATOR = Validator()
        self.SUSPENSION_ANALYSER = SuspensionAnalyser()
        self.DIGITAL_ID_REPOSITORY = DigitalIDRepository()
        self.LOG_REPOSITORY = LogRepository()

    def verify_identity(self, id_number: int, claim: IdentityClaim, context: RequestContext) -> bool:
        with record_failures(self.LOG_REPOSITORY, Action.VERIFY, context, id_number, "identity"):
            context.assert_can_perform("verify_identity")
            digital_id = self.DIGITAL_ID_REPOSITORY.get_from_id(id_number)
            self._ensure_active(digital_id)

            validated_claim = claim.validated(self.VALIDATOR)
            validated_justification = context.validated_justification(self.VALIDATOR)

            result = validated_claim.matches(digital_id)

            log = Log.for_verify(context.organisation.name, id_number, validated_justification, "identity", result)
            self.LOG_REPOSITORY.add(log)

            return result

    def verify_minimum_age(self, id_number: int, minimum_age: Any, context: RequestContext) -> bool:
        with record_failures(self.LOG_REPOSITORY, Action.VERIFY, context, id_number, "minimum_age"):
            context.assert_can_perform("verify_minimum_age")
            validated_min_age = self.VALIDATOR.validate_minimum_age(minimum_age)

            digital_id = self.DIGITAL_ID_REPOSITORY.get_from_id(id_number)
            self._ensure_active(digital_id)

            age = self._calculate_age(digital_id.date_of_birth)
            result = age >= validated_min_age

            validated_justification = context.validated_justification(self.VALIDATOR)

            log = Log.for_verify(context.organisation.name, id_number, validated_justification, "minimum_age", result, str(validated_min_age))
            self.LOG_REPOSITORY.add(log)

            return result

    def verify_attribute(self, id_number: int, attribute: str, claimed_value: str, context: RequestContext) -> bool:
        with record_failures(self.LOG_REPOSITORY, Action.VERIFY, context, id_number, attribute):
            context.assert_can_perform("verify_attribute")
            context.assert_can_verify(attribute)

            digital_id = self.DIGITAL_ID_REPOSITORY.get_from_id(id_number)

            if attribute != "status":
                self._ensure_active(digital_id)

            validated_claimed_value = self.VALIDATOR.validate_attribute(attribute, claimed_value)
            validated_justification = context.validated_justification(self.VALIDATOR)

            stored_value = digital_id.to_dict()[attribute]
            result = str(stored_value) == str(validated_claimed_value)

            log = Log.for_verify(context.organisation.name, id_number, validated_justification, attribute, result)
            self.LOG_REPOSITORY.add(log)

            return result

    def verify_suspended_in_period(self, period: Period, id_number: int, context: RequestContext) -> bool:
        with record_failures(self.LOG_REPOSITORY, Action.VERIFY, context, id_number, "suspended_in_period"):
            context.assert_can_perform("verify_suspended_in_period")
            result = self.SUSPENSION_ANALYSER.was_suspended_in_period(period, id_number)

            validated_justification = context.validated_justification(self.VALIDATOR)

            audit_log = Log.for_verify(context.organisation.name, id_number, validated_justification, "suspended_in_period", result, str(period))
            self.LOG_REPOSITORY.add(audit_log)

            return result

    def _ensure_active(self, digital_id) -> None:
        if digital_id.status != Status.ACTIVE:
            raise ValueError(f"Digital ID is {digital_id.status.value}")

    def _calculate_age(self, date_of_birth: str) -> int:
        dob = date.fromisoformat(date_of_birth)
        today = date.today()
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
