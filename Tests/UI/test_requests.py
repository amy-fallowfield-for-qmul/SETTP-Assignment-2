import pytest
from UI.requests import Requests
from Data.digitalID import DigitalID, Status
from Data.digitalIDRepository import DigitalIDRepository
from Logic.service import DigitalIDService

@pytest.fixture
def requests() -> Requests:
    DigitalID._next_id = 1
    DigitalIDRepository._instance = None
    DigitalIDService._instance = None
    Requests._instance = None
    req = Requests()
    req.DIGITAL_ID_SERVICE.create_id({"firstName": "John", "surname": "Smith", "dateOfBirth": "2000-01-01", "justification": "New registration"})
    return req

class TestRequestsCreateID:
    """Tests for creating a Digital ID via the UI"""

    def test_create_id(self, requests: Requests, monkeypatch, capsys) -> None:
        inputs = iter(["Bob", "Jones", "2005-01-01", "New registration"])
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        requests.create_id()
        captured = capsys.readouterr()
        assert "Digital ID created successfully" in captured.out

    def test_create_id_invalid_data(self, requests: Requests, monkeypatch, capsys) -> None:
        inputs = iter(["John123", "Smith", "2000-01-01", "New registration"])
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        requests.create_id()
        captured = capsys.readouterr()
        assert "Error creating Digital ID" in captured.out

class TestRequestsViewAllIDs:
    """Tests for viewing all Digital IDs via the UI"""

    def test_view_all(self, requests: Requests, monkeypatch, capsys) -> None:
        monkeypatch.setattr("builtins.input", lambda _="": "1")
        requests.view_all("digitalID")
        captured = capsys.readouterr()
        assert "John" in captured.out

    def test_filter(self, requests: Requests, monkeypatch, capsys) -> None:
        requests.DIGITAL_ID_SERVICE.create_id({"firstName": "Bob", "surname": "Jones", "dateOfBirth": "2005-01-01", "justification": "New registration"})
        inputs = iter(["2", "n", "n", "n", "y", "Smith", "n"])
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        requests.view_all("digitalID")
        captured = capsys.readouterr()
        assert "John" in captured.out

    def test_multiple_filters(self, requests: Requests, monkeypatch, capsys) -> None:
        requests.DIGITAL_ID_SERVICE.create_id({"firstName": "Bob", "surname": "Jones", "dateOfBirth": "2005-01-01", "justification": "New registration"})
        requests.DIGITAL_ID_SERVICE.create_id({"firstName": "Bob", "surname": "Johnson", "dateOfBirth": "2015-01-01", "justification": "New registration"})
        inputs = iter(["2", "n", "n", "y", "Bob", "y", "Jones", "n"])
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        requests.view_all("digitalID")
        captured = capsys.readouterr()
        assert "Bob" in captured.out
        assert "Jones" in captured.out
        assert "Johnson" not in captured.out

    def test_filter_returns_all_when_no_params(self, requests: Requests, monkeypatch, capsys) -> None:
        requests.DIGITAL_ID_SERVICE.create_id({"firstName": "Bob", "surname": "Jones", "dateOfBirth": "2005-01-01", "justification": "New registration"})
        inputs = iter(["2", "n", "n", "n", "n", "n"])
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        requests.view_all("digitalID")
        captured = capsys.readouterr()
        assert "John" in captured.out
        assert "Bob" in captured.out

    def test_view_all_empty(self, monkeypatch, capsys) -> None:
        DigitalID._next_id = 1
        DigitalIDRepository._instance = None
        DigitalIDService._instance = None
        Requests._instance = None
        req = Requests()
        monkeypatch.setattr("builtins.input", lambda _="": "1")
        req.view_all("digitalID")
        captured = capsys.readouterr()
        assert "No Digital IDs found" in captured.out

    def test_view_all_invalid_choice(self, requests: Requests, monkeypatch, capsys) -> None:
        monkeypatch.setattr("builtins.input", lambda _="": "q")
        requests.view_all("digitalID")
        captured = capsys.readouterr()
        assert "Invalid choice" in captured.out

class TestRequestsQueryID:
    """Tests for querying a Digital ID attribute via the UI"""

    def test_query_id(self, requests: Requests, monkeypatch, capsys) -> None:
        inputs = iter(["1", "1", "Status check"])
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        requests.query_id()
        captured = capsys.readouterr()
        assert "status" in captured.out
        assert "active" in captured.out

    def test_query_invalid_id(self, requests: Requests, monkeypatch, capsys) -> None:
        monkeypatch.setattr("builtins.input", lambda _="": "99")
        requests.query_id()
        captured = capsys.readouterr()
        assert "Invalid ID" in captured.out

    def test_query_invalid_attribute(self, requests: Requests, monkeypatch, capsys) -> None:
        inputs = iter(["1", "x"])
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        requests.query_id()
        captured = capsys.readouterr()
        assert "Invalid input" in captured.out

class TestRequestsUpdateID:
    """Tests for updating a Digital ID attribute via the UI"""

    def test_update_id(self, requests: Requests, monkeypatch, capsys) -> None:
        inputs = iter(["1", "1", "suspended", "Status change requested"])
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        requests.update_id()
        captured = capsys.readouterr()
        assert "active -> suspended" in captured.out

    def test_update_empty_value(self, requests: Requests, monkeypatch, capsys) -> None:
        inputs = iter(["1", "1", ""])
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        requests.update_id()
        captured = capsys.readouterr()
        assert "No value entered" in captured.out

    def test_update_invalid_id(self, requests: Requests, monkeypatch, capsys) -> None:
        monkeypatch.setattr("builtins.input", lambda _="": "99")
        requests.update_id()
        captured = capsys.readouterr()
        assert "Invalid ID" in captured.out

    def test_update_invalid_attribute(self, requests: Requests, monkeypatch, capsys) -> None:
        inputs = iter(["1", "x"])
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        requests.update_id()
        captured = capsys.readouterr()
        assert "Invalid input" in captured.out

class TestRequestsHelpers:
    """Tests for _get_id_subject and _get_attribute_subject"""

    def test_get_id_subject(self, requests: Requests, monkeypatch) -> None:
        monkeypatch.setattr("builtins.input", lambda _="": "1")
        id_subject = requests._get_id_subject()
        assert id_subject.first_name == "John"

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
        assert result == "firstName"

    def test_get_attribute_subject_invalid(self, requests: Requests, monkeypatch) -> None:
        monkeypatch.setattr("builtins.input", lambda _="": "99")
        with pytest.raises(ValueError, match="Invalid input"):
            requests._get_attribute_subject("query")
