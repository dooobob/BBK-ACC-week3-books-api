from datetime import UTC, datetime, timedelta

import pytest

from rules import checkingout_is_open


@pytest.mark.parametrize("seconds, expected", [(-1, True), (0, False), (1, False)])
def test_checkingout_boundary(seconds, expected):
    closes_at = datetime(2026, 11, 1, 12, tzinfo=UTC)
    now = closes_at + timedelta(seconds=seconds)
    assert checkingout_is_open(closes_at, now) is expected
