import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

from UI.Controllers.hmrc import HMRC

class TestHMRC:
    """Tests for HMRC class properties and functionality"""

    def test_organisation_name(self) -> None:
        hmrc_class = HMRC.__new__(HMRC)
        assert hmrc_class.organisation_name == "HMRC"

    def test_allowed_attributes(self) -> None:
        hmrc_class = HMRC.__new__(HMRC)
        expected_attributes = ["status", "address", "national_insurance"]
        assert hmrc_class.allowed_attributes == expected_attributes
