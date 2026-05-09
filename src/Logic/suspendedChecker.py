from typing import Optional
from datetime import datetime
from Common.singleton import SingletonMeta
from Data.Logging.logRepository import LogRepository
from Data.Logging.log import Log, Action

class SuspendedChecker(metaclass=SingletonMeta):

    SUSPENDED_VALUES = ["suspended", "revoked"]

    def __init__(self) -> None:
        self.LOG_REPOSITORY = LogRepository()

    def id_suspended_in_period(self, start_date: str, end_date: str, id: int) -> bool:
        all_logs = self.LOG_REPOSITORY.get_all()
        relevant_logs = [log for log in all_logs.values() if log.id_number == id]
        most_recent_update = None

        for log in relevant_logs:
            if self._log_updates_status(log):
                if self._log_in_period(log, start_date, end_date):
                    if log.new_value in self.SUSPENDED_VALUES:
                        return True
                elif self._log_most_recent(log, start_date, most_recent_update):
                    most_recent_update = log

        if most_recent_update is not None and most_recent_update.new_value in self.SUSPENDED_VALUES:
            return True

        return False

    def _log_most_recent(self, log: Log, date: str, most_recent_update: Optional[Log]) -> bool:
        log_before_period = str(log.timestamp) < date
        log_most_recent_than_current = most_recent_update == None or log.timestamp > most_recent_update.timestamp

        return log_before_period and log_most_recent_than_current
    
    def _log_updates_status(self, log: Log) -> bool:
        if log.action != Action.UPDATE:
            return False
        return log.attribute == "status"
    
    def _log_in_period(self, log: Log, start_date: str, end_date: str) -> bool:
        start_date_object = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_object = datetime.strptime(end_date, "%Y-%m-%d")
        return start_date_object <= log.timestamp <= end_date_object
