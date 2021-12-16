#!/usr/bin/python
# SPDX-License-Identifier: MIT

with open("input", "r") as file:
    depths = list(map(int, file))

differences = [j - i for i, j in zip(depths[:-1], depths[1:])]
increases = len([i for i in differences if i > 0])
print(f"number of depth increases: {increases}")
