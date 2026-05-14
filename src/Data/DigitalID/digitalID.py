from enum import Enum
from typing import Dict, Any
from ..Attributes.attributeRegistry import AttributeRegistry

class Status(Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    REVOKED = "revoked"

class DigitalID:
    """Stores data model for each individual Digital ID"""

    _next_id: int = 1

    def __init__(self, attributes: Dict[str, Any]) -> None:
        self.ATTRIBUTE_REGISTRY = AttributeRegistry()

        if "id" in attributes and attributes["id"] is not None:
            self._id = int(attributes["id"])
            if self._id >= DigitalID._next_id:
                DigitalID._next_id = self._id + 1
        else:
            self._id = DigitalID._next_id
            DigitalID._next_id += 1

        if "status" in attributes and attributes["status"] is not None:
            self._status = Status(attributes["status"])
        else:
            self._status = Status.ACTIVE

        self._first_name: str = attributes["first_name"]
        self._surname: str = attributes["surname"] 
        self._date_of_birth: str = attributes["date_of_birth"]
        self._address: str = attributes["address"]
        self._national_insurance: str = attributes["national_insurance"]

    def to_dict(self) -> Dict[str, object]:
        result: Dict[str, object] = {}
        
        for attribute_name in self.ATTRIBUTE_REGISTRY.get_all_attributes():
            if attribute_name == "status":
                result[attribute_name] = self.status.value
            else:
                result[attribute_name] = getattr(self, attribute_name)

        return result

    def __str__(self) -> str:
        attribute_pairs = [
            f"{self.ATTRIBUTE_REGISTRY.get_display_name(attr_name)}: {getattr(self, attr_name) if attr_name != 'status' else self.status.value}"
            for attr_name in self.ATTRIBUTE_REGISTRY.get_all_attributes()
        ]
        return ", ".join(attribute_pairs)

    def print(self) -> None:
        print(str(self))

    @property
    def id(self) -> int:
        return self._id

    @property
    def status(self) -> Status:
        return self._status
    
    def activate(self) -> None:
        self._status = Status.ACTIVE

    def suspend(self) -> None:
        self._status = Status.SUSPENDED

    def revoke(self) -> None:
        self._status = Status.REVOKED
    
    @property
    def first_name(self) -> str:
        return self._first_name
    
    @first_name.setter
    def first_name(self, name: str) -> None:
        self._first_name = name
    
    @property
    def surname(self) -> str:
        return self._surname
    
    @surname.setter
    def surname(self, name: str) -> None:
        self._surname = name
    
    @property
    def date_of_birth(self) -> str:
        return self._date_of_birth
    
    @property
    def address(self) -> str:
        return self._address
    
    @address.setter
    def address(self, address: str) -> None:
        self._address = address
    
    @property
    def national_insurance(self) -> str:
        return self._national_insurance
    
    @national_insurance.setter
    def national_insurance(self, ni: str) -> None:
        self._national_insurance = ni
