import os
from typing import List, Dict
from Data.log import Log
from Data.repositoryABC import RepositoryABC
from constants import LOG_PATH, LOG_HEADERS

class LogRepository(RepositoryABC):
    """Singleton repository for storing and managing log entries"""

    def _initialise(self) -> None:
        self._repository: Dict[int, Log] = {}

    def add(self, log: Log) -> None:
        self._repository[log.id] = log

    def get_from_id(self, id: int) -> Log:
        return self._repository[id]

    def get_all(self) -> Dict[int, Log]:
        return self._repository

    def _get_csv_path(self) -> str:
        return LOG_PATH

    def _get_csv_headers(self) -> List[str]:
        return LOG_HEADERS

    def _get_rows_for_csv(self) -> List[List[str]]:
        rows = []
        for log in self._repository.values():
            row = log.get_row()
            rows.append(row)
        return rows

    def _create_object_from_csv_row(self, row: List[str]) -> Log:
        attributes = {
            "id": row[0],
            "timestamp": row[1],
            "organisation": row[2],
            "digitalID": row[3],
            "action": row[4],
            "justification": row[5],
            "currentValue": row[6],
            "newValue": row[7]
        }
        return Log.from_csv(attributes)
