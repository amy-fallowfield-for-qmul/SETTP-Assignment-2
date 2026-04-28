import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

from UI.Controllers.employer import Employer

class TestEmployer:
    """Tests for Employer class properties and functionality"""

    def test_organisation_name(self) -> None:
        employer_class = Employer.__new__(Employer)
        assert employer_class.organisation_name == "Employer"

    def test_allowed_attributes(self) -> None:
        employer_class = Employer.__new__(Employer)
        expected_attributes = ["status", "first_name", "surname", "date_of_birth", "address", "national_insurance"]
        assert employer_class.allowed_attributes == expected_attributes