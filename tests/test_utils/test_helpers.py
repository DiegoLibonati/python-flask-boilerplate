import pytest

from src.utils.helpers import is_positive_integer


class TestIsPositiveInteger:
    @pytest.mark.unit
    def test_returns_true_for_positive_integer(self) -> None:
        result: bool = is_positive_integer(1)
        assert result is True

    @pytest.mark.unit
    def test_returns_true_for_large_positive_integer(self) -> None:
        result: bool = is_positive_integer(1000000)
        assert result is True

    @pytest.mark.unit
    def test_returns_false_for_zero(self) -> None:
        result: bool = is_positive_integer(0)
        assert result is False

    @pytest.mark.unit
    def test_returns_false_for_negative_integer(self) -> None:
        result: bool = is_positive_integer(-1)
        assert result is False

    @pytest.mark.unit
    def test_returns_false_for_bool_true(self) -> None:
        result: bool = is_positive_integer(True)
        assert result is False

    @pytest.mark.unit
    def test_returns_false_for_bool_false(self) -> None:
        result: bool = is_positive_integer(False)
        assert result is False

    @pytest.mark.unit
    def test_returns_true_for_digit_string(self) -> None:
        result: bool = is_positive_integer("5")
        assert result is True

    @pytest.mark.unit
    def test_returns_false_for_zero_string(self) -> None:
        result: bool = is_positive_integer("0")
        assert result is False

    @pytest.mark.unit
    def test_returns_false_for_non_digit_string(self) -> None:
        result: bool = is_positive_integer("abc")
        assert result is False

    @pytest.mark.unit
    def test_returns_false_for_empty_string(self) -> None:
        result: bool = is_positive_integer("")
        assert result is False

    @pytest.mark.unit
    def test_returns_false_for_float(self) -> None:
        result: bool = is_positive_integer(1.5)
        assert result is False

    @pytest.mark.unit
    def test_returns_false_for_none(self) -> None:
        result: bool = is_positive_integer(None)
        assert result is False

    @pytest.mark.unit
    def test_returns_false_for_list(self) -> None:
        result: bool = is_positive_integer([1])
        assert result is False

    @pytest.mark.unit
    def test_returns_false_for_negative_string(self) -> None:
        result: bool = is_positive_integer("-1")
        assert result is False
