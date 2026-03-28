from enum import Enum
from typing import List, Optional, Union, Dict
from datetime import datetime
from Data.digitalID import DigitalID

# [DD/MM/YYYY - HH:MM:SS] [Organisation] [DigitalID] [Action] [Accepted/Rejected] [Justification] [Value/Old Value -> New Value]

class Action(Enum):
    CREATE = "create"
    READ = "read"
    UPDATE = "update"

class Log:
    """Stores data model for each individual log entry"""
    
    _next_id = 1

    def __init__(self, organisation: str, id_number: int, action: Action, justification: str, current_value: Union[str, DigitalID], new_value: Optional[str]) -> None:
        self._id: int = Log._next_id
        Log._next_id += 1
        self._timestamp: datetime = datetime.now()
        self._organisation: str = organisation
        self._id_number: int = id_number
        self._action: Action = action
        self._justification: str = justification
        self._current_value: Union[str, Dict] = current_value.to_dict() if isinstance(current_value, DigitalID) else current_value
        self._new_value: Optional[str] = new_value

    @classmethod
    def from_csv(cls, attributes: Dict[str, str]) -> "Log":
        log = cls.__new__(cls)
        log._id = int(attributes["id"])
        log._timestamp = datetime.strptime(attributes["timestamp"], "%d/%m/%Y - %H:%M:%S")
        log._organisation = attributes["organisation"]
        log._id_number = int(attributes["digitalID"])
        log._action = Action(attributes["action"])
        log._justification = attributes["justification"]
        log._current_value = attributes["currentValue"]
        log._new_value = attributes["newValue"] if attributes["newValue"] != "None" else None
        
        if log._id >= cls._next_id:
            cls._next_id = log._id + 1
        
        return log

    def get_row(self) -> List[object]:
        return [
            self._id,
            self._timestamp.strftime("%d/%m/%Y - %H:%M:%S"),
            self._organisation,
            str(self._id_number),
            self._action.value,
            self._justification,
            self._current_value,
            self._new_value
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
    def justification(self) -> str:
        return self._justification
    
    @property
    def current_value(self) -> Union[str, DigitalID]:
        return self._current_value
    
    @property
    def new_value(self) -> Optional[str]:
        return self._new_value

    def to_dict(self) -> Dict[str, object]:
        return {
            "id": self._id,
            "timestamp": self._timestamp.strftime("%d/%m/%Y - %H:%M:%S"),
            "organisation": self._organisation,
            "digitalID": str(self._id_number),
            "action": self._action.value,
            "justification": self._justification,
            "currentValue": str(self._current_value),
            "newValue": str(self._new_value) if self._new_value else "None"
        }

    def print(self) -> None:
        """Print formatted log entry for display"""
        print(f"Log ID: {self._id}")
        print(f"Timestamp: {self._timestamp.strftime('%d/%m/%Y - %H:%M:%S')}")
        print(f"Organisation: {self._organisation}")
        print(f"Digital ID: {self._id_number}")
        print(f"Action: {self._action.value}")
        print(f"Justification: {self._justification}")
        print(f"Current Value: {self._current_value}")
        if self._new_value:
            print(f"New Value: {self._new_value}")
        print("-" * 50)
