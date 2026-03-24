import pytest
from Data.digitalID import DigitalID, Status

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

    def test_create_id_with_init(self) -> None:
        id = DigitalID("John", "Smith", "2000-01-01")
        assert id.id == 1
        assert id.status == Status.ACTIVE
        assert id.first_name == "John"
        assert id.surname == "Smith"
        assert id.date_of_birth == "2000-01-01"

    def test_create_id_from_csv(self) -> None:
        attributes = {"id": "1", "status": "active", "firstName": "John", "surname": "Smith", "dateOfBirth": "2000-01-01"}
        id = DigitalID.from_csv(attributes)
        assert id.id == 1
        assert id.status == Status.ACTIVE
        assert id.first_name == "John"
        assert id.surname == "Smith"
        assert id.date_of_birth == "2000-01-01"

    def test_auto_increment_id(self) -> None:
        id1 = DigitalID("John", "Smith", "2000-01-01")
        id2 = DigitalID("Bob", "Jones", "2005-01-01")
        assert id1.id == 1
        assert id2.id == 2

class TestDigitalIDProperties:
    """Tests for DigitalID getters and setters"""

    def setup_method(self) -> None:
        DigitalID._next_id = 1
        self.id = DigitalID("John", "Smith", "2000-01-01")

    def test_to_dict(self) -> None:
        assert self.id.to_dict() == {
            "id": 1,
            "status": "active",
            "firstName": "John",
            "surname": "Smith",
            "dateOfBirth": "2000-01-01"
        }

    def test_print(self, capsys) -> None:
        self.id.print()
        captured = capsys.readouterr()
        assert captured.out == "ID: 1, Name: John Smith, DOB: 2000-01-01, Status: active\n"

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
        assert self.id.first_name == "John"

    def test_set_first_name(self) -> None:
        self.id.first_name = "Alicia"
        assert self.id.first_name == "Alicia"

    def test_get_surname(self) -> None:
        assert self.id.surname == "Smith"

    def test_set_surname(self) -> None:
        self.id.surname = "Johnson"
        assert self.id.surname == "Johnson"

    def test_get_date_of_birth(self) -> None:
        assert self.id.date_of_birth == "2000-01-01"

    def test_date_of_birth_is_read_only(self) -> None:
        with pytest.raises(AttributeError):
            setattr(self.id, "date_of_birth", "2010-01-01")
