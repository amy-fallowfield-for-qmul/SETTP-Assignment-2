import pytest
from unittest.mock import MagicMock
import main

class TestMainEntryPointUserSelection:
    """Tests for the main.py entry point user selection functionality"""

    def _mock_controller(self, name: str) -> MagicMock:
        mock_cls = MagicMock()
        mock_cls.organisation_name = MagicMock(return_value=name)
        return mock_cls

    def test_select_central_authority(self, monkeypatch) -> None:
        inputs = iter(["1"])
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))

        mock_central = self._mock_controller("Central Authority")
        monkeypatch.setattr(main, "USER_OPTIONS", [mock_central, main.HMRC, main.Employer, main.Bank])

        try:
            main.select_user_type()
        except StopIteration:
            pass

        mock_central.assert_called_once()

    def test_select_hmrc(self, monkeypatch) -> None:
        inputs = iter(["2"])
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))

        mock_hmrc = self._mock_controller("HMRC")
        monkeypatch.setattr(main, "USER_OPTIONS", [main.CentralAuthorityMain, mock_hmrc, main.Employer, main.Bank])

        try:
            main.select_user_type()
        except StopIteration:
            pass

        mock_hmrc.assert_called_once()

    def test_select_employer(self, monkeypatch) -> None:
        inputs = iter(["3"])
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))

        mock_employer = self._mock_controller("Employer")
        monkeypatch.setattr(main, "USER_OPTIONS", [main.CentralAuthorityMain, main.HMRC, mock_employer, main.Bank])

        try:
            main.select_user_type()
        except StopIteration:
            pass

        mock_employer.assert_called_once()

    def test_select_bank(self, monkeypatch) -> None:
        inputs = iter(["4"])
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))

        mock_bank = self._mock_controller("Bank")
        monkeypatch.setattr(main, "USER_OPTIONS", [main.CentralAuthorityMain, main.HMRC, main.Employer, mock_bank])

        try:
            main.select_user_type()
        except StopIteration:
            pass

        mock_bank.assert_called_once()

    def test_invalid_non_numeric_input_handling(self, monkeypatch, capsys) -> None:
        inputs = iter(["abc", "5"])
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        
        with pytest.raises(SystemExit):
            main.select_user_type()
        
        captured = capsys.readouterr()
        assert "Invalid input" in captured.out

    def test_welcome_message(self, monkeypatch, capsys) -> None:
        monkeypatch.setattr("builtins.input", lambda _="": "5")
        
        with pytest.raises(SystemExit):
            main.select_user_type()
        
        captured = capsys.readouterr()
        assert "Welcome to the Digital ID System" in captured.out
        assert "=" * 100 in captured.out

    def test_menu_options_displayed_correctly(self, monkeypatch, capsys) -> None:
        monkeypatch.setattr("builtins.input", lambda _="": "5")
        
        with pytest.raises(SystemExit):
            main.select_user_type()
        
        captured = capsys.readouterr()
        assert "Please select your organisation type:" in captured.out
        assert "1. Central Authority" in captured.out
        assert "2. HMRC" in captured.out
        assert "3. Employer" in captured.out
        assert "4. Bank" in captured.out
        assert "5. Exit" in captured.out

    def test_retry_on_invalid_choice(self, monkeypatch, capsys) -> None:
        inputs = iter(["abc", "xyz", "5"])
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        
        with pytest.raises(SystemExit):
            main.select_user_type()
        
        captured = capsys.readouterr()
        
        assert captured.out.count("Invalid input") >= 2
        assert "Please select your organisation type:" in captured.out
