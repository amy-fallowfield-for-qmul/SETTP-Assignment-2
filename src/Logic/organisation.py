from dataclasses import dataclass, field
from typing import Tuple

@dataclass(frozen=True)
class Organisation:
    """Stores display name and attributes for organisations to pass to logical components"""

    name: str
    accessible_attributes: Tuple[str, ...] = field(default_factory=tuple)
    verifiable_attributes: Tuple[str, ...] = field(default_factory=tuple)

    def can_read(self, attribute: str) -> bool:
        return attribute in self.accessible_attributes

    def can_verify(self, attribute: str) -> bool:
        return attribute in self.verifiable_attributes
