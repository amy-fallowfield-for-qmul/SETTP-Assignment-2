from dataclasses import dataclass
from typing import TYPE_CHECKING
from Logic.organisation import Organisation

if TYPE_CHECKING:
    from Logic.attributeValidator import Validator


@dataclass(frozen=True)
class RequestContext:
    """Stores organisation and justification which are essential for any request"""

    organisation: Organisation
    justification: str

    def assert_can_read(self, attribute: str) -> None:
        if not self.organisation.can_read(attribute):
            raise ValueError(f"Access denied: {self.organisation.name} is not authorized to access '{attribute}' attribute")

    def assert_can_verify(self, attribute: str) -> None:
        if not self.organisation.can_verify(attribute):
            raise ValueError(f"Access denied: {self.organisation.name} is not authorised to verify '{attribute}' attribute")

    def assert_can_perform(self, operation: str) -> None:
        if not self.organisation.can_perform(operation):
            raise ValueError(f"Access denied: {self.organisation.name} is not authorised to perform '{operation}'")

    def validated_justification(self, validator: "Validator") -> str:
        return validator.validate_attribute("justification", self.justification)
