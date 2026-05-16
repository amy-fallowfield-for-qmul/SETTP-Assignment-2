from typing import Optional
from Common.singleton import SingletonMeta
from Logic.period import Period
from Data.Logging.logRepository import LogRepository
from Data.Logging.log import Log, Action

class SuspensionAnalyser(metaclass=SingletonMeta):
    """Analyses log history to determine if ID was suspended within a given period"""

    SUSPENDED_VALUES = ["suspended", "revoked"]

    def __init__(self) -> None:
        self.LOG_REPOSITORY = LogRepository()

    def was_suspended_in_period(self, period: Period, id_number: int) -> bool:
        all_logs = self.LOG_REPOSITORY.get_all()
        relevant_logs = [
            log for log in all_logs.values()
            if log.id_number == id_number and self._log_updates_status(log)
        ]
        
        return (
            self._has_suspension_during_period(relevant_logs, period)
            or self._was_suspended_at_period_start(relevant_logs, period.start_date)
        )

    def _has_suspension_during_period(self, logs, period: Period) -> bool:
        return any(
            period.is_in_period(log.timestamp) and log.new_value in self.SUSPENDED_VALUES
            for log in logs
        )

    def _was_suspended_at_period_start(self, logs, start_date: str) -> bool:
        most_recent_update = None
        for log in logs:
            if self._log_most_recent(log, start_date, most_recent_update):
                most_recent_update = log
        return most_recent_update is not None and most_recent_update.new_value in self.SUSPENDED_VALUES

    def _log_most_recent(self, log: Log, date: str, most_recent_update: Optional[Log]) -> bool:
        log_before_period = str(log.timestamp) < date
        log_most_recent_than_current = most_recent_update is None or log.timestamp > most_recent_update.timestamp
        return log_before_period and log_most_recent_than_current

    def _log_updates_status(self, log: Log) -> bool:
        if log.action != Action.UPDATE:
            return False
        return log.attribute == "status"
