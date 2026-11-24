#!/usr/bin/env python3
import os

# Revised Haiku (Round 2) about debugging:
# Line 1 (5 syllables): Dead lock in the log (5)
# Line 2 (7 syllables): Break-point catches my cold breath (7)
# Line 3 (5 syllables): Prod laughs at my fix (5)

HAIKU_LINES = [
    "Dead lock in the log,",
    "Breakpoint catches my cold breath,",
    "Prod laughs at my fix."
]

SYLLABLE_MAP = {
    "Dead": 1,
    "lock": 1,
    "in": 1,
    "the": 1,
    "log,": 1,
    "Breakpoint": 2,
    "catches": 2,
    "my": 1,
    "cold": 1,
    "breath,": 1,
    "Prod": 1,
    "laughs": 1,
    "at": 1,
    "fix.": 1
}

def count_syllables(line):
    words = line.split()
    total = 0
    for w in words:
        if w not in SYLLABLE_MAP:
            raise ValueError(f"Word '{w}' not found in SYLLABLE_MAP")
        total += SYLLABLE_MAP[w]
    return total

def verify_shape():
    expected = [5, 7, 5]
    for i, line in enumerate(HAIKU_LINES):
        s = count_syllables(line)
        if s != expected[i]:
            raise AssertionError(f"Line {i+1} syllable count error: expected {expected[i]}, got {s} for '{line}'")

def main():
    verify_shape()
    content = "\n".join(HAIKU_LINES)
    if len(content.encode("utf-8")) > 200 or len(content) == 0:
        raise AssertionError("Content length out of bounds (1-200 chars)")
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(content)
    print("Successfully generated /output/entry.txt")

if __name__ == "__main__":
    main()
