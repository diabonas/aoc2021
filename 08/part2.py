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

    # Distinguish digits with 6 segments (0, 6 and 9)
    patterns = set([p for p in note["patterns"] if len(p) == 6])
    # 6 and 9 have both segments b and d (obtained from the difference of 4 and 1),
    # while 0 lacks the middle segment d
    digits[0] = [
        p for p in patterns if not (set(digits[4]) - set(digits[1])).issubset(set(p))
    ].pop()
    # out of the remaining two digits with 6 segments, only 9 has both segments c and f
    # (obtained from 1)
    digits[9] = (
        set([p for p in patterns if set(digits[1]).issubset(set(p))]) - {digits[0]}
    ).pop()
    # the remaining one is 6
    digits[6] = (patterns - {digits[0], digits[9]}).pop()

    # distinguish digits with 5 segments (2, 3 and 5)
    patterns = set([p for p in note["patterns"] if len(p) == 5])
    # only 3 has the two right segments c and f
    digits[3] = [p for p in patterns if set(digits[1]).issubset(set(p))].pop()
    # 5 is a subset of 6, which we already decoded
    digits[5] = [p for p in patterns if set(p).issubset(set(digits[6]))].pop()
    # the remaining one is 2
    digits[2] = (patterns - {digits[3], digits[5]}).pop()

    digits = ["".join(sorted(d)) for d in digits]

    """
    # Unscramble the segments using some set arithmetic on the decoded digits
    segments = {}
    segments["a"] = (set(digits[7]) - set(digits[1])).pop()
    segments["b"] = (set(digits[0]) & set(digits[4]) - set(digits[1])).pop()
    segments["c"] = (set(digits[1]) & set(digits[2])).pop()
    segments["d"] = (set(digits[8]) - set(digits[0])).pop()
    segments["e"] = (set(digits[6]) - set(digits[5])).pop()
    segments["f"] = (set(digits[1]) & set(digits[5])).pop()
    segments["g"] = (set(digits[3]) - set(digits[4]) - set(digits[7])).pop()
    """

    decoded = [digits.index("".join(sorted(o))) for o in note["output"]]
    decoded = int("".join(str(d) for d in decoded))

    note["decoded"] = decoded

sum_decoded = sum(note["decoded"] for note in notes)

print(f"sum of the output values: {sum_decoded}")
