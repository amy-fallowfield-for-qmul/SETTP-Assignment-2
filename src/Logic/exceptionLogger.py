from contextlib import contextmanager
from typing import Optional
from Data.Logging.logRepository import LogRepository
from Data.Logging.log import Log, Action
from Logic.requestContext import RequestContext

@contextmanager
def record_failures(
    log_repository: LogRepository,
    action: Action,
    context: RequestContext,
    id_number: int,
    attribute: Optional[str] = None,
):
    safe_justification = context.justification or "Unknown justification"
    try:
        yield safe_justification
    except Exception as e:
        log_repository.add(Log.for_failure(context.organisation.name, id_number, action, safe_justification, str(e), attribute))
        raise
