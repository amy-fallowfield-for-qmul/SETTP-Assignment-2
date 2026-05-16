from dataclasses import dataclass
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from Logic.attributeValidator import Validator
    from Data.DigitalID.digitalID import DigitalID


@dataclass(frozen=True)
class IdentityClaim:
    """Stores all attributes needed to process an identity request"""

    first_name: str
    surname: str
    date_of_birth: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "first_name": self.first_name,
            "surname": self.surname,
            "date_of_birth": self.date_of_birth
        }

    def validated(self, validator: "Validator") -> "IdentityClaim":
        current_attributes = self.to_dict()
        validated_attributes = {
            "first_name": validator.validate_attribute("first_name", current_attributes["first_name"]),
            "surname": validator.validate_attribute("surname", current_attributes["surname"]),
            "date_of_birth": validator.validate_attribute("date_of_birth", current_attributes["date_of_birth"])
        }
        return IdentityClaim(**validated_attributes)

    def matches(self, digital_id: "DigitalID") -> bool:
        digital_id_attributes = {
            "first_name": digital_id.first_name,
            "surname": digital_id.surname,
            "date_of_birth": digital_id.date_of_birth
        }
        return digital_id_attributes == self.to_dict()
