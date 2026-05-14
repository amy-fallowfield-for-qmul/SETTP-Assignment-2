from dataclasses import dataclass
from enum import Enum

class AttributeType(Enum):
    STRING = "string"
    DATE = "date"
    STATUS = "status"
    INTEGER = "integer"
    NATIONAL_INSURANCE = "national_insurance"
    ADDRESS = "address"

@dataclass
class AttributeMetadata:
    """Metadata for a Digital ID attribute"""
    name: str
    display_name: str
    attribute_type: AttributeType
    is_mutable: bool
    is_required_for_creation: bool
    input_prompt: str = ""

    def __post_init__(self) -> None:
        if not self.input_prompt:
            self.input_prompt = f"Enter {self.display_name.lower()}: "
