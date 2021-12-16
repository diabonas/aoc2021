#!/usr/bin/python
# SPDX-License-Identifier: MIT

with open("input", "r") as file:
    commands = [
        {"direction": l[0], "distance": int(l[1])}
        for l in (line.split() for line in file)
    ]

horizontal = 0
depth = 0
aim = 0
for c in commands:
    if c["direction"] == "forward":
        horizontal += c["distance"]
        depth += aim * c["distance"]
    elif c["direction"] == "down":
        aim += c["distance"]
    elif c["direction"] == "up":
        aim -= c["distance"]
    else:
        raise Exception("invalid direction", c)

print("product of final horizontal position and depth: %i" % (horizontal * depth))
