import pytest
from datetime import date
from Logic.attributeValidator import Validator
from Tests.shared_test_data import new_person_dict

@pytest.fixture
def validator() -> Validator:
    return Validator()

class TestValidatorRequiredAttributes:
    """Tests for required attribute validation"""

    def test_valid_data_passes_with_justification(self, validator: Validator) -> None:
        attributes = new_person_dict.copy()
        attributes["justification"] = "New registration"
        validator.validate_all_attributes(attributes)

    def test_valid_data_passes_without_justification(self, validator: Validator) -> None:
        validator.validate_all_attributes(new_person_dict)

    def test_missing_attribute(self, validator: Validator) -> None:
        attributes = new_person_dict.copy()
        del attributes["first_name"]
        with pytest.raises(ValueError, match="Missing required attributes"):
            validator.validate_all_attributes(attributes)

    def test_empty_data(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="Missing required attributes"):
            validator.validate_all_attributes({})

    def test_unexpected_attribute(self, validator: Validator) -> None:
        attributes = new_person_dict.copy()
        attributes["unexpected"] = "I shouldn't be here"
        with pytest.raises(ValueError, match="Unexpected attribute"):
            validator.validate_all_attributes(attributes)

class TestValidateSingleAttribute:
    """Tests for validate_attribute"""

    def test_validate_first_name(self, validator: Validator) -> None:
        assert validator.validate_attribute("first_name", "john") == "John"

    def test_validate_surname(self, validator: Validator) -> None:
        assert validator.validate_attribute("surname", "smith") == "Smith"

    def test_validate_status(self, validator: Validator) -> None:
        assert validator.validate_attribute("status", "active") == "active"

    def test_validate_justification(self, validator: Validator) -> None:
        assert validator.validate_attribute("justification", "New user") == "New User"

    def test_invalid_attribute_name(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="No validation defined for attribute"):
            validator.validate_attribute("unknown", "value")

    def test_validate_attribute_rejects_invalid_value(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="cannot contain numbers or special characters"):
            validator.validate_attribute("first_name", "John123")

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
        attributes = new_person_dict.copy()
        attributes["first_name"] = "   John   "
        validator.validate_all_attributes(attributes)
        assert attributes["first_name"] == "John"

    def test_title_cases(self, validator: Validator) -> None:
        attributes = new_person_dict.copy()
        attributes["first_name"] = "JOHN"
        validator.validate_all_attributes(attributes)
        assert attributes["first_name"] == "John"

    def test_strings_with_spaces(self, validator: Validator) -> None:
        attributes = new_person_dict.copy()
        attributes["first_name"] = "John Jr"
        validator.validate_all_attributes(attributes)
        assert attributes["first_name"] == "John Jr"

    def test_strings_with_numbers(self, validator: Validator) -> None:
        attributes = new_person_dict.copy()
        attributes["first_name"] = "John123"
        with pytest.raises(ValueError, match="cannot contain numbers or special characters"):
            validator.validate_all_attributes(attributes)

    def test_strings_with_special_characters(self, validator: Validator) -> None:
        attributes = new_person_dict.copy()
        attributes["first_name"] = "John!"
        with pytest.raises(ValueError, match="cannot contain numbers or special characters"):
            validator.validate_all_attributes(attributes)

    def test_empty_strings(self, validator: Validator) -> None:
        attributes = new_person_dict.copy()
        attributes["first_name"] = ""
        with pytest.raises(ValueError, match="cannot contain numbers or special characters"):
            validator.validate_all_attributes(attributes)

    def test_whitespace_only_strings(self, validator: Validator) -> None:
        attributes = new_person_dict.copy()
        attributes["first_name"] = "   "
        with pytest.raises(ValueError, match="cannot contain numbers or special characters"):
            validator.validate_all_attributes(attributes)

    def test_non_string(self, validator: Validator) -> None:
        attributes = new_person_dict.copy()
        attributes["first_name"] = 123
        with pytest.raises(ValueError, match="must be a string"):
            validator.validate_all_attributes(attributes)

class TestValidatorDateOfBirth:
    """Tests for date of birth validation"""

    def test_valid_date(self, validator: Validator) -> None:
        attributes = new_person_dict.copy()
        validator.validate_all_attributes(attributes)

    def test_non_string_date(self, validator: Validator) -> None:
        attributes = new_person_dict.copy()
        attributes["date_of_birth"] = 20000101
        with pytest.raises(ValueError, match="must be a string"):
            validator.validate_all_attributes(attributes)

    def test_wrong_format(self, validator: Validator) -> None:
        attributes = new_person_dict.copy()
        attributes["date_of_birth"] = "01-01-2000"
        with pytest.raises(ValueError, match="YYYY-MM-DD"):
            validator.validate_all_attributes(attributes)

    def test_slashes_instead_of_dashes(self, validator: Validator) -> None:
        attributes = new_person_dict.copy()
        attributes["date_of_birth"] = "2000/01/01"
        with pytest.raises(ValueError, match="YYYY-MM-DD"):
            validator.validate_all_attributes(attributes)

    def test_invalid_month(self, validator: Validator) -> None:
        attributes = new_person_dict.copy()
        attributes["date_of_birth"] = "2000-13-02"
        with pytest.raises(ValueError):
            validator.validate_all_attributes(attributes)

    def test_invalid_day(self, validator: Validator) -> None:
        attributes = new_person_dict.copy()
        attributes["date_of_birth"] = "2000-02-30"
        with pytest.raises(ValueError):
            validator.validate_all_attributes(attributes)

    def test_future_date(self, validator: Validator) -> None:
        attributes = new_person_dict.copy()
        attributes["date_of_birth"] = "3000-01-01"
        with pytest.raises(ValueError, match="cannot be in the future"):
            validator.validate_all_attributes(attributes)

    def test_today(self, validator: Validator) -> None:
        today = date.today().isoformat()
        attributes = new_person_dict.copy()
        attributes["date_of_birth"] = today
        validator.validate_all_attributes(attributes)

class TestValidatorDataPersistence:
    """Tests that validated data is cleaned in place"""

    def test_data_is_cleaned_in_place(self, validator: Validator) -> None:
        attributes = new_person_dict.copy()
        attributes["first_name"] = "   john   "
        validator.validate_all_attributes(attributes)
        assert attributes["first_name"] == "John"
