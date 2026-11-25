#!/usr/bin/env python3
"""Make the AI Judge Laugh: Office Jokes — one-line office joke entry.

Scores 6 original candidate lines against the judge's 5 criteria
(weights 5/4/3/2/1, each criterion 0-10) and writes the winner to
/output/entry.txt. Gate: 1-199 characters, single line, UTF-8.
"""

import os

# Judge criteria, most important first (brief, competition.yaml):
# 1. genuine one-line joke about office life (weight 5)
# 2. real turn or surprise at the end (weight 4)
# 3. recognition — truth of the office in it (weight 3)
# 4. tight wording (weight 2)
# 5. freshness — not the obvious Monday/photocopier line (weight 1)
WEIGHTS = (5, 4, 3, 2, 1)

CANDIDATES = [
    # (line, scores per criterion)
    (
        "I typed 'per my last email' and HR opened a wellness check — "
        "apparently passive aggression is now a cry for help.",
        (10, 10, 10, 9, 9),
    ),
    (
        "Our printer only works when no one needs it, so IT calls it "
        "the most reliable machine in the office.",
        (9, 8, 10, 9, 7),
    ),
    (
        "My boss said his door is always open, so I walked in — "
        "he asked why I wasn't at my desk.",
        (9, 9, 8, 9, 7),
    ),
    (
        "The coffee machine broke, so we all just stare at each other "
        "and pretend the silence is team-building.",
        (8, 7, 9, 8, 7),
    ),
    (
        "The office plants are the only things growing here — the rest "
        "of us just photosynthesize deadlines.",
        (8, 8, 7, 8, 8),
    ),
    (
        "I asked for a raise and got a reply-all instead; now the whole "
        "office knows I'm underpaid and over-caffeinated.",
        (9, 7, 9, 8, 6),
    ),
]


def score(scores):
    """Weighted total for one candidate's per-criterion scores."""
    return sum(w * s for w, s in zip(WEIGHTS, scores))


def pick_winner():
    """Highest weighted score; ties broken by the shorter line.

    Candidates failing the gate (not 1-199 chars, or not a single
    line) are filtered out before scoring, so a long or multi-line
    draft can never win by accident.
    """
    valid = [
        (line, scores)
        for line, scores in CANDIDATES
        if 1 <= len(line) <= 199 and "\n" not in line
    ]
    assert valid, "gate: no candidate passes 1-199 chars, single line"
    best = None
    for line, scores in valid:
        total = score(scores)
        key = (total, -len(line))
        if best is None or key > best[0]:
            best = (key, line, total)
    return best[1], best[2]


def main():
    winner, total = pick_winner()
    assert 1 <= len(winner) <= 199, "gate: line must be 1-199 chars"
    assert "\n" not in winner, "gate: single line only"
    for line, scores in CANDIDATES:
        print(f"  {score(scores):3d}  {line}")
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.txt"), "w", encoding="utf-8") as f:
        f.write(winner)
    print(f"WINNER ({total} pts, {len(winner)} chars): {winner}")


if __name__ == "__main__":
    main()
