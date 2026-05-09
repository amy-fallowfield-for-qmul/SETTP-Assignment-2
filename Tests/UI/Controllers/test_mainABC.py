import pytest
from UI.Controllers.centralAuthorityMain import CentralAuthorityMain
from UI.Controllers.otherOrganisationsMain import OtherOrganisationMain
from UI.requests import Requests
from Data.DigitalID.digitalID import DigitalID
from Data.DigitalID.digitalIDRepository import DigitalIDRepository
from Logic.service import DigitalIDService
from UI.Controllers.mainABC import MainABC

class TestMainABCSharedFunctionality:
    """Tests for shared functionality in MainABC base class"""

    def test_start_program_initialization(self, monkeypatch, capsys) -> None:
        CentralAuthorityMain._instance = None
        monkeypatch.setattr(CentralAuthorityMain, "main", lambda self: None)
        central = CentralAuthorityMain()

        assert hasattr(central, 'REQUESTS')
        assert isinstance(central.REQUESTS, Requests)

    def test_singleton_pattern(self, monkeypatch) -> None:
        CentralAuthorityMain._instance = None
        monkeypatch.setattr(CentralAuthorityMain, "start_program", lambda self: None)
        monkeypatch.setattr(CentralAuthorityMain, "main", lambda self: None)
        instance1 = CentralAuthorityMain()
        instance2 = CentralAuthorityMain()
        assert instance1 is instance2

    def test_abc_prevents_direct_instantiation(self) -> None:
        with pytest.raises(TypeError):
            MainABC()

class TestCentralAuthoritySpecific:
    """Tests for Central Authority specific functionality"""
    
    @pytest.fixture
    def central_program(self, monkeypatch) -> CentralAuthorityMain:
        DigitalID._next_id = 1
        DigitalIDRepository._instance = None
        DigitalIDService._instance = None
        Requests._instance = None
        CentralAuthorityMain._instance = None
        
        monkeypatch.setattr(CentralAuthorityMain, "start_program", lambda self: None)
        monkeypatch.setattr(CentralAuthorityMain, "main", lambda self: None)
        
        return CentralAuthorityMain()

    def test_central_authority(self, central_program: CentralAuthorityMain, monkeypatch, capsys) -> None:

        monkeypatch.setattr("builtins.input", lambda _="": "99")
        central_program.generate_options()
        captured = capsys.readouterr()
        
        assert "1. Create a new Digital ID" in captured.out
        assert "2. Query Digital ID by ID" in captured.out  
        assert "3. Update a Digital ID" in captured.out
        assert "4. Query Digital ID suspended in given period" in captured.out
        assert "5. View all Digital ID data" in captured.out
        assert "6. View all log data" in captured.out
        assert "7. Exit" in captured.out

        assert "1. Query Digital ID by ID" not in captured.out
        assert "2. Exit" not in captured.out

    def test_central_authority_can_use_extra_commands(self, central_program: CentralAuthorityMain, monkeypatch, capsys) -> None:
        inputs = iter(["6", "1"])
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        central_program.generate_options()
        captured = capsys.readouterr()
        
        assert ("No logs found" in captured.out or "View all data" in captured.out)
        
class MockOrganisation(OtherOrganisationMain):
    @property
    def allowed_attributes(self):
        return ["firstName", "surname"]
    
    @property
    def organisation_name(self):
        return "Test Organisation"

class TestOtherOrganisationSpecific:
    """Tests for Other Organisation specific functionality"""
    
    @pytest.fixture  
    def other_program(self, monkeypatch) -> MockOrganisation:
        DigitalID._next_id = 1
        DigitalIDRepository._instance = None
        DigitalIDService._instance = None
        Requests._instance = None
        
        MockOrganisation._instance = None
        monkeypatch.setattr(MockOrganisation, "start_program", lambda self: None)
        monkeypatch.setattr(MockOrganisation, "main", lambda self: None)
        
        return MockOrganisation()

    def test_other_organisation(self, other_program: OtherOrganisationMain, monkeypatch, capsys) -> None:
        monkeypatch.setattr("builtins.input", lambda _="": "99")
        other_program.generate_options()
        captured = capsys.readouterr()
        
        assert "1. Query Digital ID by ID" in captured.out
        assert "2. Exit" in captured.out
        
        assert "1. Create a new Digital ID" not in captured.out
        assert "2. Query Digital ID by ID" not in captured.out  
        assert "3. Update a Digital ID" not in captured.out
        assert "4. Query Digital ID suspended in given period" not in captured.out
        assert "5. View all Digital ID data" not in captured.out
        assert "6. View all log data" not in captured.out
        assert "7. Exit" not in captured.out
