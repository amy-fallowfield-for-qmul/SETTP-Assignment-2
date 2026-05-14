import pytest
from Data.Attributes.address import Address


class TestAddressCreation:
    """Tests for the Address constructor"""

    def test_create_address_stores_components(self) -> None:
        address = Address("123 This Street", "London", "M2 1AA")

        assert address.address_line == "123 This Street"
        assert address.town_city == "London"
        assert address.postcode == "M2 1AA"

    def test_constructor_strips_whitespace_from_address_line(self) -> None:
        address = Address("  123 This Street  ", "London", "M2 1AA")
        assert address.address_line == "123 This Street"

    def test_constructor_strips_whitespace_from_town_city(self) -> None:
        address = Address("123 This Street", "  London  ", "M2 1AA")
        assert address.town_city == "London"

    def test_constructor_strips_whitespace_from_postcode(self) -> None:
        address = Address("123 This Street", "London", "  M2 1AA  ")
        assert address.postcode == "M2 1AA"

class TestAddressFromString:
    """Tests for Address.from_string parsing"""

    def test_from_string_parses_three_parts(self) -> None:
        address = Address.from_string("123 This Street, London, M2 1AA")

        assert address.address_line == "123 This Street"
        assert address.town_city == "London"
        assert address.postcode == "M2 1AA"

    def test_from_string_strips_whitespace_around_each_part(self) -> None:
        address = Address.from_string("  123 This Street  ,  London  ,  M2 1AA  ")

        assert address.address_line == "123 This Street"
        assert address.town_city == "London"
        assert address.postcode == "M2 1AA"

    def test_from_string_uppercases_postcode(self) -> None:
        address = Address.from_string("123 This Street, London, m2 1aa")
        assert address.postcode == "M2 1AA"

    def test_from_string_empty_raises(self) -> None:
        with pytest.raises(ValueError, match="Address string cannot be empty"):
            Address.from_string("")

    def test_from_string_whitespace_only_raises(self) -> None:
        with pytest.raises(ValueError, match="Address string cannot be empty"):
            Address.from_string("   ")

    def test_from_string_non_string_raises(self) -> None:
        with pytest.raises(ValueError, match="Address string cannot be empty"):
            Address.from_string(None)   # type: ignore[arg-type]

    def test_from_string_too_few_parts_raises(self) -> None:
        with pytest.raises(ValueError, match="Address must contain exactly 3 parts"):
            Address.from_string("123 This Street, London")

    def test_from_string_too_many_parts_raises(self) -> None:
        with pytest.raises(ValueError, match="Address must contain exactly 3 parts"):
            Address.from_string("123 This Street, Flat 1, London, M2 1AA")

    def test_from_string_ignores_empty_parts_between_commas(self) -> None:
        address = Address.from_string("123 This Street, London, M2 1AA,")

        assert address.address_line == "123 This Street"
        assert address.town_city == "London"
        assert address.postcode == "M2 1AA"


class TestAddressFormatting:
    """Tests for Address serialisation methods"""

    def setup_method(self) -> None:
        self.address = Address("123 This Street", "London", "M2 1AA")

    def test_to_dict(self) -> None:
        assert self.address.to_dict() == {
            "address_line": "123 This Street",
            "town_city": "London",
            "postcode": "M2 1AA",
        }

    def test_str(self) -> None:
        assert str(self.address) == "123 This Street, London, M2 1AA"


class TestAddressEquality:
    """Tests for Address Equality"""

    def test_equal_addresses_compare_equal(self) -> None:
        a = Address("123 This Street", "London", "M2 1AA")
        b = Address("123 This Street", "London", "M2 1AA")
        assert a == b

    def test_different_address_line_not_equal(self) -> None:
        a = Address("123 This Street", "London", "M2 1AA")
        b = Address("456 That Street", "London", "M2 1AA")
        assert a != b

    def test_different_town_city_not_equal(self) -> None:
        a = Address("123 This Street", "London", "M1 1AA")
        b = Address("123 This Street", "Manchester", "M1 1AA")
        assert a != b

    def test_different_postcode_not_equal(self) -> None:
        a = Address("123 This Street", "London", "M2 1AA")
        b = Address("123 This Street", "London", "M2 1XX")
        assert a != b

    def test_case_does_not_break_equality(self) -> None:
        a = Address("123 This Street", "London", "m2 1aa")
        b = Address("123 This Street", "London", "M2 1AA")
        assert a == b

    def test_not_equal_to_non_address_type(self) -> None:
        a = Address("123 This Street", "London", "M2 1AA")
        assert a != "123 This Street, London, M2 1AA"
        assert a != {"address_line": "123 This Street", "town_city": "London", "postcode": "M2 1AA"}
