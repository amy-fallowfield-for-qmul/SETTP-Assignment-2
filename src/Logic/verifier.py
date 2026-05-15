from typing import Any, List
from datetime import date
from Common.singleton import SingletonMeta
from Logic.attributeValidator import Validator
from Logic.verificationValidator import VerificationValidator
from Logic.suspensionAnalyser import SuspensionAnalyser
from Data.DigitalID.digitalIDRepository import DigitalIDRepository
from Data.DigitalID.digitalID import Status
from Data.Logging.logRepository import LogRepository
from Data.Logging.log import Log, Action

class Verifier(metaclass=SingletonMeta):
    """Singleton verifier for Digital ID verification operations"""

    def __init__(self) -> None:
        self.VALIDATOR = Validator()
        self.VERIFICATION_VALIDATOR = VerificationValidator()
        self.SUSPENSION_ANALYSER = SuspensionAnalyser()
        self.DIGITAL_ID_REPOSITORY = DigitalIDRepository()
        self.LOG_REPOSITORY = LogRepository()

    def verify_identity(self, id_number: int, first_name: str, surname: str, date_of_birth: str, justification: str, organisation: str) -> bool:
        safe_justification = justification if justification else "Unknown justification"

        try:
            required_attributes = {
                "first_name": first_name,
                "surname": surname,
                "date_of_birth": date_of_birth,
            }

            digital_id = self._get_id_by_number(id_number)

            if digital_id.status != Status.ACTIVE:
                raise ValueError(f"Digital ID is {digital_id.status.value}")

            validated_attributes = {
                name: self.VALIDATOR.validate_attribute(name, value)
                for name, value in required_attributes.items()
            }
            validated_justification = self.VALIDATOR.validate_attribute("justification", justification)

            result = all(
                getattr(digital_id, name) == validated_value
                for name, validated_value in validated_attributes.items()
            )

            log = Log.for_verify(organisation, id_number, validated_justification, "identity", result)
            self.LOG_REPOSITORY.add(log)

            return result
        except Exception as e:
            error_message = str(e)
            failed_log = Log.for_failure(organisation, id_number, Action.VERIFY, safe_justification, error_message, "identity")
            self.LOG_REPOSITORY.add(failed_log)
            raise

    def verify_minimum_age(self, id_number: int, minimum_age: Any, justification: str, organisation: str) -> bool:
        safe_justification = justification if justification else "Unknown justification"

        try:
            validated_min_age = self.VERIFICATION_VALIDATOR.validate_minimum_age(minimum_age)

            digital_id = self._get_id_by_number(id_number)

            if digital_id.status != Status.ACTIVE:
                raise ValueError(f"Digital ID is {digital_id.status.value}")

            date_of_birth = date.fromisoformat(digital_id.date_of_birth)
            today = date.today()
            age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))

            result = age >= validated_min_age

            validated_justification = self.VALIDATOR.validate_attribute("justification", justification)

            log = Log.for_verify(organisation, id_number, validated_justification, "minimum_age", result, str(validated_min_age))
            self.LOG_REPOSITORY.add(log)

            return result
        except Exception as e:
            error_message = str(e)
            failed_log = Log.for_failure(organisation, id_number, Action.VERIFY, safe_justification, error_message, "minimum_age")
            self.LOG_REPOSITORY.add(failed_log)
            raise

    def verify_attribute(self, id_number: int, attribute: str, claimed_value: str, justification: str, organisation: str, accessible_attributes: List[str]) -> bool:
        safe_justification = justification if justification else "Unknown justification"

        try:
            if attribute not in accessible_attributes:
                raise ValueError(f"Access denied: {organisation} is not authorised to verify '{attribute}' attribute")

            digital_id = self._get_id_by_number(id_number)

            if attribute != "status" and digital_id.status != Status.ACTIVE:
                raise ValueError(f"Digital ID is {digital_id.status.value}")

            validated_claimed_value = self.VALIDATOR.validate_attribute(attribute, claimed_value)
            validated_justification = self.VALIDATOR.validate_attribute("justification", justification)

            stored_value = digital_id.to_dict()[attribute]
            result = str(stored_value) == str(validated_claimed_value)

            log = Log.for_verify(organisation, id_number, validated_justification, attribute, result)
            self.LOG_REPOSITORY.add(log)

            return result
        except Exception as e:
            error_message = str(e)
            failed_log = Log.for_failure(organisation, id_number, Action.VERIFY, safe_justification, error_message, attribute)
            self.LOG_REPOSITORY.add(failed_log)
            raise

    def verify_suspended_in_period(self, start_date: str, end_date: str, id_number: int, justification: str, organisation: str) -> bool:
        safe_justification = justification if justification else "Unknown justification"

        try:
            result = self.SUSPENSION_ANALYSER.was_suspended_in_period(start_date, end_date, id_number)

            period_context = f"{start_date} to {end_date}"
            audit_log = Log.for_verify(organisation, id_number, safe_justification, "suspended_in_period", result, period_context)
            self.LOG_REPOSITORY.add(audit_log)

            return result
        except Exception as e:
            failed_log = Log.for_failure(organisation, id_number, Action.VERIFY, safe_justification, str(e), "suspended_in_period")
            self.LOG_REPOSITORY.add(failed_log)
            raise

    def _get_id_by_number(self, id_number: int):
        try:
            return self.DIGITAL_ID_REPOSITORY.get_from_id(id_number)
        except KeyError:
            raise ValueError(f"Digital ID with ID {id_number} not found")
