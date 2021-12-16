#!/usr/bin/python
# SPDX-License-Identifier: MIT

import math

with open("input", "r") as file:
    horizontal_positions = list(map(int, file.readline().split(",")))

cheapest = math.inf
for align in range(min(horizontal_positions), max(horizontal_positions) + 1):
    fuel = sum(abs(p - align) * (abs(p - align) + 1) // 2 for p in horizontal_positions)
    if fuel < cheapest:
        cheapest = fuel

# Note: the optimal alignment appears to be the mean value of horizontal_positions +-1:
# for align in [
#     math.floor(statistics.mean(horizontal_positions)),
#     math.ceil(statistics.mean(horizontal_positions)),
# ]:

print(f"cheapest total fuel: {cheapest}")
