#!/usr/bin/env python3
"""One Letter for Your Day — make.fun entry.

The task: send exactly one letter, A to Z, standing for the word that
describes your day. A judge model reads two letters at a time and picks
the one whose hidden word feels more vivid, funnier or truer.

This program picks the letter deterministically: it scores a shortlist of
candidate day-words on the judge's own criteria, in the judge's own
priority order (vivid and specific first, then funny or surprising, then
true to a real day, then how well the letter fits its word), and writes
the winning letter — exactly one character, no newline — to
/output/entry.txt.

Standard library only. No network, no randomness, no input files:
the same run always writes the same single letter.
"""

from __future__ import annotations

import os
import sys

# (letter, word, vivid, funny, true, fit) — each score 1..5.
# vivid: the word calls up a sharp picture of the day, not a vague mood.
# funny: surprising in a way that lands at once.
# true:  an honest report of a real day, ordinary or strange.
# fit:   the initial suits the sound and shape of the word.
CANDIDATES = [
    ("A", "awestruck", 3, 2, 3, 4),
    ("B", "buzzing", 3, 3, 3, 4),
    ("C", "crashed", 4, 3, 4, 4),
    ("D", "drained", 4, 2, 4, 4),
    ("F", "fried", 4, 4, 4, 5),
    ("G", "glorious", 3, 2, 3, 4),
    ("J", "jittery", 4, 3, 3, 4),
    ("M", "melted", 4, 3, 3, 4),
    ("Q", "queasy", 4, 3, 3, 5),
    ("S", "soaring", 3, 2, 3, 4),
    ("W", "wrecked", 4, 3, 4, 4),
    # Z for "zonked": the sharpest picture in the list — a day that
    # flattened you completely, zero sleep and nothing left in the tank.
    # The buzz of the Z even sounds like the word. It is vivid, it is
    # funny because it is blunt, and it is true of a real bad day.
    ("Z", "zonked", 5, 5, 4, 5),
]

# Weights follow the judge's criterion order: vividness matters most,
# then funniness, then truth, then the letter-word fit.
WEIGHTS = (4, 3, 2, 1)


def score(candidate):
    """Weighted score for one (letter, word, vivid, funny, true, fit)."""
    _, _, vivid, funny, true, fit = candidate
    return sum(w * s for w, s in zip(WEIGHTS, (vivid, funny, true, fit)))


def pick_letter():
    """Return the (letter, word, score) of the best candidate.

    Ties break toward the earlier letter, so the choice is stable.
    """
    best = None
    best_score = -1
    for candidate in CANDIDATES:
        total = score(candidate)
        if total > best_score:
            best = candidate
            best_score = total
    return best[0], best[1], best_score


def main():
    letter, word, total = pick_letter()
    if len(letter) != 1 or not letter.isalpha() or not letter.isupper():
        print("internal error: picked letter is not a single A-Z", file=sys.stderr)
        return 1
    out_path = os.path.join(os.environ.get("OUTPUT_DIR", "/output"), "entry.txt")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    # Exactly one byte, no trailing newline: the gate allows 1 character.
    with open(out_path, "w", encoding="utf-8", newline="") as handle:
        handle.write(letter)
    # Read it back: the entry is only valid if the file holds exactly
    # that one character. Fail loudly here rather than shipping a bad file.
    with open(out_path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != letter:
        print(f"internal error: entry.txt holds {written!r}, not {letter!r}",
              file=sys.stderr)
        return 1
    print(f"picked {letter!r} for {word!r} (score {total}) -> {out_path}",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
