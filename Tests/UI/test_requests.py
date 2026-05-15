import pytest
from UI.requests import Requests
from Data.DigitalID.digitalID import DigitalID
from Data.DigitalID.digitalIDRepository import DigitalIDRepository
from Logic.service import DigitalIDService
from Logic.verifier import Verifier
from Data.Attributes.attributeRegistry import AttributeRegistry
from Tests.shared_test_data import justification_person_dict, CENTRAL_AUTHORITY_ORG, BANK_ORG, EMPLOYER_ORG

@pytest.fixture
def requests() -> Requests:
    DigitalID._next_id = 1
    DigitalIDRepository.clear_instance()
    DigitalIDService.clear_instance()
    Requests.clear_instance()
    Verifier.clear_instance()
    return Requests()

class TestRequestsCreateID:
    """Tests for creating a Digital ID via the UI"""

    def test_create_id(self, requests: Requests, monkeypatch, capsys) -> None:
        inputs = iter(justification_person_dict.values())
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        requests.create_id(CENTRAL_AUTHORITY_ORG)
        captured = capsys.readouterr()
        assert "Digital ID created successfully" in captured.out

    def test_create_id_invalid_data(self, requests: Requests, monkeypatch, capsys) -> None:
        id = justification_person_dict.copy()
        id["first_name"] = "John123"
        inputs = iter(id.values())
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        requests.create_id(CENTRAL_AUTHORITY_ORG)
        captured = capsys.readouterr()
        assert "Error creating Digital ID" in captured.out

class TestRequestsViewAllIDs:
    """Tests for viewing all Digital IDs via the UI"""

    def test_view_all(self, requests: Requests, monkeypatch, capsys) -> None:
        id = requests.DIGITAL_ID_SERVICE.create_id(justification_person_dict, CENTRAL_AUTHORITY_ORG)
        monkeypatch.setattr("builtins.input", lambda _="": "1")
        requests.view_all_ids()
        captured = capsys.readouterr()
        assert id.first_name in captured.out

    def test_filter(self, requests: Requests, monkeypatch, capsys) -> None:
        id1 = requests.DIGITAL_ID_SERVICE.create_id(justification_person_dict, CENTRAL_AUTHORITY_ORG)
        id2_dict = justification_person_dict.copy()
        id2_dict["surname"] = "Johnson"
        id2 = requests.DIGITAL_ID_SERVICE.create_id(id2_dict, CENTRAL_AUTHORITY_ORG)
        num_attrs = len(justification_person_dict) - 3
        inputs = iter(["2", "n", "n", "n", "y", "Johnson"] + ["n"] * num_attrs)
        
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        requests.view_all_ids()
        captured = capsys.readouterr()
        assert id1.surname not in captured.out
        assert "Johnson" in captured.out

    def test_multiple_filters(self, requests: Requests, monkeypatch, capsys) -> None:
        requests.DIGITAL_ID_SERVICE.create_id(justification_person_dict, CENTRAL_AUTHORITY_ORG)
        id2 = justification_person_dict.copy()
        id2_dict = justification_person_dict.copy()
        id2_dict["surname"] = "Johnson"
        requests.DIGITAL_ID_SERVICE.create_id(id2_dict, CENTRAL_AUTHORITY_ORG)
        extra_ns = ["n"] * (len(justification_person_dict) - 3)
        inputs = iter(["2", "n", "n", "y", id2["first_name"], "y", "Johnson"] + extra_ns)
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        requests.view_all_ids()
        captured = capsys.readouterr()
        assert justification_person_dict["surname"] not in captured.out
        assert id2_dict["surname"] in captured.out

    def test_filter_returns_all_when_no_params(self, requests: Requests, monkeypatch, capsys) -> None:
        requests.DIGITAL_ID_SERVICE.create_id(justification_person_dict, CENTRAL_AUTHORITY_ORG)
        id2 = justification_person_dict.copy()
        id2["first_name"] = "Bob"
        requests.DIGITAL_ID_SERVICE.create_id(id2, CENTRAL_AUTHORITY_ORG)
        extra_ns = ["n"] * (len(justification_person_dict) + 1)
        inputs = iter(["2"] + extra_ns)
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        requests.view_all_ids()
        captured = capsys.readouterr()
        assert justification_person_dict["first_name"] in captured.out
        assert "Bob" in captured.out

    def test_view_all_empty(self, monkeypatch, capsys) -> None:
        DigitalID._next_id = 1
        DigitalIDRepository.clear_instance()
        DigitalIDService.clear_instance()
        Requests.clear_instance()
        Verifier.clear_instance()
        req = Requests()
        monkeypatch.setattr("builtins.input", lambda _="": "1")
        req.view_all_ids()
        captured = capsys.readouterr()
        assert "No Digital IDs found" in captured.out

    def test_view_all_invalid_choice(self, requests: Requests, monkeypatch, capsys) -> None:
        monkeypatch.setattr("builtins.input", lambda _="": "q")
        requests.view_all_ids()
        captured = capsys.readouterr()
        assert "Invalid choice" in captured.out

