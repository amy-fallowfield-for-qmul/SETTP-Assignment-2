from typing import Any
from Common.singleton import SingletonMeta
from Config.constants import MAX_AGE

class VerificationValidator(metaclass=SingletonMeta):
    """Singleton validator for verification query inputs"""

    def validate_minimum_age(self, age: Any) -> int:
        """
        Validates the following:
        - Values must be integers (or convertible to int)
        - Values must be non-negative
        - Values must be less than MAX_AGE
        """

        try:
            age_int = int(age)
        except (ValueError, TypeError):
            raise ValueError("Minimum age must be an integer")

        if age_int < 0:
            raise ValueError("Minimum age cannot be negative")

        if age_int >= MAX_AGE:
            raise ValueError(f"Minimum age must be less than {MAX_AGE}")

        return age_int
