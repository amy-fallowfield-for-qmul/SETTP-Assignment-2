from typing import Dict, List
from Common.singleton import SingletonMeta
from .attributeMetadata import AttributeMetadata, AttributeType

class AttributeRegistry(metaclass=SingletonMeta):
    """Singleton repository for storing and managing Digital ID attributes"""

    def __init__(self) -> None:
        self._attributes: Dict[str, AttributeMetadata] = {}
        self._register_core_attributes()
    
    def _register_core_attributes(self) -> None:
        
        self.register_attribute(AttributeMetadata(
            name="id",
            display_name="ID",
            attribute_type=AttributeType.INTEGER,
            is_mutable=False,
            is_required_for_creation=False
        ))
        
        self.register_attribute(AttributeMetadata(
            name="status", 
            display_name="Status",
            attribute_type=AttributeType.STATUS,
            is_mutable=True,
            is_required_for_creation=False,
            input_prompt="Enter status (active/suspended/revoked): "
        ))

        self.register_attribute(AttributeMetadata(
            name="first_name",
            display_name="First Name", 
            attribute_type=AttributeType.STRING,
            is_mutable=True,
            is_required_for_creation=True,
        ))
        
        self.register_attribute(AttributeMetadata(
            name="surname",
            display_name="Surname",
            attribute_type=AttributeType.STRING, 
            is_mutable=True,
            is_required_for_creation=True,
        ))
        
        self.register_attribute(AttributeMetadata(
            name="date_of_birth",
            display_name="Date of Birth",
            attribute_type=AttributeType.DATE,
            is_mutable=False,
            is_required_for_creation=True,
            input_prompt="Enter date of birth (YYYY-MM-DD): "
        ))
        
        self.register_attribute(AttributeMetadata(
            name="address",
            display_name="Address",
            attribute_type=AttributeType.ADDRESS,
            is_mutable=True,
            is_required_for_creation=True,
            input_prompt="Enter address (Address Line, Town/City, Postcode): "
        ))
        
        self.register_attribute(AttributeMetadata(
            name="national_insurance",
            display_name="National Insurance Number",
            attribute_type=AttributeType.NATIONAL_INSURANCE,
            is_mutable=False,
            is_required_for_creation=True,
            input_prompt="Enter National Insurance number (AB123456C): "
        ))
    
    def register_attribute(self, metadata: AttributeMetadata) -> None:
        self._attributes[metadata.name] = metadata
    
    def get_attribute(self, name: str) -> AttributeMetadata:
        if name not in self._attributes:
            raise ValueError(f"Unknown attribute: {name}")
        return self._attributes[name]
    
    def get_all_attributes(self) -> List[str]:
        return list(self._attributes.keys())
    
    def get_required_for_creation(self) -> List[str]:
        return [name for name, attr in self._attributes.items() if attr.is_required_for_creation]
    
    def get_mutable_attributes(self) -> List[str]:
        return [name for name, attr in self._attributes.items() if attr.is_mutable]
    
    def get_queryable_attributes(self) -> List[str]:
        return [name for name in self._attributes.keys() if name != "id"]
    
    def get_input_prompt(self, attribute_name: str) -> str:
        return self.get_attribute(attribute_name).input_prompt
    
    def get_display_name(self, attribute_name: str) -> str:
        return self.get_attribute(attribute_name).display_name
