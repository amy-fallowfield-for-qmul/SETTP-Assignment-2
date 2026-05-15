from typing import Any, List, Optional
from datetime import date, datetime
from Common.singleton import SingletonMeta
from Logic.attributeValidator import Validator
from Logic.verificationValidator import VerificationValidator
from Data.DigitalID.digitalIDRepository import DigitalIDRepository
from Data.DigitalID.digitalID import Status
from Data.Logging.logRepository import LogRepository
from Data.Logging.log import Log, Action

class Verifier(metaclass=SingletonMeta):
    """Singleton verifier for Digital ID verification operations"""

    SUSPENDED_VALUES = ["suspended", "revoked"]

    def __init__(self) -> None:
        self.VALIDATOR = Validator()
        self.VERIFICATION_VALIDATOR = VerificationValidator()
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
            result = self._was_suspended_in_period(start_date, end_date, id_number)

            period_context = f"{start_date} to {end_date}"
            audit_log = Log.for_verify(organisation, id_number, safe_justification, "suspended_in_period", result, period_context)
            self.LOG_REPOSITORY.add(audit_log)

            return result
        except Exception as e:
            failed_log = Log.for_failure(organisation, id_number, Action.VERIFY, safe_justification, str(e), "suspended_in_period")
            self.LOG_REPOSITORY.add(failed_log)
            raise

    def _was_suspended_in_period(self, start_date: str, end_date: str, id_number: int) -> bool:
        all_logs = self.LOG_REPOSITORY.get_all()
        relevant_logs = [log for log in all_logs.values() if log.id_number == id_number]
        most_recent_update = None

        for log in relevant_logs:
            if self._log_updates_status(log):
                if self._log_in_period(log, start_date, end_date):
                    if log.new_value in self.SUSPENDED_VALUES:
                        return True
                elif self._log_most_recent(log, start_date, most_recent_update):
                    most_recent_update = log

        if most_recent_update is not None and most_recent_update.new_value in self.SUSPENDED_VALUES:
            return True

        return False

    def _get_id_by_number(self, id_number: int):
        try:
            return self.DIGITAL_ID_REPOSITORY.get_from_id(id_number)
        except KeyError:
            raise ValueError(f"Digital ID with ID {id_number} not found")

    def _log_most_recent(self, log: Log, date: str, most_recent_update: Optional[Log]) -> bool:
        log_before_period = str(log.timestamp) < date
        log_most_recent_than_current = most_recent_update is None or log.timestamp > most_recent_update.timestamp
        return log_before_period and log_most_recent_than_current

    def _log_updates_status(self, log: Log) -> bool:
        if log.action != Action.UPDATE:
            return False
        return log.attribute == "status"

    def _log_in_period(self, log: Log, start_date: str, end_date: str) -> bool:
        start_date_object = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_object = datetime.strptime(end_date, "%Y-%m-%d")
        return start_date_object <= log.timestamp <= end_date_object
