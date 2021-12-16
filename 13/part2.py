#!/usr/bin/python
# SPDX-License-Identifier: MIT

import numpy as np

with open("input", "r") as file:
    dots = []
    for line in file:
        if line == "\n":
            break
        dots.append(tuple(map(int, line.split(","))))

    instructions = []
    for line in file:
        instruction = line.removeprefix("fold along ").split("=")
        instructions.append({"direction": instruction[0], "line": int(instruction[1])})

max_x = max(d[0] for d in dots)
max_y = max(d[1] for d in dots)

# There should always be an odd number of rows/columns (counted including 0),
# otherwise folding might not work
if max_x % 2 == 1:
    max_x += 1
if max_y % 2 == 1:
    max_y += 1

paper = np.zeros((max_y + 1, max_x + 1), dtype=bool)

for dot in dots:
    paper[dot[1], dot[0]] = True

for instruction in instructions:
    if instruction["direction"] == "x":
        assert not np.any(paper[:, instruction["line"]])

        # The instructions always seem to fold the paper in half, otherwise some
        # padding would need to be applied to the smaller side
        assert instruction["line"] == np.shape(paper)[1] // 2

        paper = paper[:, : instruction["line"]] | paper[:, : instruction["line"] : -1]
    elif instruction["direction"] == "y":
        assert not np.any(paper[instruction["line"], :])
        assert instruction["line"] == np.shape(paper)[0] // 2
        paper = paper[: instruction["line"], :] | paper[: instruction["line"] : -1, :]
    else:
        raise Exception("invalid direction", instruction["direction"])

print("folded paper:")
for row in paper:
    print("".join("#" if x else "." for x in row))