class TestRequestsQueryID:
    """Tests for querying a Digital ID attribute via the UI"""

    central_authority_attributes = AttributeRegistry().get_queryable_attributes()

    def setup_method(self) -> None:
        DigitalID._next_id = 1
        DigitalIDRepository.clear_instance()
        DigitalIDService.clear_instance()
        Requests.clear_instance()
        Verifier.clear_instance()
        self.requests = Requests()
        self.requests.DIGITAL_ID_SERVICE.create_id(justification_person_dict, CENTRAL_AUTHORITY_ORG)

    def test_query_id(self, monkeypatch, capsys) -> None:
        inputs = iter(["1", "1", "Status check"])
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        self.requests.query_id(CENTRAL_AUTHORITY_ORG)
        captured = capsys.readouterr()
        assert "status" in captured.out
        assert "active" in captured.out

    def test_query_invalid_id(self, monkeypatch, capsys) -> None:
        monkeypatch.setattr("builtins.input", lambda _="": "99")
        self.requests.query_id(CENTRAL_AUTHORITY_ORG)
        captured = capsys.readouterr()
        assert "Invalid ID" in captured.out

    def test_query_invalid_attribute(self, monkeypatch, capsys) -> None:
        inputs = iter(["1", "x"])
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        self.requests.query_id(CENTRAL_AUTHORITY_ORG)
        captured = capsys.readouterr()
        assert "Invalid input" in captured.out

class TestRequestsVerifyIdentity:
    """Tests for verifying a Digital ID's identity via the UI"""

    def setup_method(self) -> None:
        DigitalID._next_id = 1
        DigitalIDRepository.clear_instance()
        DigitalIDService.clear_instance()
        Requests.clear_instance()
        Verifier.clear_instance()
        self.requests = Requests()
        self.requests.DIGITAL_ID_SERVICE.create_id(justification_person_dict, CENTRAL_AUTHORITY_ORG)

    def test_verify_identity_match(self, monkeypatch, capsys) -> None:
        inputs = iter(["1", "John", "Smith", "2000-01-01", "Account opening"])
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        self.requests.verify_identity(BANK_ORG)
        captured = capsys.readouterr()
        assert "Identity verified for Digital ID 1" in captured.out

    def test_verify_identity_mismatch(self, monkeypatch, capsys) -> None:
        inputs = iter(["1", "Alice", "Smith", "2000-01-01", "Account opening"])
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        self.requests.verify_identity(BANK_ORG)
        captured = capsys.readouterr()
        assert "Identity NOT verified for Digital ID 1" in captured.out

    def test_verify_identity_rejected(self, monkeypatch, capsys) -> None:
        inputs = iter(["99", "John", "Smith", "2000-01-01", "Account opening"])
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        self.requests.verify_identity(BANK_ORG)
        captured = capsys.readouterr()
        assert "Request rejected" in captured.out

class TestRequestsVerifyMinimumAge:
    """Tests for verifying a Digital ID's minimum age via the UI"""

    def setup_method(self) -> None:
        DigitalID._next_id = 1
        DigitalIDRepository.clear_instance()
        DigitalIDService.clear_instance()
        Requests.clear_instance()
        Verifier.clear_instance()
        self.requests = Requests()
        self.requests.DIGITAL_ID_SERVICE.create_id(justification_person_dict, CENTRAL_AUTHORITY_ORG)

    def test_verify_minimum_age_meets(self, monkeypatch, capsys) -> None:
        inputs = iter(["1", "18", "ISA eligibility"])
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        self.requests.verify_minimum_age(BANK_ORG)
        captured = capsys.readouterr()
        assert "meets the minimum age" in captured.out

    def test_verify_minimum_age_does_not_meet(self, monkeypatch, capsys) -> None:
        inputs = iter(["1", "99", "Pension eligibility"])
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        self.requests.verify_minimum_age(BANK_ORG)
        captured = capsys.readouterr()
        assert "does NOT meet the minimum age" in captured.out

    def test_verify_minimum_age_rejected(self, monkeypatch, capsys) -> None:
        inputs = iter(["99", "18", "ISA eligibility"])
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        self.requests.verify_minimum_age(BANK_ORG)
        captured = capsys.readouterr()
        assert "Request rejected" in captured.out

