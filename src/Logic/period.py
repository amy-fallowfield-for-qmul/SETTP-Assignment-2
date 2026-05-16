from dataclasses import dataclass

@dataclass(frozen=True)
class Period:
    """Holds start and end dates for querying in a set period"""

    start_date: str
    end_date: str
