from enum import Enum
from typing import List, Optional, Union, Dict
from datetime import datetime
from ..DigitalID.digitalID import DigitalID

class Action(Enum):
    CREATE = "create"
    READ = "read"
    UPDATE = "update"

class Log:
    """Stores data model for each individual log entry"""
    
    _next_id = 1

    def __init__(self, accepted: bool, organisation: str, id_number: int, action: Action, justification: str, current_value: Union[str, DigitalID], new_value: Optional[str], attribute: Optional[str] = None) -> None:
        self._id: int = Log._next_id
        Log._next_id += 1
        self._timestamp: datetime = datetime.now()
        self._accepted: bool = accepted
        self._organisation: str = organisation
        self._id_number: int = id_number
        self._action: Action = action
        self._justification: str = justification
        self._current_value: Union[str, DigitalID] = current_value
        self._new_value: Optional[str] = new_value
        self._attribute: Optional[str] = attribute

    @classmethod
    def from_csv(cls, attributes: Dict[str, str]) -> "Log":
        log = cls.__new__(cls)
        log._id = int(attributes["id"])
        log._timestamp = datetime.strptime(attributes["timestamp"], "%d/%m/%Y - %H:%M:%S")
        log._accepted = True if attributes["accepted"] == "True" else False
        log._organisation = attributes["organisation"]
        log._id_number = int(attributes["digitalID"])
        log._action = Action(attributes["action"])
        log._justification = attributes["justification"]
        log._current_value = attributes["currentValue"]
        log._new_value = attributes["newValue"] if attributes["newValue"] != "None" else None
        log._attribute = attributes["attribute"] if attributes["attribute"] != "None" else None
        
        if log._id >= cls._next_id:
            cls._next_id = log._id + 1
        
        return log

    def get_row(self) -> List[object]:
        return [
            self._id,
            self._timestamp.strftime("%d/%m/%Y - %H:%M:%S"),
            self._accepted,
            self._organisation,
            str(self._id_number),
            self._action.value,
            self._justification,
            self._current_value,
            self._new_value,
            self._attribute
        ]
    
    @property
    def id(self) -> int:
        return self._id

    @property
    def timestamp(self) -> datetime:
        return self._timestamp
    
    @property
    def organisation(self) -> str:
        return self._organisation
    
    @property
    def id_number(self) -> int:
        return self._id_number
    
    @property
    def action(self) -> Action:
        return self._action
    
    @property
    def accepted(self) -> bool:
        return self._accepted
    
    @property
    def justification(self) -> str:
        return self._justification
    
    @property
    def current_value(self) -> Union[str, DigitalID]:
        return self._current_value
    
    @property
    def new_value(self) -> Optional[str]:
        return self._new_value

    @property
    def attribute(self) -> Optional[str]:
        return self._attribute

    def to_dict(self) -> Dict[str, object]:
        return {
            "id": self._id,
            "timestamp": self._timestamp.strftime("%d/%m/%Y - %H:%M:%S"),
            "accepted": self._accepted,
            "organisation": self._organisation,
            "digitalID": str(self._id_number),
            "action": self._action.value,
            "justification": self._justification,
            "currentValue": self._current_value.to_dict() if isinstance(self._current_value, DigitalID) else str(self._current_value),
            "newValue": str(self._new_value) if self._new_value else "None",
            "attribute": str(self._attribute) if self._attribute else "None"
        }

    def print(self) -> None:
        match(self._action):
            case Action.CREATE:
                value_string = str(self._current_value)
            case Action.READ:
                value_string = str(self._current_value)
            case Action.UPDATE:
                value_string = f"{self.attribute}: {self._current_value} -> {self._new_value}"
        accepted_string = "ACCEPTED" if self._accepted else "REJECTED"
        print(f"[{self._timestamp.strftime('%d/%m/%Y - %H:%M:%S')}] [{self._organisation}] Requested to {self._action.value} ID {self._id_number} to [{value_string}] because {self._justification} was {accepted_string}")

