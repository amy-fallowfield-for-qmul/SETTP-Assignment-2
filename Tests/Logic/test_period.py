import pytest
from dataclasses import FrozenInstanceError
from datetime import datetime
from Logic.period import Period


class TestPeriodIsInPeriod:
    """Tests for Period.is_in_period"""

    def test_timestamp_before_start_date_returns_false(self):
        period = Period(start_date="2026-01-02", end_date="2026-01-04")
        assert period.is_in_period(datetime(2026, 1, 1, 12, 0, 0)) is False

    def test_timestamp_after_end_date_returns_false(self):
        period = Period(start_date="2026-01-02", end_date="2026-01-04")
        assert period.is_in_period(datetime(2026, 1, 5, 0, 0, 0)) is False

    def test_timestamp_on_start_date_returns_true(self):
        period = Period(start_date="2026-01-02", end_date="2026-01-04")
        assert period.is_in_period(datetime(2026, 1, 2, 0, 0, 0)) is True

    def test_timestamp_on_end_date_returns_true(self):
        period = Period(start_date="2026-01-02", end_date="2026-01-04")
        assert period.is_in_period(datetime(2026, 1, 4, 0, 0, 0)) is True

    def test_timestamp_inside_period_returns_true(self):
        period = Period(start_date="2026-01-02", end_date="2026-01-04")
        assert period.is_in_period(datetime(2026, 1, 3, 12, 0, 0)) is True

    def test_single_day_period_returns_true(self):
        period = Period(start_date="2026-01-02", end_date="2026-01-02")
        assert period.is_in_period(datetime(2026, 1, 2, 0, 0, 0)) is True

class TestPeriodStr:
    """Tests for Period.__str__"""

    def test_str(self):
        period = Period(start_date="2026-01-01", end_date="2026-01-02")
        assert str(period) == "2026-01-01 to 2026-01-02"