class TestRequestsVerifyAttribute:
    """Tests for verifying a single Digital ID attribute via the UI"""

    def setup_method(self) -> None:
        DigitalID._next_id = 1
        DigitalIDRepository.clear_instance()
        DigitalIDService.clear_instance()
        Requests.clear_instance()
        Verifier.clear_instance()
        self.requests = Requests()
        self.requests.DIGITAL_ID_SERVICE.create_id(justification_person_dict, CENTRAL_AUTHORITY_ORG)

    def test_verify_attribute_match(self, monkeypatch, capsys) -> None:
        inputs = iter(["1", "1", "AB123456C", "New hire"])
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        self.requests.verify_attribute(EMPLOYER_ORG)
        captured = capsys.readouterr()
        assert "national_insurance matches for Digital ID 1" in captured.out

    def test_verify_attribute_mismatch(self, monkeypatch, capsys) -> None:
        inputs = iter(["1", "1", "BC123456C", "New hire"])
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        self.requests.verify_attribute(EMPLOYER_ORG)
        captured = capsys.readouterr()
        assert "national_insurance does NOT match for Digital ID 1" in captured.out

    def test_verify_attribute_rejected(self, monkeypatch, capsys) -> None:
        inputs = iter(["99", "1", "AB123456C", "New hire"])
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        self.requests.verify_attribute(EMPLOYER_ORG)
        captured = capsys.readouterr()
        assert "Request rejected" in captured.out

class TestRequestsUpdateID:
    """Tests for updating a Digital ID attribute via the UI"""

    def setup_method(self) -> None:
        DigitalID._next_id = 1
        DigitalIDRepository.clear_instance()
        DigitalIDService.clear_instance()
        Requests.clear_instance()
        Verifier.clear_instance()
        self.requests = Requests()
        self.requests.DIGITAL_ID_SERVICE.create_id(justification_person_dict, CENTRAL_AUTHORITY_ORG)

    def test_update_id(self, monkeypatch, capsys) -> None:
        inputs = iter(["1", "1", "suspended", "Status change requested"])
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        self.requests.update_id(CENTRAL_AUTHORITY_ORG)
        captured = capsys.readouterr()
        assert "active -> suspended" in captured.out

    def test_update_empty_value(self, monkeypatch, capsys) -> None:
        inputs = iter(["1", "1", ""])
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        self.requests.update_id(CENTRAL_AUTHORITY_ORG)
        captured = capsys.readouterr()
        assert "No value entered" in captured.out

    def test_update_invalid_id(self, monkeypatch, capsys) -> None:
        monkeypatch.setattr("builtins.input", lambda _="": "99")
        self.requests.update_id(CENTRAL_AUTHORITY_ORG)
        captured = capsys.readouterr()
        assert "Invalid ID" in captured.out

    def test_update_invalid_attribute(self, monkeypatch, capsys) -> None:
        inputs = iter(["1", "x"])
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        self.requests.update_id(CENTRAL_AUTHORITY_ORG)
        captured = capsys.readouterr()
        assert "Invalid input" in captured.out

class TestRequestsHelpers:
    """Tests for _get_id_subject and _get_attribute_subject"""

    def setup_method(self) -> None:
        DigitalID._next_id = 1
        DigitalIDRepository.clear_instance()
        DigitalIDService.clear_instance()
        Requests.clear_instance()
        Verifier.clear_instance()
        self.requests = Requests()
        self.requests.DIGITAL_ID_SERVICE.create_id(justification_person_dict, CENTRAL_AUTHORITY_ORG)

    def test_get_id_subject(self, monkeypatch) -> None:
        monkeypatch.setattr("builtins.input", lambda _="": "1")
        id_subject = self.requests._get_id_subject()
        assert id_subject.first_name == justification_person_dict["first_name"]

    def test_get_id_subject_invalid(self, requests: Requests, monkeypatch) -> None:
        monkeypatch.setattr("builtins.input", lambda _="": "abc")
        with pytest.raises(ValueError, match="Invalid ID"):
            requests._get_id_subject()

    def test_get_attribute_subject_query(self, requests: Requests, monkeypatch) -> None:
        monkeypatch.setattr("builtins.input", lambda _="": "1")
        result = requests._get_attribute_subject("query")
        assert result == "status"

    def test_get_attribute_subject_update(self, requests: Requests, monkeypatch) -> None:
        monkeypatch.setattr("builtins.input", lambda _="": "2")
        result = requests._get_attribute_subject("update")
        assert result == "first_name"

    def test_get_attribute_subject_invalid(self, requests: Requests, monkeypatch) -> None:
        monkeypatch.setattr("builtins.input", lambda _="": "99")
        with pytest.raises(ValueError, match="Invalid input"):
            requests._get_attribute_subject("query")
