from dataclasses import dataclass

@dataclass(frozen=True)
class IdentityClaim:
    """Stores all attributes needed to process an identity request"""

    first_name: str
    surname: str
    date_of_birth: str
