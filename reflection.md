# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I first ran the game it was unplayable. The hints were backwards
(being told to "go higher" when I'd already guessed too high), the secret
number appeared to change on some submits, and the score moved in
directions that made no sense. Winning was nearly impossible, and even
when I did win on the first try the score wasn't the full 100. It looked
like a game, but every feedback signal it gave me was unreliable.

**Bug Reproduction Log**

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess 60 when secret is 50 | Hint: go LOWER | Hint said "📈 Go HIGHER!" | None (silent logic bug) |
| Guess 9 when secret is 50 on an even attempt | Hint: go HIGHER | Hint said "Too High" (string compare: "9" > "50") | None (silent type bug) |
| Guess too high on attempt 2 | Score decreases | Score *increased* by 5 | None |
| Win on first attempt | Score = 100 | Score = 80 | None |
| Click "New Game" after losing | Game restarts | Game stayed "lost" / stopped | None |

---

## 2. How did you use AI as a teammate?

I used Claude (in Claude Code) as a pair programmer, working in phases:
investigate, fix, test, document, with my approval at each step.
**Correct suggestion:** the AI proposed splitting `check_guess` so it
returns only the outcome string and moving the emoji text into a separate
`hint_message()` function. I verified this by running the starter tests,
which expected `check_guess(...) == "Win"` and now passed unchanged.
**Incorrect/misleading angle:** the original AI-generated code "claimed to
be production-ready" but its `check_guess` had a `try/except TypeError`
fallback that silently compared numbers as strings — a confident-looking
solution that was actually a hidden bug. That taught me to distrust code
that quietly swallows type errors.

---

## 3. Debugging and testing your fixes

I decided a bug was fixed only when a test captured the correct behavior
and passed. For example, `test_large_values` checks that
`check_guess(1000000, 999999) == "Too High"` — under the old
string-comparison bug this would have failed, so it acts as a regression
guard. The AI helped me design edge-case tests I wouldn't have thought of
immediately: negative numbers, decimal input being truncated, and very
large values that expose lexicographic-vs-numeric comparison bugs. In the
end all 13 tests pass, which gave me confidence the logic is correct.

---

## 4. What did you learn about Streamlit and state?

Streamlit re-runs your entire script from top to bottom every time you
interact with a widget — so any normal variable resets on every click.
`st.session_state` is the fix: it's a dictionary that survives reruns, so
the secret number, score, and attempts persist between submits. I'd
explain it to a friend like this: the script is a stage play that restarts
from scene one every time the audience claps, and `session_state` is the
only notebook the actors are allowed to carry between performances.

---

## 5. Looking ahead: your developer habits

The habit I want to keep is **writing a failing test that captures the bug
before fixing it**, then making it pass — it turns "I think it works" into
"I can prove it works." Next time I'd be more skeptical of AI code up
front and read it for hidden `except` blocks and silent fallbacks before
trusting it, rather than only reacting once something breaks. Overall this
project changed how I see AI-generated code: it's a fast first draft from a
confident teammate who still makes mistakes, so my job is to verify, not
just accept.
