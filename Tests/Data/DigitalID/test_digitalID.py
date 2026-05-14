import pytest
from Data.DigitalID.digitalID import DigitalID, Status
from Data.Attributes.address import Address
from Tests.shared_test_data import new_person_dict, from_csv_person_dict

class TestStatus:
    """Tests for the Status enum"""

    def test_status_values(self) -> None:
        assert Status.ACTIVE.value == "active"
        assert Status.SUSPENDED.value == "suspended"
        assert Status.REVOKED.value == "revoked"

    def test_status_members(self) -> None:
        assert set(Status.__members__.keys()) == {"ACTIVE", "SUSPENDED", "REVOKED"}

class TestDigitalIDCreation:
    """Tests for DigitalID constructor"""

    def setup_method(self) -> None:
        DigitalID._next_id = 1

    def test_create_id_from_cli(self) -> None:
        id = DigitalID(new_person_dict)
        result = id.to_dict()
        
        for key, value in new_person_dict.items():
            assert result[key] == value
        assert result["id"] == 1
        assert result["status"] == "active"

    def test_create_id_from_csv(self) -> None:
        id = DigitalID(from_csv_person_dict)
        assert id.to_dict() == from_csv_person_dict

    def test_auto_increment_id(self) -> None:
        id1 = DigitalID(new_person_dict)
        id2 = DigitalID(from_csv_person_dict)
        assert id1.id == 1
        assert id2.id == 2

class TestDigitalIDProperties:
    """Tests for DigitalID getters and setters"""

    def setup_method(self) -> None:
        DigitalID._next_id = 1
        self.id = DigitalID(new_person_dict)

    def test_to_dict(self) -> None:
        result = self.id.to_dict()

        for key, value in new_person_dict.items():
            assert result[key] == value

        assert "id" in result
        assert "status" in result

    def test_str(self) -> None:
        output = str(self.id)
        
        for value in new_person_dict.values():
            assert str(value) in output
        
        assert ":" in output
        assert "," in output

    def test_print(self, capsys) -> None:
        self.id.print()
        captured = capsys.readouterr()
        output = captured.out
        
        assert output.strip() == str(self.id)

    def test_id_is_read_only(self) -> None:
        with pytest.raises(AttributeError):
            setattr(self.id, "id", 99)

    def test_get_status(self) -> None:
        assert self.id.status == Status.ACTIVE

    def test_suspend(self) -> None:
        self.id.suspend()
        assert self.id.status == Status.SUSPENDED

        self.id.activate()
        self.id.suspend()
        assert self.id.status == Status.SUSPENDED

    def test_revoke(self) -> None:
        self.id.revoke()
        assert self.id.status == Status.REVOKED

        self.id.suspend()
        self.id.revoke()
        assert self.id.status == Status.REVOKED

    def test_activate(self) -> None:
        assert self.id.status == Status.ACTIVE

        self.id.suspend()
        self.id.activate()
        assert self.id.status == Status.ACTIVE

    def test_get_first_name(self) -> None:
        assert self.id.first_name == new_person_dict["first_name"]

    def test_set_first_name(self) -> None:
        self.id.first_name = "Alicia"
        assert self.id.first_name == "Alicia"

    def test_get_surname(self) -> None:
        assert self.id.surname == new_person_dict["surname"]

    def test_set_surname(self) -> None:
        self.id.surname = "Johnson"
        assert self.id.surname == "Johnson"

    def test_get_date_of_birth(self) -> None:
        assert self.id.date_of_birth == new_person_dict["date_of_birth"]

    def test_date_of_birth_is_read_only(self) -> None:
        with pytest.raises(AttributeError):
            setattr(self.id, "date_of_birth", "2010-01-01")

    def test_get_address(self) -> None:
        assert self.id.address == Address.from_string(new_person_dict["address"])

    def test_set_address(self) -> None:
        new_address = "789 New Street, Birmingham, B1 1BA"
        setattr(self.id, "address", new_address)
        assert self.id.address == Address.from_string(new_address)

    def test_get_national_insurance(self) -> None:
        assert self.id.national_insurance == new_person_dict["national_insurance"]

    def test_national_insurance_is_read_only(self) -> None:
        with pytest.raises(AttributeError):
            setattr(self.id, "national_insurance", "EF123456A")
