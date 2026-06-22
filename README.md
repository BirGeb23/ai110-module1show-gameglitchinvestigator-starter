# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] **Purpose:** A Streamlit number-guessing game. The player guesses a
      secret number within a difficulty-based range and limited attempts,
      getting "higher/lower" hints and a score that rewards faster wins.
- [x] **Bugs found:** 11 total — inverted hints, a secret that was silently
      cast to a string on even turns (breaking comparisons), scoring that
      *added* points for wrong guesses, a first-try win worth only 80,
      "New Game" that didn't reset score/status/history, a range message
      hardcoded to "1 and 100", invalid input costing an attempt, and a
      "Hard" mode easier than "Normal".
- [x] **Fixes applied:** Moved all game logic into `logic_utils.py`, made
      `check_guess` return a plain outcome string with a separate
      `hint_message()`, corrected the scoring formula, and made "New Game"
      a full state reset. Verified with 13 pytest tests.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. **Start the app** with `python -m streamlit run app.py` and pick a
   difficulty in the sidebar. The info box now correctly shows the real
   range for that difficulty (e.g. "between 1 and 20" on Easy).
2. **Make a guess.** Enter a number and click "Submit Guess 🚀". The hint
   is now correct — guessing too high tells you to "📉 Go LOWER!".
3. **Watch the score.** A wrong guess always costs 5 points; it never
   accidentally rewards you. Open "Developer Debug Info" to confirm the
   secret stays the same across submits.
4. **Win the game.** Guess the secret and the game ends: balloons appear,
   a win message shows your final score, and further guesses are blocked.
   Winning on the first try scores the full 100.
5. **Click "New Game 🔁".** Score, attempts, status, and history all reset
   cleanly, and a fresh secret is drawn from the current difficulty's range.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
$ pytest tests/
============================= test session starts =============================
collected 13 items

tests/test_game_logic.py .............                                    [100%]

============================== 13 passed in 0.02s =============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
