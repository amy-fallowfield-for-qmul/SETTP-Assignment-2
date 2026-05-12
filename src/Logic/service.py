from typing import Dict, Any, List
from datetime import date
from Common.singleton import SingletonMeta
from Logic.attributeValidator import Validator
from Logic.verificationValidator import VerificationValidator
from Data.DigitalID.digitalIDRepository import DigitalIDRepository
from Data.DigitalID.digitalID import DigitalID, Status
from Data.Logging.logRepository import LogRepository
from Data.Logging.log import Log, Action
from Data.Attributes.attributeRepository import AttributeRegistry
from Config.constants import ID_PATH, LOG_PATH, LOG_HEADERS

class DigitalIDService(metaclass=SingletonMeta):
    """Singleton service for managing Digital ID operations"""

    def __init__(self) -> None:
        self.VALIDATOR = Validator()
        self.VERIFICATION_VALIDATOR = VerificationValidator()
        self.DIGITAL_ID_REPOSITORY = DigitalIDRepository()
        self.LOG_REPOSITORY = LogRepository()
        self.ATTRIBUTE_REGISTRY = AttributeRegistry()

    def create_id(self, data: Dict[str, Any]) -> DigitalID:
        justification = data.get("justification", "Unknown justification")

        try:
            valid_data = self.VALIDATOR.validate_all_attributes(data)

            creation_attributes = {}
            for attr_name in self.ATTRIBUTE_REGISTRY.get_required_for_creation():
                creation_attributes[attr_name] = valid_data[attr_name]

            justification = valid_data["justification"]

            new_id = DigitalID(creation_attributes)
            self.DIGITAL_ID_REPOSITORY.add(new_id)
            
            log = Log.for_create("Central Authority", new_id.id, justification, new_id)
            self.LOG_REPOSITORY.add(log)

            return new_id

        except Exception as e:
            error_message = f"Invalid attribute data: {e}"

            failed_log = Log.for_failure("Central Authority", 0, Action.CREATE, justification, error_message)
            self.LOG_REPOSITORY.add(failed_log)
            raise ValueError(error_message)

    def get_all_ids(self) -> Dict[int, DigitalID]:
        return self.DIGITAL_ID_REPOSITORY.get_all()
    
    def get_all_logs(self) -> Dict[int, Log]:
        return self.LOG_REPOSITORY.get_all()

    def get_filtered_ids(self, filters: Dict[str, str]) -> Dict[int, DigitalID]:
        return self._apply_filter(self.DIGITAL_ID_REPOSITORY.get_all(), filters, self.ATTRIBUTE_REGISTRY.get_all_attributes())

    def get_filtered_logs(self, filters: Dict[str, str]) -> Dict[int, Log]:
        return self._apply_filter(self.LOG_REPOSITORY.get_all(), filters, LOG_HEADERS)

    def _apply_filter(self, all_data: Dict[int, Any], filters: Dict[str, str], valid_fields: List[str]) -> Dict[int, Any]:
        for key in filters:
            if key not in valid_fields:
                raise ValueError(f"Invalid filter field: {key}")

        if not filters:
            return dict(all_data)

        matches: Dict[int, Any] = {}
        for data_id, data_object in all_data.items():
            data_dictionary = data_object.to_dict()
            if all(str(data_dictionary.get(key)).lower() == str(value).lower() for key, value in filters.items()):
                matches[data_id] = data_object

        return matches

    def get_id_by_number(self, id_number: int) -> DigitalID:
        try:
            return self.DIGITAL_ID_REPOSITORY.get_from_id(id_number)
        except KeyError:
            raise ValueError(f"Digital ID with ID {id_number} not found")
        
    def query_attribute(self, id_number: int, attribute: str, justification: str, organisation: str, accessible_attributes: List[str]) -> str:
        safe_justification = justification if justification else "Unknown justification"
        
        try:
            if attribute not in accessible_attributes:
                raise ValueError(f"Access denied: {organisation} is not authorized to access '{attribute}' attribute")
            
            digital_id = self.get_id_by_number(id_number)
            
            attribute_value = digital_id.to_dict()[attribute]
            validated_justification = self.VALIDATOR._validate_string(justification, "justification")
            
            log = Log.for_read(organisation, id_number, validated_justification, str(attribute_value))
            self.LOG_REPOSITORY.add(log)
            
            return str(attribute_value)
        except Exception as e:
            error_message = str(e)
            failed_log = Log.for_failure(organisation, id_number, Action.READ, safe_justification, error_message)
            self.LOG_REPOSITORY.add(failed_log)
            raise

    def verify_identity(self, id_number: int, first_name: str, surname: str, date_of_birth: str, justification: str, organisation: str, accessible_attributes: List[str]) -> bool:
        safe_justification = justification if justification else "Unknown justification"

        try:
            required_attributes = {
                "first_name": first_name,
                "surname": surname,
                "date_of_birth": date_of_birth,
            }

            for attr in required_attributes:
                if attr not in accessible_attributes:
                    raise ValueError(f"Access denied: {organisation} is not authorised to access '{attr}' attribute")

            digital_id = self.get_id_by_number(id_number)

            if digital_id.status != Status.ACTIVE:
                raise ValueError(f"Digital ID is {digital_id.status.value}")

            validated_attributes = {
                name: self.VALIDATOR.validate_attribute(name, value)
                for name, value in required_attributes.items()
            }
            validated_justification = self.VALIDATOR._validate_string(justification, "justification")

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

    def verify_minimum_age(self, id_number: int, minimum_age: Any, justification: str, organisation: str, accessible_attributes: List[str]) -> bool:
        safe_justification = justification if justification else "Unknown justification"

        try:
            if "date_of_birth" not in accessible_attributes:
                raise ValueError(f"Access denied: {organisation} is not authorized to access 'date_of_birth' attribute")

            validated_min_age = self.VERIFICATION_VALIDATOR.validate_minimum_age(minimum_age)

            digital_id = self.get_id_by_number(id_number)

            if digital_id.status != Status.ACTIVE:
                raise ValueError(f"Digital ID is {digital_id.status.value}")

            date_of_birth = date.fromisoformat(digital_id.date_of_birth)
            today = date.today()
            age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))

            result = age >= validated_min_age

            validated_justification = self.VALIDATOR._validate_string(justification, "justification")

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

            digital_id = self.get_id_by_number(id_number)

            if attribute != "status" and digital_id.status != Status.ACTIVE:
                raise ValueError(f"Digital ID is {digital_id.status.value}")

            validated_claimed_value = self.VALIDATOR.validate_attribute(attribute, claimed_value)
            validated_justification = self.VALIDATOR._validate_string(justification, "justification")

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

    def update_id(self, id_number: int, attribute: str, value: Any, justification: str) -> None:
        safe_justification = justification if justification else "Unknown justification"
        
        try:
            digital_id = self.get_id_by_number(id_number)
            old_value = digital_id.to_dict()[attribute]

            if digital_id.status == Status.REVOKED:
                raise ValueError("Cannot update a revoked Digital ID")

            if not self.ATTRIBUTE_REGISTRY.get_attribute(attribute).is_mutable:
                raise ValueError(f"{attribute} is immutable and cannot be updated")

            validated_value = self.VALIDATOR.validate_attribute(attribute, value)
            validated_justification = self.VALIDATOR._validate_string(justification, "justification")

            if attribute == "status":
                STATUS_MAP = {
                    "active": digital_id.activate,
                    "suspended": digital_id.suspend,
                    "revoked": digital_id.revoke,
                }
                STATUS_MAP[validated_value.lower()]()
            else:
                setattr(digital_id, attribute, validated_value)

            log = Log.for_update("Central Authority", id_number, validated_justification, attribute, old_value, validated_value)
            self.LOG_REPOSITORY.add(log)
        except Exception as e:
            error_message = str(e)
            failed_log = Log.for_failure("Central Authority", id_number, Action.UPDATE, safe_justification, error_message, attribute)
            self.LOG_REPOSITORY.add(failed_log)
            raise
  
    def load_csv_data(self) -> None:
        try:
            self.DIGITAL_ID_REPOSITORY.load_from_csv()
            print(f"Loaded digital ID data from {ID_PATH}")

            self.LOG_REPOSITORY.load_from_csv()
            print(f"Loaded log data from {LOG_PATH}")
        except FileNotFoundError:
            print("No existing data found")

    def save_csv_data(self) -> None:
        try:
            if self.DIGITAL_ID_REPOSITORY.get_all():
                self.DIGITAL_ID_REPOSITORY.save_to_csv()
                print(f"Saved digital ID data to {ID_PATH}")
            else:
                print("No digital IDs to save")

            if self.LOG_REPOSITORY.get_all():
                self.LOG_REPOSITORY.save_to_csv()
                print(f"Saved log data to {LOG_PATH}")
            else:
                print("No logs to save")
        except Exception as e:
            print(f"Error saving to CSV: {e}")

    def get_required_attributes_for_creation(self) -> List[str]:
        return self.ATTRIBUTE_REGISTRY.get_required_for_creation()
    
    def get_attribute_input_prompt(self, attribute_name: str) -> str:
        return self.ATTRIBUTE_REGISTRY.get_input_prompt(attribute_name)
    
    def get_all_digital_id_attributes(self) -> List[str]:
        return self.ATTRIBUTE_REGISTRY.get_all_attributes()
    
    def get_queryable_attributes(self) -> List[str]:
        return self.ATTRIBUTE_REGISTRY.get_queryable_attributes()
    
    def get_mutable_attributes(self) -> List[str]:
        return self.ATTRIBUTE_REGISTRY.get_mutable_attributes()
