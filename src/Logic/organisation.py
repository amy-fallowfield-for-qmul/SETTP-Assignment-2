from dataclasses import dataclass, field
from typing import Tuple

@dataclass(frozen=True)
class Organisation:
    """Stores display name and attributes for organisations to pass to logical components"""

    name: str
    accessible_attributes: Tuple[str, ...] = field(default_factory=tuple)
    verifiable_attributes: Tuple[str, ...] = field(default_factory=tuple)
