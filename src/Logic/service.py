from typing import Dict, Any
from Logic.attributeValidator import Validator
from Data.digitalIDRepository import DigitalIDRepository
from Data.digitalID import DigitalID, Status

class DigitalIDService:
    """Singleton service for managing Digital ID operations"""

    DIGITAL_ID_FIELDS = ["id", "status", "firstName", "surname", "dateOfBirth"]
    CSV_PATH = "../../digital_ids.csv"
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialised'):
            self._initialised = True
            self.VALIDATOR = Validator()
            self.REPOSITORY = DigitalIDRepository()

    def create_id(self, data: Dict[str, Any]) -> DigitalID:
        try:
            valid_data = self.VALIDATOR.validate_all_attributes(data)

            first_name = valid_data["firstName"]
            surname = valid_data["surname"]
            date_of_birth = valid_data["dateOfBirth"]

            new_id = DigitalID(first_name, surname, date_of_birth)
            self.REPOSITORY.add_id(new_id)

            return new_id

        except Exception as e:
            raise ValueError(f"Invalid attribute data: {e}")

    def get_all_ids(self) -> Dict[int, DigitalID]:
        return self.REPOSITORY.get_all_ids()

    def get_filtered_ids(self, params: Dict[str, Any]) -> Dict[int, DigitalID]:
        """
        Takes a list of parameters specifiying any specific values an attribute should have
        and returns a dictionary of all Digital IDs which match those parameters
        """

        all_ids = self.REPOSITORY.get_all_ids()

        for key in params:
            if key not in self.DIGITAL_ID_FIELDS:
                raise ValueError(f"Invalid filter field: {key}")

        filtered_ids: Dict[int, DigitalID] = {}

        for id_number, id_object in all_ids.items():
            id_dictionary = id_object.to_dict()
            if all(str(id_dictionary.get(key)) == str(value) for key, value in params.items()):
                filtered_ids[id_number] = id_object

        return filtered_ids

    def get_id_by_number(self, id_number: int) -> DigitalID:
        try:
            return self.REPOSITORY.get_id(id_number)
        except KeyError:
            raise ValueError(f"Digital ID with ID {id_number} not found")

    def update_id(self, id_number: int, attribute: str, value: Any) -> None:
        digital_id = self.get_id_by_number(id_number)

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
        SETTER_MAP[attribute](validated_value)
        
    def load_csv_data(self) -> None:
        try:
            self.REPOSITORY.load_from_csv()
            print(f"Loaded digital ID data from {self.CSV_PATH}")
        except FileNotFoundError:
            print("No existing data found")

    def save_csv_data(self) -> None:
        try:
            if self.REPOSITORY.get_all_ids():
                self.REPOSITORY.save_to_csv()
                print(f"Saved digital ID data to {self.CSV_PATH}")
            else:
                print("No digital IDs to save")
        except Exception as e:
            print(f"Error saving to CSV: {e}")
