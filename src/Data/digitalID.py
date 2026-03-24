from enum import Enum
from typing import Dict

class Status(Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    REVOKED = "revoked"

class DigitalID:
    """Stores data model for each individual Digital ID"""

    _next_id: int = 1

    def __init__(self, first_name: str, surname: str, date_of_birth: str) -> None:
        self._id: int = DigitalID._next_id
        DigitalID._next_id += 1

        self._status: Status = Status.ACTIVE
        self._first_name: str = first_name
        self._surname: str = surname
        self._date_of_birth: str = date_of_birth

    def to_dict(self) -> Dict[str, object]:
        return {
            "id": self.id,
            "status": self.status.value,
            "firstName": self.first_name,
            "surname": self.surname,
            "dateOfBirth": self.date_of_birth
        }

    def print(self) -> None:
        print(f"ID: {self.id}, Name: {self.first_name} {self.surname}, DOB: {self.date_of_birth}, Status: {self.status.value}")

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
