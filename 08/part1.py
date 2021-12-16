#!/usr/bin/python
# SPDX-License-Identifier: MIT

with open("input", "r") as file:
    notes = [
        {"patterns": p.split(), "output": o.split()}
        for p, o in (l.split("|") for l in file.readlines())
    ]

for note in notes:
    digits = [None] * 10
    digits[1] = [p for p in note["patterns"] if len(p) == 2].pop()
    digits[4] = [p for p in note["patterns"] if len(p) == 4].pop()
    digits[7] = [p for p in note["patterns"] if len(p) == 3].pop()
    digits[8] = [p for p in note["patterns"] if len(p) == 7].pop()

    digits = ["".join(sorted(d)) for d in digits if d is not None]

    appearances = len([o for o in note["output"] if "".join(sorted(o)) in digits])

    note["appearances"] = appearances

appearances = sum(n["appearances"] for n in notes)
print(f"number of appearances of the digits 1, 4, 7 and 8: {appearances}")
