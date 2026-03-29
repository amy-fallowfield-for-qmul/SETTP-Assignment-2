import csv
from typing import List

class DataStorage:
    """Singleton handler for CSV file input/output"""

    _instance = None

    def __new__(cls) -> "DataStorage":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, '_initialised'):
            self._initialised = True

    def save_to_csv(self, path: str, headers: List[str], rows: List[List[str]]) -> None:
        try:
            with open(path, "w") as file:
                writer = csv.writer(file)
                writer.writerow(headers)

                for row in rows:
                    writer.writerow(row)
        except Exception as e:
            raise IOError(f"Failed to save CSV file at {path}: {e}")

    def load_from_csv(self, path: str) -> List[List[str]]:
        try:
            with open(path, "r") as file:
                reader = csv.reader(file)
                next(reader)
                return [row for row in reader]
        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file not found at {path}")
        except Exception as e:
            raise IOError(f"Failed to load CSV file from {path}: {e}")
