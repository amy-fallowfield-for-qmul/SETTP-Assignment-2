import csv
from typing import List
from Common.singleton import SingletonMeta

class DataStorage(metaclass=SingletonMeta):
    """Singleton handler for CSV file input/output"""

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
