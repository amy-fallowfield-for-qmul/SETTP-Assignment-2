from dataclasses import dataclass
from Logic.organisation import Organisation


@dataclass(frozen=True)
class RequestContext:
    """Stores organisation and justification which are essential for any request"""

    organisation: Organisation
    justification: str
