import pytest
from main import Program
from UI.requests import Requests
from Data.digitalID import DigitalID
from Data.digitalIDRepository import DigitalIDRepository
from Logic.service import DigitalIDService

@pytest.fixture
def program(monkeypatch) -> Program:
    DigitalID._next_id = 1
    DigitalIDRepository._instance = None
    DigitalIDService._instance = None
    Requests._instance = None
    Program._instance = None

    monkeypatch.setattr(Program, "start_program", lambda self: None)
    monkeypatch.setattr(Program, "main", lambda self: None)

    program = Program()
    return program

class TestProgramStartProgram:
    """Tests for start_program"""

    def test_start_program_prints_welcome(self, program: Program, monkeypatch, capsys) -> None:
        monkeypatch.undo()
        program.start_program()
        captured = capsys.readouterr()
        assert "Welcome to the Digital ID System" in captured.out

class TestProgramGenerateOptions:
    """Tests for generate_options menu routing"""

    def test_create_id_option(self, program: Program, monkeypatch, capsys) -> None:
        inputs = iter(["1", "John", "Smith", "2000-01-01", "New registration"])
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        program.generate_options()
        captured = capsys.readouterr()
        assert "Digital ID created successfully" in captured.out

    def test_view_all_option(self, program: Program, monkeypatch, capsys) -> None:
        program.REQUESTS.DIGITAL_ID_SERVICE.create_id({"firstName": "John", "surname": "Smith", "dateOfBirth": "2000-01-01", "justification": "Test data"})
        inputs = iter(["2", "1"])
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        program.generate_options()
        captured = capsys.readouterr()
        assert "John" in captured.out

    def test_filter_option(self, program: Program, monkeypatch, capsys) -> None:
        program.REQUESTS.DIGITAL_ID_SERVICE.create_id({"firstName": "John", "surname": "Smith", "dateOfBirth": "2000-01-01", "justification": "New registration"})
        program.REQUESTS.DIGITAL_ID_SERVICE.create_id({"firstName": "Bob", "surname": "Jones", "dateOfBirth": "2005-01-01", "justification": "New registration"})
        inputs = iter(["2", "2", "n", "n", "y", "Bob", "n", "n"])
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        program.generate_options()
        captured = capsys.readouterr()
        assert "Bob" in captured.out

    def test_query_id_option(self, program: Program, monkeypatch, capsys) -> None:
        program.REQUESTS.DIGITAL_ID_SERVICE.create_id({"firstName": "John", "surname": "Smith", "dateOfBirth": "2000-01-01", "justification": "New registration"})
        inputs = iter(["3", "1", "1", "Status check"])
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        program.generate_options()
        captured = capsys.readouterr()
        assert "status" in captured.out

    def test_update_id_option(self, program: Program, monkeypatch, capsys) -> None:
        program.REQUESTS.DIGITAL_ID_SERVICE.create_id({"firstName": "John", "surname": "Smith", "dateOfBirth": "2000-01-01", "justification": "New registration"})
        inputs = iter(["4", "1", "1", "suspended", "Status change requested"])
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        program.generate_options()
        captured = capsys.readouterr()
        assert "active -> suspended" in captured.out

    def test_exit_option(self, program: Program, monkeypatch) -> None:
        monkeypatch.setattr("builtins.input", lambda _="": "5")
        with pytest.raises(SystemExit):
            program.generate_options()

    def test_invalid_choice_non_numeric(self, program: Program, monkeypatch, capsys) -> None:
        monkeypatch.setattr("builtins.input", lambda _="": "abc")
        program.generate_options()
        captured = capsys.readouterr()
        assert "Invalid choice" in captured.out

    def test_invalid_choice_out_of_range(self, program: Program, monkeypatch, capsys) -> None:
        monkeypatch.setattr("builtins.input", lambda _="": "9")
        program.generate_options()
        captured = capsys.readouterr()
        assert "Invalid choice" in captured.out
