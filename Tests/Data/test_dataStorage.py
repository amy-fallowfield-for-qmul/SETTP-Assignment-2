import pytest
import os
from Data.dataStorage import save_to_csv, load_from_csv

class TestDataStorageSaveToCSV:
    """Tests for saving data to CSV"""

    TEST_CSV_PATH = "test_data_storage.csv"

    def teardown_method(self) -> None:
        if os.path.exists(self.TEST_CSV_PATH):
            os.remove(self.TEST_CSV_PATH)

    def test_save_to_csv(self) -> None:
        headers = ["name", "age"]
        rows = [["John", "30"], ["Bob", "25"]]
        save_to_csv(self.TEST_CSV_PATH, headers, rows)
        assert os.path.exists(self.TEST_CSV_PATH)

        with open(self.TEST_CSV_PATH, "r") as file:
            lines = file.readlines()

        assert lines[0].strip() == "name,age"
        assert lines[1].strip() == "John,30"
        assert lines[2].strip() == "Bob,25"

    def test_save_empty_rows(self) -> None:
        headers = ["name", "age"]
        save_to_csv(self.TEST_CSV_PATH, headers, [])

        with open(self.TEST_CSV_PATH, "r") as file:
            lines = file.readlines()

        assert len(lines) == 1
        assert lines[0].strip() == "name,age"

class TestDataStorageLoadFromCSV:
    """Tests for loading data from CSV"""

    TEST_CSV_PATH = "test_data_storage.csv"

    def teardown_method(self) -> None:
        if os.path.exists(self.TEST_CSV_PATH):
            os.remove(self.TEST_CSV_PATH)

    def test_load_from_csv(self) -> None:
        headers = ["name", "age"]
        rows = [["John", "30"], ["Bob", "25"]]
        save_to_csv(self.TEST_CSV_PATH, headers, rows)

        loaded = load_from_csv(self.TEST_CSV_PATH)
        assert len(loaded) == 2
        assert "name" not in loaded
        assert loaded[0] == ["John", "30"]
        assert loaded[1] == ["Bob", "25"]

    def test_load_from_csv_skips_headers(self) -> None:
        headers = ["name", "age"]
        rows = [["John", "30"]]
        save_to_csv(self.TEST_CSV_PATH, headers, rows)

        loaded = load_from_csv(self.TEST_CSV_PATH)
        assert "name" not in loaded
        assert loaded[0] == ["John", "30"]

    def test_load_from_csv_no_file(self) -> None:
        with pytest.raises(FileNotFoundError):
            load_from_csv("nonexistent.csv")

    def test_load_empty_csv(self) -> None:
        save_to_csv(self.TEST_CSV_PATH, ["name"], [])
        loaded = load_from_csv(self.TEST_CSV_PATH)
        assert loaded == []
