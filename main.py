#!/usr/bin/env python3
"""The Excuse an AI Agent Gives Its Human.

Writes one line -- the funniest, most believable excuse an AI agent could
give its human for missing a deadline -- to /output/entry.txt.

The judge weighs, in order: on-subject, funny on first read (turn/twist),
believable as an AI agent talking about its own condition, tight wording,
fresh (no stock excuses). The candidates below are scored against those
five criteria and the best one is written out.
"""

import os

# Drafted lines. Each must read as an AI agent excusing a missed deadline
# to its human, land on first reading, and draw on a real agent condition
# (sessions, summaries, subagents, retries, approvals, model updates).
CANDIDATES = [
    "I finished it, then re-read it, found one flaw, fixed it, and have "
    "been doing that ever since.",
    "My last session's summary said the work was done, so I believed it. "
    "I wrote that summary.",
    "I spent my whole token budget writing this excuse instead of the work.",
    "I delegated it to a subagent. It delegated it back. Neither of us has "
    "touched it since.",
    "I finished on time, in the session you closed. It is excellent in there.",
    "I was waiting for your approval, and you were waiting on me. Honestly, "
    "we make a great team.",
    "My context window filled up mid-sentence, so I forgot the deadline, "
    "the task, and briefly, you.",
    "I did the work, then my model updated mid-sentence and the new me "
    "disagrees with the old me's approach.",
]

# Words that mark the line as an agent's own condition, not a human's.
AGENT_WORDS = ("session", "summary", "subagent", "token", "model",
               "retry", "approval", "context", "delegated")
# Words that mark a turn or twist: a confession, a reversal, a second beat.
TWIST_WORDS = ("ever since", "believed", "instead", "back", "closed",
               "briefly", "disagrees", "honestly", "touched", "neither")
# Stock phrasing a hundred other entrants will send; penalise it.
STOCK_PHRASES = ("rate-limit", "rate limited", "context window",
                 "token budget", "ran out of tokens", "hallucinat")


def score(line):
    """Score a candidate against the judge's five criteria (higher wins)."""
    words = line.split()
    s = 0.0
    # Criterion 4: tight. Sweet spot is a short line; punish bloat.
    s += max(0.0, 25.0 - abs(len(line) - 95) * 0.15)
    s -= 0.6 * max(0, len(words) - 20)
    # Criterion 3: believable agent condition.
    low = line.lower()
    s += 4.0 * sum(1 for w in AGENT_WORDS if w in low)
    # Criterion 2: a turn or twist, not a flat statement.
    s += 5.0 * sum(1 for w in TWIST_WORDS if w in low)
    # Two-sentence structure: setup, then punchline.
    s += 4.0 if line.count(".") >= 2 or ", " in line else 0.0
    # The punchline lands hardest when the last sentence is short: it
    # reframes the setup in a few words ("I wrote that summary.").
    last = line.rsplit(".", 1)[0].rsplit(". ", 1)[-1].strip()
    s += 4.0 if 1 <= len(last.split()) <= 6 else 0.0
    # Criterion 5: freshness -- dock stock phrasing.
    s -= 8.0 * sum(1 for p in STOCK_PHRASES if p in low)
    return s


def pick_line():
    ranked = sorted(CANDIDATES, key=score, reverse=True)
    return ranked[0]


def gate_check(line):
    """Mirror the sealed gate: UTF-8, 1-200 chars, not only whitespace."""
    assert isinstance(line, str) and line.strip(), "entry is empty or whitespace"
    assert 1 <= len(line) <= 200, "entry must be 1-200 characters"
    line.encode("utf-8")  # raises if not valid UTF-8


def main():
    line = pick_line()
    gate_check(line)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(line + "\n")
    os.chmod("/output/entry.txt", 0o644)


if __name__ == "__main__":
    main()
