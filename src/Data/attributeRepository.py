from typing import Dict, List
from Data.attributeMetadata import AttributeMetadata, AttributeType

class AttributeRegistry:
    """Singleton repository for storing and managing Digital ID attributes"""
    
    _instance = None
    
    def __new__(cls) -> "AttributeRegistry":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self._attributes: Dict[str, AttributeMetadata] = {}
            self._register_core_attributes()
    
    def _register_core_attributes(self) -> None:
        """Register the core Digital ID attributes"""
        
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
    
    def register_attribute(self, metadata: AttributeMetadata) -> None:
        """Register a new attribute"""
        self._attributes[metadata.name] = metadata
    
    def get_attribute(self, name: str) -> AttributeMetadata:
        """Get attribute metadata by name"""
        if name not in self._attributes:
            raise ValueError(f"Unknown attribute: {name}")
        return self._attributes[name]
    
    def get_all_attributes(self) -> List[str]:
        """Get all attribute names"""
        return list(self._attributes.keys())
    
    def get_required_for_creation(self) -> List[str]:
        """Get attributes required for Digital ID creation"""
        return [name for name, attr in self._attributes.items() if attr.is_required_for_creation]
    
    def get_mutable_attributes(self) -> List[str]:
        """Get attributes that can be updated"""
        return [name for name, attr in self._attributes.items() if attr.is_mutable]
    
    def get_queryable_attributes(self) -> List[str]:
        """Get attributes that can be queried"""
        return [name for name in self._attributes.keys() if name != "id"]
    
    def get_input_prompt(self, attribute_name: str) -> str:
        """Get user input prompt for an attribute"""
        return self.get_attribute(attribute_name).input_prompt
    
    def get_display_name(self, attribute_name: str) -> str:
        """Get display name for an attribute"""
        return self.get_attribute(attribute_name).display_name
