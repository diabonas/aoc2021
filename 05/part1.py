#!/usr/bin/python
# SPDX-License-Identifier: MIT

import math
import re


def parse_line(line):
    match = re.fullmatch(r"(\d+),(\d+) -> (\d+),(\d+)\n", line)
    return (
        (int(match.group(1)), int(match.group(2))),
        (int(match.group(3)), int(match.group(4))),
    )


def draw_line(diagram, line):
    slope = (line[1][0] - line[0][0], line[1][1] - line[0][1])
    gcd = math.gcd(slope[0], slope[1])
    slope = (slope[0] // gcd, slope[1] // gcd)

    pos = line[0]
    diagram[pos[0]][pos[1]] += 1
    while pos != line[1]:
        pos = (pos[0] + slope[0], pos[1] + slope[1])
        diagram[pos[0]][pos[1]] += 1


with open("input", "r") as file:
    lines = list(map(parse_line, file))

max_x = max(max(l[0][0], l[1][0]) for l in lines)
max_y = max(max(l[0][1], l[1][1]) for l in lines)

diagram = [[0] * (max_y + 1) for x in range(max_x + 1)]
for line in lines:
    if not (line[0][0] == line[1][0] or line[0][1] == line[1][1]):
        continue
    draw_line(diagram, line)

# for y in range(len(diagram[0])):
#     print("".join(str(diagram[x][y]) for x in range(len(diagram))))

overlaps = sum(d > 1 for row in diagram for d in row)

print(f"number of points where at least two lines overlap: {overlaps}")
