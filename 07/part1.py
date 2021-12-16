#!/usr/bin/python
# SPDX-License-Identifier: MIT

import math

with open("input", "r") as file:
    horizontal_positions = list(map(int, file.readline().split(",")))

cheapest = math.inf
for align in range(min(horizontal_positions), max(horizontal_positions) + 1):
    fuel = sum(abs(p - align) for p in horizontal_positions)
    if fuel < cheapest:
        cheapest = fuel

# Alternative:
# align = int(statistics.median(horizontal_positions))
# cheapest = sum(abs(p - align) for p in horizontal_positions)

print(f"cheapest total fuel: {cheapest}")
