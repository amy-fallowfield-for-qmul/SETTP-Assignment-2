import os
from typing import List
from Data.log import Log
from Data.repositoryABC import RepositoryABC

class LogRepository(RepositoryABC):
    """Singleton repository for storing and managing log entries"""

    def _initialise(self) -> None:
        self._repository: List[Log] = []

    def add(self, log: Log) -> None:
        self._repository.append(log)

    def get_all(self) -> List[Log]:
        return self._repository

    def _get_csv_path(self) -> str:
        return os.path.join(os.path.dirname(__file__), "../../logs.csv")

    def _get_csv_headers(self) -> List[str]:
        return ["timestamp", "organisation", "digitalID", "action", "justification", "currentValue", "newValue"]

    def _get_rows_for_csv(self) -> List[List[str]]:
        rows = []
        for log in self._repository:
            row = log.get_row()
            rows.append(row)
        return rows

    def _create_object_from_csv_row(self, row: List[str]) -> Log:
        return Log.from_csv_row(row)
