"""Core game logic for Game Glitch Investigator.

Refactored out of app.py so it can be unit-tested without Streamlit.
check_guess returns ONLY the outcome string; hint_message maps an
outcome to its user-facing text (separates logic from presentation).
"""


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 200          # Bug 10 fix: Hard is now wider than Normal
    return 1, 100


def parse_guess(raw: str):
    """Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw == "":
        return False, None, "Enter a guess."
    try:
        # accept decimals like "42.0" by truncating to int
        value = int(float(raw)) if "." in raw else int(raw)
    except (ValueError, TypeError):
        return False, None, "That is not a number."
    return True, value, None


def check_guess(guess, secret):
    """Compare guess to secret. Returns the outcome string only:
    'Win', 'Too High', or 'Too Low'.

    Bug 1 & 2 fix: callers pass an int secret (no str casting), so the
    comparison is always numeric -- no lexicographic string compare.
    """
    # Collaboration note: the AI-generated original wrapped this in a
    # try/except TypeError that fell back to comparing str(guess) > secret.
    # We (developer + AI) found that fallback only existed to paper over the
    # str-cast bug in app.py, and that "9" > "50" compares as strings -> wrong
    # hint. Removing the str cast upstream let us delete the fallback entirely
    # and split the emoji text out into hint_message(), so this function is
    # pure logic and unit-testable.
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def hint_message(outcome: str):
    """Return the user-facing hint text for an outcome.

    Bug 11 fix: 'Too High' now advises the player to go LOWER, and
    vice versa.
    """
    return {
        "Win": "🎉 Correct!",
        "Too High": "📉 Go LOWER!",
        "Too Low": "📈 Go HIGHER!",
    }.get(outcome, "")


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and 1-based attempt_number.

    Bug 4 fix: a first-try win (attempt 1) scores the full 100.
    Bug 3 fix: any wrong guess always subtracts 5 -- never adds points.
    """
    # Collaboration note: the original added +5 on even-numbered "Too High"
    # attempts and used (attempt_number + 1) for wins. We traced both back to
    # app.py incrementing `attempts` *before* scoring, which threw the math
    # off by one. We fixed the counter in app.py (count only valid guesses)
    # and switched this to a clean 1-based formula, then locked it in with
    # test_first_try_win_scores_full_100 and test_wrong_guess_always_subtracts.
    if outcome == "Win":
        points = 100 - 10 * (attempt_number - 1)
        return current_score + max(points, 10)
    if outcome in ("Too High", "Too Low"):
        return current_score - 5
    return current_score
