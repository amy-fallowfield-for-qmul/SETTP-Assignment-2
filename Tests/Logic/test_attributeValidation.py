import pytest
from datetime import date
from Logic.attributeValidator import Validator
from Config.constants import MAX_AGE
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

class TestValidatorAddress:
    """Tests for address validation"""

    def test_valid_address(self, validator: Validator) -> None:
        result = validator.validate_attribute("address", "123 Main Street , London , M1 1AA")
        assert result == "123 Main Street, London, M1 1AA"

    def test_address_with_spaces_around_commas(self, validator: Validator) -> None:
        result = validator.validate_attribute("address", "123 Main Street , London , M1 1AA")
        assert result == "123 Main Street, London, M1 1AA"

    def test_non_string_address(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="Address must be a string"):
            validator.validate_attribute("address", 123)

    def test_empty_address(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="Address string cannot be empty"):
            validator.validate_attribute("address", "")

    def test_whitespace_address(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="Address string cannot be empty"):
            validator.validate_attribute("address", "  ")

    def test_address_missing_components(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="Address must contain exactly 3 parts"):
            validator.validate_attribute("address", "123 Main Street, London")

    def test_address_too_many_components(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="Address must contain exactly 3 parts"):
            validator.validate_attribute("address", "123, Main Street, Apartment 4B, London, M1 1AA")

    def test_empty_address_line(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="Address must contain exactly 3 parts"):
            validator.validate_attribute("address", ", London, M1 1AA")

    def test_invalid_town_or_city_with_numbers(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="Town or city cannot contain numbers"):
            validator.validate_attribute("address", "123 Main Street, London123, M1 1AA")

    def test_invalid_postcode_format(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="Invalid UK postcode format"):
            validator.validate_attribute("address", "123 Main Street, London, INVALID")

class TestValidatorNationalInsurance:
    """Tests for National Insurance number validation"""

    def test_valid_ni_number(self, validator: Validator) -> None:
        result = validator.validate_attribute("national_insurance", "AB123456C")
        assert result == "AB123456C"

    def test_ni_number_with_spaces(self, validator: Validator) -> None:
        result = validator.validate_attribute("national_insurance", "AB 12 34 56 C")
        assert result == "AB123456C"

    def test_lowercase_ni_number(self, validator: Validator) -> None:
        result = validator.validate_attribute("national_insurance", "ab123456c")
        assert result == "AB123456C"

    def test_non_string_ni_number(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="National Insurance number must be a string"):
            validator.validate_attribute("national_insurance", 123456789)

    def test_wrong_format_ni_number(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="National Insurance number must be in format AB123456C"):
            validator.validate_attribute("national_insurance", "AB12345")

    def test_invalid_first_letter(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="National Insurance number cannot start with D"):
            validator.validate_attribute("national_insurance", "DB123456C")

    def test_invalid_second_letter(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="National Insurance number cannot have I as second letter"):
            validator.validate_attribute("national_insurance", "AI123456C")

    def test_invalid_combination(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="National Insurance number cannot begin with BG"):
            validator.validate_attribute("national_insurance", "BG123456C")

    def test_invalid_final_letter(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="National Insurance number must end with A, B, C, or D"):
            validator.validate_attribute("national_insurance", "AB123456E")

class TestValidatorPostcode:
    """Tests for postcode validation"""

    def test_valid_postcode_an_naa(self, validator: Validator) -> None:
        result = validator._validate_postcode("M1 1AA")
        assert result == "M1 1AA"

    def test_valid_postcode_ann_naa(self, validator: Validator) -> None:
        result = validator._validate_postcode("M11 1AA")
        assert result == "M11 1AA"

    def test_valid_postcode_aan_naa(self, validator: Validator) -> None:
        result = validator._validate_postcode("MM1 1AA")
        assert result == "MM1 1AA"

    def test_valid_postcode_aann_naa(self, validator: Validator) -> None:
        result = validator._validate_postcode("MM11 1AA")
        assert result == "MM11 1AA"

    def test_valid_postcode_ana_naa_with_third_letter(self, validator: Validator) -> None:
        result = validator._validate_postcode("M1A 1AA")
        assert result == "M1A 1AA"

    def test_valid_postcode_aana_naa_with_third_letter(self, validator: Validator) -> None:
        result = validator._validate_postcode("MM1A 1AA")
        assert result == "MM1A 1AA"

    def test_invalid_postcode_first_letter(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="Postcode cannot start with Q"):
            validator._validate_postcode("Q1 1AA")

    def test_invalid_postcode_second_letter(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="Postcode cannot have I as second letter"):
            validator._validate_postcode("MI1 1AA")

    def test_invalid_postcode_third_letter(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="Postcode cannot have I in third position"):
            validator._validate_postcode("M1I 1AA")

    def test_invalid_postcode_second_half_letter(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="Postcode cannot have C in second half"):
            validator._validate_postcode("M1 1CA")

    def test_invalid_postcode_basic_format_no_space(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="Invalid UK postcode format"):
            validator._validate_postcode("M11AA")

    def test_invalid_postcode_no_digits(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="Invalid UK postcode format"):
            validator._validate_postcode("MA AAA")

    def test_invalid_postcode_too_many_digits(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="Invalid UK postcode format"):
            validator._validate_postcode("M123 1AA")

    def test_postcode_case_handling(self, validator: Validator) -> None:
        result = validator._validate_postcode("m1 1aa")
        assert result == "M1 1AA"

class TestValidatorDataPersistence:
    """Tests that validated data is cleaned in place"""

    def test_data_is_cleaned_in_place(self, validator: Validator) -> None:
        attributes = new_person_dict.copy()
        attributes["first_name"] = "   john   "
        validator.validate_all_attributes(attributes)
        assert attributes["first_name"] == "John"

class TestValidateMinimumAgeAccepts:
    """Tests for valid minimum age inputs"""

    def test_accepts_positive_int(self, validator: Validator) -> None:
        assert validator.validate_minimum_age(18) == 18

    def test_accepts_zero(self, validator: Validator) -> None:
        assert validator.validate_minimum_age(0) == 0

    def test_accepts_string_representation_of_int(self, validator: Validator) -> None:
        assert validator.validate_minimum_age("21") == 21

    def test_accepts_value_one_below_max(self, validator: Validator) -> None:
        assert validator.validate_minimum_age(MAX_AGE - 1) == MAX_AGE - 1

    def test_truncates_float(self, validator: Validator) -> None:
        assert validator.validate_minimum_age(5.7) == 5

class TestValidateMinimumAgeRejectsNonInteger:
    """Tests inputs that cannot be coerced to int"""

    def test_rejects_non_numeric_string(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="must be an integer"):
            validator.validate_minimum_age("eighteen")

    def test_rejects_none(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="must be an integer"):
            validator.validate_minimum_age(None)

    def test_rejects_empty_string(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="must be an integer"):
            validator.validate_minimum_age("")

    def test_rejects_string_with_decimal(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="must be an integer"):
            validator.validate_minimum_age("5.7")

class TestValidateMinimumAgeRejectsOutOfRange:
    """Tests for non-negative and upper-bound rules"""

    def test_rejects_negative(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match="cannot be negative"):
            validator.validate_minimum_age(-1)

    def test_rejects_max_age(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match=f"must be less than {MAX_AGE}"):
            validator.validate_minimum_age(MAX_AGE)

    def test_rejects_above_max_age(self, validator: Validator) -> None:
        with pytest.raises(ValueError, match=f"must be less than {MAX_AGE}"):
            validator.validate_minimum_age(MAX_AGE + 1)
