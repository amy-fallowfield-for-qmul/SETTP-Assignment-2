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

    def __init__(self, organisation: str, id_number: int, action: Action, justification: str, current_value: Union[str, DigitalID], new_value: Optional[str]) -> None:
        self._timestamp: datetime = datetime.now()
        self._organisation: str = organisation
        self._id_number: int = id_number
        self._action: Action = action
        self._justification: str = justification
        self._current_value: Union[str, Dict] = current_value.to_dict() if isinstance(current_value, DigitalID) else current_value
        self._new_value: Optional[str] = new_value

    def get_row(self) -> List[object]:
        return [
            self._timestamp.strftime("%d/%m/%Y - %H:%M:%S"),
            self._organisation,
            str(self._id_number),
            self._action.value,
            self._justification,
            self._current_value,
            self._new_value
        ]
