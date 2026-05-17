from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class Period:
    """Holds start and end dates for querying in a set period"""

    start_date: str
    end_date: str

    def __post_init__(self) -> None:
        from Logic.attributeValidator import Validator
        validator = Validator()
        validator.validate_date(self.start_date)
        validator.validate_date(self.end_date)

    def is_in_period(self, timestamp: datetime) -> bool:
        start = datetime.strptime(self.start_date, "%Y-%m-%d")
        end = datetime.strptime(self.end_date, "%Y-%m-%d")
        return start <= timestamp <= end

    def __str__(self) -> str:
        return f"{self.start_date} to {self.end_date}"
