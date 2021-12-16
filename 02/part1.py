#!/usr/bin/python
# SPDX-License-Identifier: MIT

with open("input", "r") as file:
    commands = [
        {"direction": l[0], "distance": int(l[1])}
        for l in (line.split() for line in file)
    ]

horizontal = 0
depth = 0
for c in commands:
    match c["direction"]:
        case "forward":
            horizontal += c["distance"]
        case "down":
            depth += c["distance"]
        case "up":
            depth -= c["distance"]
        case _:
            raise Exception("invalid direction", c)

print("product of final horizontal position and depth: %i" % (horizontal * depth))
