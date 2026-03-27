import os
from typing import List
from Data.log import Log, Action
from Data.dataStorage import DataStorage

class LogRepository:
    """Singleton repository for storing and managing log entries"""

    CSV_PATH = os.path.join(os.path.dirname(__file__), "../../logs.csv")
    CSV_HEADERS = ["timestamp", "organisation", "digitalID", "action", "justification", "currentValue", "newValue"]
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, '_initialised'):
            self._initialised = True
            self._logs: List[Log] = []
            self._storage = DataStorage()

    def add_log(self, log: Log) -> None:
        self._logs.append(log)

    def get_all_logs(self) -> List[Log]:
        return self._logs

    def save_to_csv(self) -> None:
        rows = []
        for log in self._logs:
            row = log.get_row()
            rows.append(row)
        self._storage.save_to_csv(self.CSV_PATH, self.CSV_HEADERS, rows)

    def load_from_csv(self) -> None:
        rows = self._storage.load_from_csv(self.CSV_PATH)

        for row in rows:
            log = Log.from_csv_row(row)
            self.add_log(log)
