from contextlib import contextmanager
from typing import Optional
from Data.Logging.logRepository import LogRepository
from Data.Logging.log import Log, Action

@contextmanager
def record_failures(
    log_repository: LogRepository,
    action: Action,
    organisation: str,
    id_number: int,
    justification: str,
    attribute: Optional[str] = None,
):
    safe_justification = justification or "Unknown justification"
    try:
        yield safe_justification
    except Exception as e:
        log_repository.add(Log.for_failure(organisation, id_number, action, safe_justification, str(e), attribute))
        raise
