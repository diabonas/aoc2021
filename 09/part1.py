#!/usr/bin/python
# SPDX-License-Identifier: MIT


def adjacent_positions(row, column):
    adjacent = []

    if row > 0:
        adjacent.append((row - 1, column))
    if row < len(heightmap) - 1:
        adjacent.append((row + 1, column))
    if column > 0:
        adjacent.append((row, column - 1))
    if column < len(heightmap[row]) - 1:
        adjacent.append((row, column + 1))

    return adjacent


with open("input", "r") as file:
    heightmap = [[int(h) for h in line.strip()] for line in file.readlines()]

low_points = []
for row in range(len(heightmap)):
    for column in range(len(heightmap[row])):
        adjacent = [heightmap[p[0]][p[1]] for p in adjacent_positions(row, column)]
        if heightmap[row][column] < min(adjacent):
            low_points.append((row, column))

risk_levels = [heightmap[p[0]][p[1]] + 1 for p in low_points]

print("sum of the risk levels of all low points: %i" % sum(risk_levels))
