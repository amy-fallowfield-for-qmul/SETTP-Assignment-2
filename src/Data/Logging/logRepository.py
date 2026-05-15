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
        headers = self._get_csv_headers()
        rows: List[List[str]] = []
        for log in self._repository.values():
            log_dict = log.to_dict()
            rows.append([log_dict[header] for header in headers])
        return rows

    def _create_object_from_csv_row(self, row: List[str]) -> Log:
        attributes = dict(zip(self._get_csv_headers(), row))
        return Log.from_csv(attributes)
