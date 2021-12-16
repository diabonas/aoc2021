#!/usr/bin/python
# SPDX-License-Identifier: MIT

STEPS = 100


with open("input", "r") as file:
    energy_levels = [[int(l) for l in line.strip()] for line in file.readlines()]

flashes = 0
for steps in range(STEPS):
    flashed = [[False] * len(row) for row in energy_levels]

    energy_levels = [[l + 1 for l in row] for row in energy_levels]

    while any(l > 9 for row in energy_levels for l in row):
        for row in range(len(energy_levels)):
            for column in range(len(energy_levels[row])):
                if energy_levels[row][column] > 9:
                    energy_levels[row][column] = 0
                    flashed[row][column] = True

                    for r in range(max(row - 1, 0), min(row + 2, len(energy_levels))):
                        for c in range(
                            max(column - 1, 0), min(column + 2, len(energy_levels))
                        ):
                            if not flashed[r][c]:
                                energy_levels[r][c] += 1

    flashes += len([f for row in flashed for f in row if f])

print(f"number of flashes after {STEPS} steps: {flashes}")
