from typing import Dict, List
from Data.digitalID import DigitalID
from constants import CSV_PATH, DIGITAL_ID_ALL_FIELDS
from Data.repositoryABC import RepositoryABC

class DigitalIDRepository(RepositoryABC):
    """Singleton repository for storing and managing Digital IDs"""

    def _initialise(self) -> None:
        self._repository: Dict[int, DigitalID] = {}

    def add(self, digitalID: DigitalID) -> None:
        self._repository[digitalID.id] = digitalID

    def get_from_id(self, id: int) -> DigitalID:
        return self._repository[id]
    
    def get_all(self) -> Dict[int, DigitalID]:
        return self._repository

    def _get_csv_path(self) -> str:
        return CSV_PATH

    def _get_csv_headers(self) -> List[str]:
        return DIGITAL_ID_ALL_FIELDS

    def _get_rows_for_csv(self) -> List[List[str]]:
        rows = []
        for digitalID in self._repository.values():
            rows.append([
                str(digitalID.id),
                digitalID.status.value,
                digitalID.first_name,
                digitalID.surname,
                digitalID.date_of_birth
            ])
        return rows

    def _create_object_from_csv_row(self, row: List[str]) -> DigitalID:
        attributes = {
            "id": row[0],
            "status": row[1],
            "firstName": row[2],
            "surname": row[3],
            "dateOfBirth": row[4]
        }
        return DigitalID.from_csv(attributes)
