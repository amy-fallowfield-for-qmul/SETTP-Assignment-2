from typing import Any, Dict
from datetime import date
import re
from Data.digitalID import Status

class Validator:
    """Singleton validator for Digital ID attributes"""

    REQUIRED_FIELDS = ["firstName", "surname", "dateOfBirth", "justification"]
    STRING_FIELDS = ["firstName", "surname", "justification"]
    _instance = None

    def __new__(cls) -> "Validator":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, '_initialised'):
            self._initialised = True

    def validate_all_attributes(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates the following:
        - No attributes are missing
        - No attribute are unexpected
        - All expected attributes run their own validation function
        """

        required_attributes = self.REQUIRED_FIELDS

        if not all(attribute in data for attribute in required_attributes):
            raise ValueError("Missing required attributes")
        
        for key in data:
            if key not in required_attributes:
                raise ValueError(f"Unexpected attribute: {key}")

        for key in self.STRING_FIELDS:
            data[key] = self._validate_string(data[key], key)
        self._validate_date_of_birth(data["dateOfBirth"])

        return data
    
    def validate_attribute(self, attribute: str, value: str) -> str:
        VALIDATION_MAP = {
            "firstName": lambda value: self._validate_string(value, attribute),
            "surname": lambda value: self._validate_string(value, attribute),
            "status": lambda value: self._validate_status(value),
            "justification": lambda value: self._validate_string(value, attribute),
        }

        if attribute not in VALIDATION_MAP:
            raise ValueError(f"No validation defined for attribute: {attribute}")

        return VALIDATION_MAP[attribute](value)

    def _validate_status(self, status: str) -> str:
        """
        Validates the following:
        - Values must be one of the 3 accepted states
          (Active, Suspended, Revoked)
        """

        valid_values = [s.value for s in Status]
        status = status.lower()
        if status not in valid_values:
            raise ValueError("Status must be 'active', 'suspended', or 'revoked'")
            
        return status

    def _validate_string(self, value: str, attribute: str) -> str:
        """
        Validates the following:
        - Values must be strings
        - Values must only contain letters and spaces
        """
        
        if not isinstance(value, str):
            raise ValueError(f"{attribute} must be a string")

        value = value.strip().title()
        if not re.match(r"^[a-zA-Z\s]+$", value):
            raise ValueError(f"{attribute} cannot contain numbers or special characters")
        return value

    def _validate_date_of_birth(self, date_string: str) -> str:
        """
        Validates the following:
        - Values must be strings
        - Values must use the format: YYYY-MM-DD
        - Values must be today or in the past
        """
        
        if not isinstance(date_string, str):
            raise ValueError("Date of birth must be a string")
        
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_string):
            raise ValueError("Date of birth must be in YYYY-MM-DD format")
        
        date_object = date.fromisoformat(date_string)
        if date_object > date.today():
            raise ValueError("Date of birth cannot be in the future")
        
        return date_string