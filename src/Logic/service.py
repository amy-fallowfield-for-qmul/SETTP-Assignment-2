from typing import Dict, Any
from Logic.attributeValidator import Validator
from Data.digitalIDRepository import DigitalIDRepository
from Data.digitalID import DigitalID, Status
from Data.logRepository import LogRepository
from Data.log import Log, Action
from constants import ID_PATH, LOG_PATH, DIGITAL_ID_ALL_FIELDS

class DigitalIDService:
    """Singleton service for managing Digital ID operations"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialised'):
            self._initialised = True
            self.VALIDATOR = Validator()
            self.DIGITAL_ID_REPOSITORY = DigitalIDRepository()
            self.LOG_REPOSITORY = LogRepository()

    def create_id(self, data: Dict[str, Any]) -> DigitalID:
        try:
            valid_data = self.VALIDATOR.validate_all_attributes(data)

            first_name = valid_data["firstName"]
            surname = valid_data["surname"]
            date_of_birth = valid_data["dateOfBirth"]
            justification = valid_data["justification"]

            new_id = DigitalID(first_name, surname, date_of_birth)
            self.DIGITAL_ID_REPOSITORY.add(new_id)
            
            log = Log("Central Authority", new_id.id, Action.CREATE, justification, new_id, None)
            self.LOG_REPOSITORY.add(log)

            return new_id

        except Exception as e:
            raise ValueError(f"Invalid attribute data: {e}")

    def get_all(self) -> Dict[int, DigitalID]:
        return self.DIGITAL_ID_REPOSITORY.get_all()

    def get_filtered_ids(self, params: Dict[str, Any]) -> Dict[int, DigitalID]:
        """
        Takes a list of parameters specifiying any specific values an attribute should have
        and returns a dictionary of all Digital IDs which match those parameters
        """

        all_ids = self.DIGITAL_ID_REPOSITORY.get_all()

        for key in params:
            if key not in DIGITAL_ID_ALL_FIELDS:
                raise ValueError(f"Invalid filter field: {key}")

        filtered_ids: Dict[int, DigitalID] = {}

        for id_number, id_object in all_ids.items():
            id_dictionary = id_object.to_dict()
            if all(str(id_dictionary.get(key)).lower() == str(value).lower() for key, value in params.items()):
                filtered_ids[id_number] = id_object

        return filtered_ids

    def get_id_by_number(self, id_number: int) -> DigitalID:
        try:
            return self.DIGITAL_ID_REPOSITORY.get_from_id(id_number)
        except KeyError:
            raise ValueError(f"Digital ID with ID {id_number} not found")

    def update_id(self, id_number: int, attribute: str, value: Any, justification) -> None:
        digital_id = self.get_id_by_number(id_number)
        old_value = digital_id.to_dict()[attribute]

        if digital_id.status == Status.REVOKED:
            raise ValueError("Cannot update a revoked Digital ID")

        STATUS_MAP = {
            "active": digital_id.activate,
            "suspended": digital_id.suspend,
            "revoked": digital_id.revoke,
        }

        SETTER_MAP = {
            "firstName": lambda value: setattr(digital_id, 'first_name', value),
            "surname": lambda value: setattr(digital_id, 'surname', value),
            "status": lambda value: STATUS_MAP[value.lower()](),
        }

        if attribute not in SETTER_MAP:
            raise ValueError(f"Cannot update field: {attribute}")

        validated_value = self.VALIDATOR.validate_attribute(attribute, value)
        validated_justification = self.VALIDATOR._validate_string(justification, "justification")

        log = Log("Central Authority", id_number, Action.UPDATE, validated_justification, old_value, validated_value)
        self.LOG_REPOSITORY.add(log)

        SETTER_MAP[attribute](validated_value)

        
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
