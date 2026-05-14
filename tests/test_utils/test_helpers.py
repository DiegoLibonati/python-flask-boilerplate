from typing import Any

import pytest

from src.utils.helpers import is_positive_integer


@pytest.mark.unit
class TestIsPositiveInteger:
    @pytest.mark.parametrize(
        "value,expected",
        [
            (1, True),
            (100, True),
            (0, False),
            (-1, False),
            (-100, False),
            (True, False),
            (False, False),
            ("5", True),
            ("100", True),
            ("0", False),
            ("abc", False),
            ("", False),
            (None, False),
            (1.5, False),
            ([], False),
            ({}, False),
        ],
    )
    def test_is_positive_integer(self, value: Any, expected: bool) -> None:
        assert is_positive_integer(value) is expected
