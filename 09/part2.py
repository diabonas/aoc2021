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


def basin_size(row, column):
    # Mark location as already visited
    heightmap[row][column] = 10

    size = 1
    for p in adjacent_positions(row, column):
        if heightmap[p[0]][p[1]] < 9:
            size += basin_size(p[0], p[1])

    return size


with open("input", "r") as file:
    heightmap = [[int(h) for h in line.strip()] for line in file.readlines()]

low_points = []
for row in range(len(heightmap)):
    for column in range(len(heightmap[row])):
        adjacent = [heightmap[p[0]][p[1]] for p in adjacent_positions(row, column)]
        if heightmap[row][column] < min(adjacent):
            low_points.append((row, column))

basin_sizes = sorted(basin_size(p[0], p[1]) for p in low_points)

# for row in heightmap:
#     print("".join(["." if h == 10 else "9" for h in row]))

print(
    "product of the three largest basin sizes: %i"
    % (basin_sizes[-1] * basin_sizes[-2] * basin_sizes[-3])
)
