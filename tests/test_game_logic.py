"""Unit tests for the refactored game logic in logic_utils.py.

check_guess now returns a plain outcome string, so the original starter
tests pass unchanged. Added tests cover scoring behavior and edge cases.
"""

from logic_utils import (
    check_guess,
    parse_guess,
    update_score,
    get_range_for_difficulty,
    hint_message,
)


# --- Required: core hint outcomes -----------------------------------------

def test_winning_guess():
    # secret 50, guess 50 -> Win
    assert check_guess(50, 50) == "Win"


def test_guess_too_high():
    # secret 50, guess 60 -> Too High
    assert check_guess(60, 50) == "Too High"


def test_guess_too_low():
    # secret 50, guess 40 -> Too Low
    assert check_guess(40, 50) == "Too Low"


# --- Required: score behavior ---------------------------------------------

def test_first_try_win_scores_full_100():
    # Bug 4 fix: winning on attempt 1 awards the full 100 points.
    assert update_score(0, "Win", attempt_number=1) == 100


def test_later_win_scores_less():
    # attempt 3 -> 100 - 10*(3-1) = 80
    assert update_score(0, "Win", attempt_number=3) == 80


def test_win_score_never_below_10():
    # Even a very late win floors at +10 points.
    assert update_score(0, "Win", attempt_number=50) == 10


def test_wrong_guess_always_subtracts():
    # Bug 3 fix: a wrong guess never gains points, regardless of attempt parity.
    assert update_score(100, "Too High", attempt_number=2) == 95
    assert update_score(100, "Too High", attempt_number=3) == 95
    assert update_score(100, "Too Low", attempt_number=4) == 95


# --- Edge cases -----------------------------------------------------------

def test_negative_numbers():
    # Negative guesses compare numerically, not lexicographically (Bug 2 fix).
    assert check_guess(-10, -5) == "Too Low"
    assert check_guess(-1, -5) == "Too High"
    assert check_guess(-5, -5) == "Win"


def test_decimal_input_is_truncated():
    # parse_guess accepts "42.9" and truncates to 42.
    ok, value, err = parse_guess("42.9")
    assert ok is True
    assert value == 42
    assert err is None


def test_large_values():
    # Large numbers still compare numerically (a lexicographic bug would fail this).
    assert check_guess(1000000, 999999) == "Too High"
    assert check_guess(999999, 1000000) == "Too Low"


def test_invalid_input_rejected():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None
    assert err == "That is not a number."


# --- Bonus: regression guards for other fixed bugs ------------------------

def test_hard_is_wider_than_normal():
    # Bug 10 fix: Hard's range is larger than Normal's.
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > normal_high


def test_hint_direction_is_correct():
    # Bug 11 fix: "Too High" tells the player to go LOWER.
    assert "LOWER" in hint_message("Too High")
    assert "HIGHER" in hint_message("Too Low")
