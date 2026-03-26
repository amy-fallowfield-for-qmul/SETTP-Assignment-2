import pytest
from datetime import date
from Logic.attributeValidator import Validator

@pytest.fixture
def validator() -> Validator:
    return Validator()

class TestValidatorRequiredAttributes:
    """Tests for required attribute validation"""

    def test_valid_data_passes(self, validator: Validator) -> None:
        validator.validate_all_attributes({"firstName": "John", "surname": "Smith", "dateOfBirth": "2000-01-01"})

    def test_missing_first_name(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="Missing required attributes"):
            validator.validate_all_attributes({"surname": "Smith", "dateOfBirth": "2000-01-01"})

    def test_missing_surname(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="Missing required attributes"):
            validator.validate_all_attributes({"firstName": "John", "dateOfBirth": "2000-01-01"})

    def test_missing_date_of_birth(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="Missing required attributes"):
            validator.validate_all_attributes({"firstName": "John", "surname": "Smith"})

    def test_empty_data(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="Missing required attributes"):
            validator.validate_all_attributes({})

    def test_unexpected_attribute(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="Unexpected attribute"):
            validator.validate_all_attributes({"firstName": "John", "surname": "Smith", "dateOfBirth": "2000-01-01", "email": "test@test.com"})

class TestValidateSingleAttribute:
    """Tests for validate_attribute"""

    def test_validate_first_name(self, validator: Validator) -> None:
        assert validator.validate_attribute("firstName", "john") == "John"

    def test_validate_surname(self, validator: Validator) -> None:
        assert validator.validate_attribute("surname", "smith") == "Smith"

    def test_validate_status(self, validator: Validator) -> None:
        assert validator.validate_attribute("status", "active") == "active"

    def test_invalid_attribute_name(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="No validation defined for attribute"):
            validator.validate_attribute("unknown", "value")

    def test_validate_attribute_rejects_invalid_value(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="cannot contain numbers or special characters"):
            validator.validate_attribute("firstName", "John123")

class TestValidatorStatusField:
    """Tests for status validation"""

    def test_valid_active_status(self, validator: Validator) -> None:
        assert validator.validate_attribute("status", "active") == "active"

    def test_valid_suspended_status(self, validator: Validator) -> None:
        assert validator.validate_attribute("status", "suspended") == "suspended"

    def test_valid_revoked_status(self, validator: Validator) -> None:
        assert validator.validate_attribute("status", "revoked") == "revoked"

    def test_status_case_insensitive(self, validator: Validator) -> None:
        assert validator.validate_attribute("status", "ACTIVE") == "active"

    def test_invalid_status(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="must be 'active', 'suspended', or 'revoked'"):
            validator.validate_attribute("status", "invalid")

class TestValidatorStringFields:
    """Tests for string validation"""

    def test_strips_whitespace(self, validator: Validator) -> None:
        data = {"firstName": "  John  ", "surname": "Smith", "dateOfBirth": "2000-01-01"}
        validator.validate_all_attributes(data)
        assert data["firstName"] == "John"

    def test_title_cases(self, validator: Validator) -> None:
        data = {"firstName": "john", "surname": "SMITH", "dateOfBirth": "2000-01-01"}
        validator.validate_all_attributes(data)
        assert data["firstName"] == "John"

    def test_strings_with_spaces(self, validator: Validator) -> None:
        data = {"firstName": "John Jr", "surname": "Smith", "dateOfBirth": "2000-01-01"}
        validator.validate_all_attributes(data)
        assert data["firstName"] == "John Jr"

    def test_strings_with_numbers(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="cannot contain numbers or special characters"):
            validator.validate_all_attributes({"firstName": "John123", "surname": "Smith", "dateOfBirth": "2000-01-01"})

    def test_strings_with_special_characters(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="cannot contain numbers or special characters"):
            validator.validate_all_attributes({"firstName": "John!", "surname": "Smith", "dateOfBirth": "2000-01-01"})

    def test_empty_strings(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="cannot contain numbers or special characters"):
            validator.validate_all_attributes({"firstName": "", "surname": "Smith", "dateOfBirth": "2000-01-01"})

    def test_whitespace_only_strings(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="cannot contain numbers or special characters"):
            validator.validate_all_attributes({"firstName": "   ", "surname": "Smith", "dateOfBirth": "2000-01-01"})

    def test_non_string(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="must be a string"):
            validator.validate_all_attributes({"firstName": 123, "surname": "Smith", "dateOfBirth": "2000-01-01"})

    def test_first_name(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="cannot contain numbers or special characters"):
            validator.validate_all_attributes({"firstName": "John123", "surname": "Smith", "dateOfBirth": "2000-01-01"})

    def test_surname(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="cannot contain numbers or special characters"):
            validator.validate_all_attributes({"firstName": "John", "surname": "Smith123", "dateOfBirth": "2000-01-01"})

class TestValidatorDateOfBirth:
    """Tests for date of birth validation"""

    def test_valid_date(self, validator: Validator) -> None:
        validator.validate_all_attributes({"firstName": "John", "surname": "Smith", "dateOfBirth": "2000-01-01"})

    def test_non_string_date(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="must be a string"):
            validator.validate_all_attributes({"firstName": "John", "surname": "Smith", "dateOfBirth": 20000101})

    def test_wrong_format(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="YYYY-MM-DD"):
            validator.validate_all_attributes({"firstName": "John", "surname": "Smith", "dateOfBirth": "01-01-2000"})

    def test_slashes_instead_of_dashes(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="YYYY-MM-DD"):
            validator.validate_all_attributes({"firstName": "John", "surname": "Smith", "dateOfBirth": "2000/01/01"})

    def test_non_date_string(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="YYYY-MM-DD"):
            validator.validate_all_attributes({"firstName": "John", "surname": "Smith", "dateOfBirth": "hello"})

    def test_invalid_month(self, validator: Validator) -> None:
        with pytest.raises(ValueError):
            validator.validate_all_attributes({"firstName": "John", "surname": "Smith", "dateOfBirth": "2000-13-01"})

    def test_invalid_day(self, validator: Validator) -> None:
        with pytest.raises(ValueError):
            validator.validate_all_attributes({"firstName": "John", "surname": "Smith", "dateOfBirth": "2000-02-31"})

    def test_future_date(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="cannot be in the future"):
            validator.validate_all_attributes({"firstName": "John", "surname": "Smith", "dateOfBirth": "2099-01-01"})

    def test_today(self, validator: Validator) -> None:
        today = date.today().isoformat()
        validator.validate_all_attributes({"firstName": "John", "surname": "Smith", "dateOfBirth": today})

class TestValidatorDataPersistence:
    """Tests that validated data is cleaned in place"""

    def test_data_is_cleaned_in_place(self, validator: Validator) -> None:
        data = {"firstName": "  john  ", "surname": "  SMITH  ", "dateOfBirth": "2000-01-01"}
        validator.validate_all_attributes(data)
        assert data["firstName"] == "John"
        assert data["surname"] == "Smith"
        assert data["dateOfBirth"] == "2000-01-01"
