from typing import Optional
from enum import Enum

class AttributeType(Enum):
    STRING = "string"
    DATE = "date" 
    STATUS = "status"
    INTEGER = "integer"

class AttributeMetadata:
    """Metadata for a Digital ID attribute"""
    
    def __init__(
        self,
        name: str,
        display_name: str,
        attribute_type: AttributeType,
        is_mutable: bool,
        is_required_for_creation: bool,
        input_prompt: Optional[str] = None
    ):
        self.name = name
        self.display_name = display_name
        self.type = attribute_type
        self.is_mutable = is_mutable
        self.is_required_for_creation = is_required_for_creation
        self.input_prompt = input_prompt or f"Enter {display_name.lower()}: "
