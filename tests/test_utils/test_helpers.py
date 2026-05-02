import pytest

from src.utils.helpers import is_positive_integer


@pytest.mark.unit
class TestIsPositiveInteger:
    def test_returns_true_for_positive_integer(self) -> None:
        assert is_positive_integer(1) is True

    def test_returns_true_for_large_positive_integer(self) -> None:
        assert is_positive_integer(1000) is True

    def test_returns_false_for_zero_integer(self) -> None:
        assert is_positive_integer(0) is False

    def test_returns_false_for_negative_integer(self) -> None:
        assert is_positive_integer(-1) is False

    def test_returns_true_for_positive_digit_string(self) -> None:
        assert is_positive_integer("5") is True

    def test_returns_true_for_large_positive_digit_string(self) -> None:
        assert is_positive_integer("999") is True

    def test_returns_false_for_zero_string(self) -> None:
        assert is_positive_integer("0") is False

    def test_returns_false_for_non_digit_string(self) -> None:
        assert is_positive_integer("abc") is False

    def test_returns_false_for_negative_number_string(self) -> None:
        assert is_positive_integer("-1") is False

    def test_returns_false_for_float(self) -> None:
        assert is_positive_integer(1.5) is False

    def test_returns_false_for_none(self) -> None:
        assert is_positive_integer(None) is False

    def test_returns_false_for_true_boolean(self) -> None:
        assert is_positive_integer(True) is False

    def test_returns_false_for_false_boolean(self) -> None:
        assert is_positive_integer(False) is False

    def test_returns_false_for_empty_string(self) -> None:
        assert is_positive_integer("") is False

    def test_returns_false_for_list(self) -> None:
        assert is_positive_integer([1]) is False

    def test_returns_false_for_dict(self) -> None:
        assert is_positive_integer({"value": 1}) is False
