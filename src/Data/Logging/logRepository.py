from typing import List, Dict
from .log import Log
from ..repositoryABC import RepositoryABC
from Config.constants import LOG_PATH, LOG_HEADERS

class LogRepository(RepositoryABC[Log]):
    """Singleton repository for storing and managing log entries"""

    def _initialise(self) -> None:
        self._repository: Dict[int, Log] = {}

    def add(self, log: Log) -> None:
        if log.id in self._repository:
            raise ValueError(f"Log with id {log.id} already exists")
        self._repository[log.id] = log

    def _get_csv_path(self) -> str:
        return LOG_PATH

    def _get_csv_headers(self) -> List[str]:
        return LOG_HEADERS

    def _get_rows_for_csv(self) -> List[List[str]]:
        rows: List[List[str]] = []
        for log in self._repository.values():
            row = log.get_row()
            rows.append(row)
        return rows

    def _create_object_from_csv_row(self, row: List[str]) -> Log:
        attributes = {
            "id": row[0],
            "timestamp": row[1],
            "accepted": row[2],
            "organisation": row[3],
            "digitalID": row[4],
            "action": row[5],
            "justification": row[6],
            "currentValue": row[7],
            "newValue": row[8],
            "attribute": row[9],
            "comparativeValue": row[10]
        }
        return Log.from_csv(attributes)
