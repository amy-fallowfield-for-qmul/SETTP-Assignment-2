import pytest
from Logic.verificationValidator import VerificationValidator
from Config.constants import MAX_AGE

@pytest.fixture
def validator() -> VerificationValidator:
    return VerificationValidator()

class TestValidateMinimumAgeAccepts:
    """Tests for valid minimum age inputs"""

    def test_accepts_positive_int(self, validator: VerificationValidator) -> None:
        assert validator.validate_minimum_age(18) == 18

    def test_accepts_zero(self, validator: VerificationValidator) -> None:
        assert validator.validate_minimum_age(0) == 0

    def test_accepts_string_representation_of_int(self, validator: VerificationValidator) -> None:
        assert validator.validate_minimum_age("21") == 21

    def test_accepts_value_one_below_max(self, validator: VerificationValidator) -> None:
        assert validator.validate_minimum_age(MAX_AGE - 1) == MAX_AGE - 1

    def test_truncates_float(self, validator: VerificationValidator) -> None:
        assert validator.validate_minimum_age(5.7) == 5

class TestValidateMinimumAgeRejectsNonInteger:
    """Tests inputs that cannot be coerced to int"""

    def test_rejects_non_numeric_string(self, validator: VerificationValidator) -> None:
        with pytest.raises(ValueError, match="must be an integer"):
            validator.validate_minimum_age("eighteen")

    def test_rejects_none(self, validator: VerificationValidator) -> None:
        with pytest.raises(ValueError, match="must be an integer"):
            validator.validate_minimum_age(None)

    def test_rejects_empty_string(self, validator: VerificationValidator) -> None:
        with pytest.raises(ValueError, match="must be an integer"):
            validator.validate_minimum_age("")

    def test_rejects_string_with_decimal(self, validator: VerificationValidator) -> None:
        with pytest.raises(ValueError, match="must be an integer"):
            validator.validate_minimum_age("5.7")

class TestValidateMinimumAgeRejectsOutOfRange:
    """Tests for non-negative and upper-bound rules"""

    def test_rejects_negative(self, validator: VerificationValidator) -> None:
        with pytest.raises(ValueError, match="cannot be negative"):
            validator.validate_minimum_age(-1)

    def test_rejects_max_age(self, validator: VerificationValidator) -> None:
        with pytest.raises(ValueError, match=f"must be less than {MAX_AGE}"):
            validator.validate_minimum_age(MAX_AGE)

    def test_rejects_above_max_age(self, validator: VerificationValidator) -> None:
        with pytest.raises(ValueError, match=f"must be less than {MAX_AGE}"):
            validator.validate_minimum_age(MAX_AGE + 1)
