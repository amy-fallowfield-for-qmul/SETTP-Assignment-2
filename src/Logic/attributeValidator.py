from typing import Any, Dict
from datetime import date
import re
from Common.singleton import SingletonMeta
from Data.DigitalID.digitalID import Status
from Data.Attributes.attributeRepository import AttributeRegistry
from Data.Attributes.attributeMetadata import AttributeMetadata, AttributeType
from Data.Attributes.address import Address

class Validator(metaclass=SingletonMeta):
    """Singleton validator for Digital ID attributes"""

    def __init__(self) -> None:
        self.ATTRIBUTE_REGISTRY = AttributeRegistry()

    def validate_all_attributes(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates the following:
        - No attributes are missing
        - No attribute are unexpected
        - All expected attributes run their own validation function
        """

        required_attributes = self.ATTRIBUTE_REGISTRY.get_required_for_creation()
        allowed_attributes = required_attributes + ["justification"]

        if not all(attribute in data for attribute in required_attributes):
            raise ValueError("Missing required attributes")
        
        for key in data:
            if key not in allowed_attributes:
                raise ValueError(f"Unexpected attribute: {key}")

        for key in required_attributes:
            data[key] = self.validate_attribute(key, data[key])

        if "justification" in data:
            data["justification"] = self.validate_attribute("justification", data["justification"])

        return data
    
    def validate_attribute(self, attribute: str, value: str) -> str:
        if attribute == "justification":
            return self._validate_string(value, attribute)

        if attribute not in self.ATTRIBUTE_REGISTRY.get_all_attributes():
            raise ValueError(f"No validation defined for attribute: {attribute}")

        metadata = self.ATTRIBUTE_REGISTRY.get_attribute(attribute)
        return self._validate_by_type(metadata, value)

    def _validate_by_type(self, metadata: AttributeMetadata, value: str) -> str:
        if metadata.type == AttributeType.STRING:
            return self._validate_string(value, metadata.name)
        elif metadata.type == AttributeType.DATE:
            return self.validate_date(value)
        elif metadata.type == AttributeType.NATIONAL_INSURANCE:
            return self._validate_national_insurance(value)
        elif metadata.type == AttributeType.ADDRESS:
            return self._validate_address(value)
        elif metadata.type == AttributeType.STATUS:
            return self._validate_status(value)
        else:
            raise ValueError(f"No validation defined for attribute type: {metadata.type.value}")

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

    def validate_date(self, date_string: str) -> str:
        """
        Validates the following:
        - Values must be strings
        - Values must use the format: YYYY-MM-DD
        - Values must be today or in the past
        """
        
        if not isinstance(date_string, str):
            raise ValueError("Date must be a string")
        
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_string):
            raise ValueError("Date must be in YYYY-MM-DD format")
        
        date_object = date.fromisoformat(date_string)
        if date_object > date.today():
            raise ValueError("Date cannot be in the future")
        
        return date_string
    
    def _validate_national_insurance(self, ni_number: str) -> str:
        """
        Validates the following:
        - Values must be strings
        - Values must follow UK NI format: 2 letters + 6 digits + 1 letter (e.g., AB123456C)
        - First letter cannot be D, F, I, Q, U, or V
        - Second letter cannot be D, F, I, Q, U, V, or O
        - The first 2 letters combines cannot be BG, GB, NK, KN, TN, NT, or ZZ
        - Final letter must be A, B, C, or D
        """
        
        if not isinstance(ni_number, str):
            raise ValueError("National Insurance number must be a string")
        
        ni_number = ni_number.strip().replace(" ", "").upper()
        
        if not re.match(r"^[A-Z]{2}\d{6}[A-Z]$", ni_number):
            raise ValueError("National Insurance number must be in format AB123456C (2 letters, 6 digits, 1 letter)")
        
        first_letter = ni_number[0]
        second_letter = ni_number[1]
        first_two_letters = ni_number[:2]
        final_letter = ni_number[8]

        validations = [
            (first_letter, ["D", "F", "I", "Q", "U", "V"], f"National Insurance number cannot start with {first_letter}"),
            (second_letter, ["D", "F", "I", "Q", "U", "V", "O"], f"National Insurance number cannot have {second_letter} as second letter"),
            (first_two_letters, ["BG", "GB", "NK", "KN", "TN", "NT", "ZZ"], f"National Insurance number cannot begin with {first_two_letters}"),
        ]
        
        for value, invalid_list, error_message in validations:
            if value in invalid_list:
                raise ValueError(error_message)


        valid_final_letter = ["A", "B", "C", "D"]
        if final_letter not in valid_final_letter:
            raise ValueError(f"National Insurance number must end with A, B, C, or D")
        
        return ni_number
    
    def _validate_address(self, address_string: str) -> str:
        """
        Validates the following:
        - Values must be strings
        - Values must use comma-separated format (Address Line, Town/City, Postcode)
        """
        
        if not isinstance(address_string, str):
            raise ValueError("Address must be a string")
        
        if not address_string.strip():
            raise ValueError("Address string cannot be empty")
        
        parts = [part.strip() for part in address_string.split(',') if part.strip()]
        
        if len(parts) != 3:
            raise ValueError("Address must contain exactly 3 parts: address line, town/city, and postcode")
        
        address_line, town_or_city, postcode = parts
        
        if not address_line:
            raise ValueError("Address line cannot be empty")
        
        self._validate_string(town_or_city, "Town or city")
        self._validate_postcode(postcode)

        return f"{address_line}, {town_or_city}, {postcode.upper()}"

    def _validate_postcode(self, postcode: str) -> str:
        """
        Validates the following:
        - Values must be strings
        - First letter cannot be Q, V, or X
        - Second letter cannot be I, J, or Z and may not exist
        - Third position cannot be I, L, M, N, O, P, Q, R, V, X, Y, or Z and may not exist
        - Second half must use format: digit + letter + letter
        - Second half letters cannot be C, I, K, M, O, or V
        """
        
        if not isinstance(postcode, str):
            raise ValueError("Postcode must be a string")
        
        postcode = postcode.strip().upper()
        
        if not postcode:
            raise ValueError("Postcode cannot be empty")
        
        if not re.match(r'^[A-Z]{1,2}\d[A-Z\d]? \d[A-Z]{2}$', postcode):
            raise ValueError("Invalid UK postcode format")
        
        first_letter = postcode[0]
        second_char = postcode[1] if len(postcode) > 1 else ""
        second_half_letters = postcode[-2:]
        
        third_letter = None
        for i, char in enumerate(postcode):
            if i >= 2 and char.isalpha() and i < len(postcode) - len(second_half_letters):
                third_letter = char
                break
        
        validations = [
            (first_letter, ["Q", "V", "X"], f"Postcode cannot start with {first_letter}"),
        ]
        
        if second_char.isalpha():
            validations.append((second_char, ["I", "J", "Z"], f"Postcode cannot have {second_char} as second letter"))
        
        if third_letter:
            validations.append((third_letter, ["I", "L", "M", "N", "O", "P", "Q", "R", "V", "X", "Y", "Z"], f"Postcode cannot have {third_letter} in third position"))
        
        for value, invalid_list, error_message in validations:
            if value in invalid_list:
                raise ValueError(error_message)
        
        for letter in second_half_letters:
            if letter in ["C", "I", "K", "M", "O", "V"]:
                raise ValueError(f"Postcode cannot have {letter} in second half")
        
        return postcode
