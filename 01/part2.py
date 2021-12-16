#!/usr/bin/python
# SPDX-License-Identifier: MIT

with open("input", "r") as file:
    depths = list(map(int, file))

windows = [i + j + k for i, j, k in zip(depths[:-2], depths[1:-1], depths[2:])]
differences = [j - i for i, j in zip(windows[:-1], windows[1:])]
increases = len([i for i in differences if i > 0])
print(f"number of depth increases: {increases}")
