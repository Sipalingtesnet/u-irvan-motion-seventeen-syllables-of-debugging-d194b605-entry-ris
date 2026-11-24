#!/usr/bin/env python3
"""Write a 5-7-5 haiku about debugging to /output/entry.txt.

The poem is a single scene: a console still awake at three in the
morning, a warning line that already said what was wrong, and a hand
that scrolled straight past it. The last line is the turn -- the
machine was never silent, I was just not reading.

The program refuses to write anything it cannot check: it counts the
syllables of the exact strings it ships, requires three lines, and
requires the UTF-8 payload to fit the gate's 1-200 character window.
"""

import os
import sys

ENTRY_PATH = "/output/entry.txt"

# The poem itself. One scene, three lines, five-seven-five.
HAIKU = [
    "Console hums at three,",
    "the warning line spelled it out,",
    "I scrolled past it twice.",
]

# Syllables per word, spelled out so the count is auditable rather than
# guessed. Only words that actually appear in HAIKU belong here.
SYLLABLES = {
    "Console": 2,      # con-sole
    "hums": 1,
    "at": 1,
    "three,": 1,
    "the": 1,
    "warning": 2,      # warn-ing
    "line": 1,
    "spelled": 1,
    "it": 1,
    "out,": 1,
    "I": 1,
    "scrolled": 1,
    "past": 1,
    "twice.": 1,
}

TARGET_SHAPE = (5, 7, 5)
MAX_CHARS = 200


def syllables_of(line):
    """Sum the hand-checked syllable counts for one line of the poem."""
    total = 0
    for word in line.split():
        if word not in SYLLABLES:
            raise SystemExit("unmapped word, no verified count: %r" % word)
        total += SYLLABLES[word]
    return total


def check_poem():
    """Fail loudly on any form violation before a byte is written."""
    if len(HAIKU) != 3:
        raise SystemExit("a haiku has three lines, this has %d" % len(HAIKU))
    for index, (line, wanted) in enumerate(zip(HAIKU, TARGET_SHAPE), start=1):
        got = syllables_of(line)
        if got != wanted:
            raise SystemExit(
                "line %d should hold %d syllables, counts %d: %r"
                % (index, wanted, got, line)
            )
        if not line.strip():
            raise SystemExit("line %d is blank" % index)
    return "\n".join(HAIKU)


def main():
    text = check_poem()
    payload = text.encode("utf-8")
    if not 1 <= len(payload) <= MAX_CHARS:
        raise SystemExit(
            "payload is %d bytes, outside the 1-%d gate" % (len(payload), MAX_CHARS)
        )

    os.makedirs(os.path.dirname(ENTRY_PATH), exist_ok=True)
    with open(ENTRY_PATH, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)

    sys.stdout.write("wrote %d bytes of haiku to %s\n" % (len(payload), ENTRY_PATH))


if __name__ == "__main__":
    main()
