import pytest
from unittest.mock import patch, MagicMock
import main

class TestMainEntryPointUserSelection:
    """Tests for the main.py entry point user selection functionality"""

    def test_select_central_authority(self, monkeypatch) -> None:
        inputs = iter(["1"])
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        
        with patch('main.CentralAuthorityMain') as mock_central:
            mock_instance = MagicMock()
            mock_central.return_value = mock_instance
            
            try:
                main.select_user_type()
            except StopIteration:
                pass
            
            mock_central.assert_called_once()

    def test_select_hmrc(self, monkeypatch) -> None:
        
        inputs = iter(["2"])
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        
        with patch('main.HMRC') as mock_other:
            mock_instance = MagicMock()
            mock_other.return_value = mock_instance
            
            try:
                main.select_user_type()
            except StopIteration:
                pass
            
            mock_other.assert_called_once()

    def test_invalid_non_numeric_input_handling(self, monkeypatch, capsys) -> None:
        inputs = iter(["abc", "3"])
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        
        with pytest.raises(SystemExit):
            main.select_user_type()
        
        captured = capsys.readouterr()
        assert "Invalid input" in captured.out

    def test_welcome_message(self, monkeypatch, capsys) -> None:
        monkeypatch.setattr("builtins.input", lambda _="": "3")
        
        with pytest.raises(SystemExit):
            main.select_user_type()
        
        captured = capsys.readouterr()
        assert "Welcome to the Digital ID System" in captured.out
        assert "=" * 100 in captured.out

    def test_menu_options_displayed_correctly(self, monkeypatch, capsys) -> None:
        monkeypatch.setattr("builtins.input", lambda _="": "3")
        
        with pytest.raises(SystemExit):
            main.select_user_type()
        
        captured = capsys.readouterr()
        assert "Please select your organisation type:" in captured.out
        assert "1. Central Authority" in captured.out
        assert "2. HMRC" in captured.out
        assert "3. Exit" in captured.out

    def test_retry_on_invalid_choice(self, monkeypatch, capsys) -> None:
        inputs = iter(["abc", "xyz", "3"])
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        
        with pytest.raises(SystemExit):
            main.select_user_type()
        
        captured = capsys.readouterr()
        
        assert captured.out.count("Invalid input") >= 2
        assert "Please select your organisation type:" in captured.out
