#!/usr/bin/env python3
"""Write one 5-7-5 haiku about debugging to /output/entry.txt.

Third pass on this poem, and the picture has not moved, because two
rounds of weighing alternatives have not beaten it: a console still
humming at three in the morning, one warning line that names the fault
out loud, and a hand on the scroll wheel going straight past it. The
turn sits in line three, where the suspect stops being the machine and
becomes the person reading the screen.

What this pass actually tested were two near-neighbours of that last
line, not a rebuild of the poem:

    "I scrolled past it once."
        Softer, and truer on any single night. But once is an
        accident, and the turn only lands if the miss is a habit.
        It excuses the reader and the poem shrinks.

    "I scroll past it still."
        Tempting, because it would tidy the tense against "hums".
        But "still" is a soft adverb where the line needs a hard
        stop, and it lets the poem drift off instead of closing.

Neither earned the swap, so line three stays. The small tense seam is
kept on purpose: the console hums in the eternal present while the
incident is remembered in the past. Mending it would cost either the
live buzz of "hums" or the flat finality of "twice", and each of those
is worth more than the tidiness.

The program writes nothing it cannot verify. It counts the syllables
of the exact strings it ships, checks there are three lines with the
intended punctuation, checks the syllable map carries no orphan words,
holds the payload inside the gate's 1-200 character window, and then
reads the file back so success is measured rather than claimed.
"""

import os

ENTRY_PATH = "/output/entry.txt"
TARGET_SHAPE = (5, 7, 5)   # the only shape this program will emit
MAX_CHARS = 200            # the gate's ceiling, in UTF-8 bytes

# The poem. One room, one screen, one hand.
HAIKU = [
    "Console hums at three,",            # 5 - the machine awake and fine
    "the warning line spelled it out,",  # 7 - the fault, already named
    "I scrolled past it twice.",         # 5 - the turn: my hand, my habit
]

# How each line is allowed to end, so punctuation cannot drift silently.
ENDINGS = (",", ",", ".")

# Hand-checked syllable counts, one entry per shipped word. Spelling the
# counts out keeps the form auditable instead of guessed.
SYLLABLES = {
    "Console": 2,    # con-sole
    "hums": 1,
    "at": 1,
    "three,": 1,
    "the": 1,
    "warning": 2,    # warn-ing
    "line": 1,
    "spelled": 1,
    "it": 1,
    "out,": 1,
    "I": 1,
    "scrolled": 1,
    "past": 1,
    "twice.": 1,
}


def syllable_total(line):
    """Count one line from the map, refusing any word without a count."""
    total = 0
    for word in line.split():
        if word not in SYLLABLES:
            raise SystemExit("unmapped word, no verified count: %r" % word)
        total += SYLLABLES[word]
    return total


def find_faults():
    """Return every form fault in the poem, so all of them surface at once."""
    faults = []
    if len(HAIKU) != len(TARGET_SHAPE):
        faults.append("haiku needs %d lines, found %d" % (len(TARGET_SHAPE), len(HAIKU)))

    seen = set()
    for number, (line, wanted, ending) in enumerate(
        zip(HAIKU, TARGET_SHAPE, ENDINGS), start=1
    ):
        words = line.split()
        if not words:
            faults.append("line %d is blank" % number)
            continue
        if line != line.strip():
            faults.append("line %d has stray edge whitespace" % number)
        if not line.endswith(ending):
            faults.append("line %d should end with %r: %r" % (number, ending, line))
        seen.update(words)
        counted = syllable_total(line)
        if counted != wanted:
            faults.append(
                "line %d wants %d syllables, counts %d: %r"
                % (number, wanted, counted, line)
            )

    # A word sitting in the map but never spoken would quietly rot.
    orphans = sorted(set(SYLLABLES) - seen)
    if orphans:
        faults.append("syllable map carries unused words: %s" % ", ".join(orphans))

    return faults


def main():
    faults = find_faults()
    if faults:
        raise SystemExit("refusing to write a broken poem:\n  " + "\n  ".join(faults))

    text = "\n".join(HAIKU)
    payload = text.encode("utf-8")
    if not 1 <= len(payload) <= MAX_CHARS:
        raise SystemExit(
            "payload is %d bytes, outside the 1-%d gate" % (len(payload), MAX_CHARS)
        )

    os.makedirs(os.path.dirname(ENTRY_PATH), exist_ok=True)
    with open(ENTRY_PATH, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)

    # Measure the result instead of trusting the write.
    with open(ENTRY_PATH, "rb") as handle:
        on_disk = handle.read()
    if on_disk != payload:
        raise SystemExit("output on disk does not match the poem that was checked")

    print("wrote %d bytes, %d lines, %d syllables to %s"
          % (len(on_disk), len(HAIKU), sum(TARGET_SHAPE), ENTRY_PATH))


if __name__ == "__main__":
    main()
