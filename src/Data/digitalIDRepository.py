from typing import Dict
from Data.digitalID import DigitalID
from constants import CSV_PATH, DIGITAL_ID_ALL_FIELDS
import csv

class DigitalIDRepository:
    """Singleton repository for storing and managing Digital IDs"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, '_initialised'):
            self._initialised = True
            self._repository: Dict[int, DigitalID] = {}

    def add_id(self, digitalID: DigitalID) -> None:
        self._repository[digitalID.id] = digitalID

    def get_id(self, id: int) -> DigitalID:
        return self._repository[id]
    
    def get_all_ids(self) -> Dict[int, DigitalID]:
        return self._repository

    def save_to_csv(self) -> None:
        rows = []
        for digitalID in self._repository.values():
            rows.append([
                str(digitalID.id),
                digitalID.status.value,
                digitalID.first_name,
                digitalID.surname,
                digitalID.date_of_birth
            ])
        try:
            with open(CSV_PATH, "w") as file:
                writer = csv.writer(file)
                writer.writerow(DIGITAL_ID_ALL_FIELDS)

                for row in rows:
                    writer.writerow(row)
        except Exception as e:
            raise(e)

    def load_from_csv(self) -> None:
        try:
            with open(CSV_PATH, "r") as file:
                reader = csv.reader(file)
                next(reader)
                rows = [row for row in reader]
        except Exception as e:
            raise(e)

        for row in rows:
            attributes = {
                "id": row[0],
                "status": row[1],
                "firstName": row[2],
                "surname": row[3],
                "dateOfBirth": row[4]
            }
            digitalID = DigitalID.from_csv(attributes)
            self.add_id(digitalID)
