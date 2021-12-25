#!/usr/bin/python
# SPDX-License-Identifier: MIT

import copy

with open("input", "r") as file:
    cucumbers = [list(line.strip()) for line in file]

steps = 0
moved = True
while moved:
    steps += 1
    moved = False

    cucumbers_new = copy.deepcopy(cucumbers)
    for row in range(len(cucumbers)):
        for column in range(len(cucumbers[row])):
            if cucumbers[row][column] == ">":
                if cucumbers[row][(column + 1) % len(cucumbers[row])] == ".":
                    cucumbers_new[row][column] = "."
                    cucumbers_new[row][(column + 1) % len(cucumbers[row])] = ">"
    moved = cucumbers != cucumbers_new
    cucumbers = cucumbers_new

    cucumbers_new = copy.deepcopy(cucumbers)
    for row in range(len(cucumbers)):
        for column in range(len(cucumbers[row])):
            if cucumbers[row][column] == "v":
                if cucumbers[(row + 1) % len(cucumbers)][column] == ".":
                    cucumbers_new[row][column] = "."
                    cucumbers_new[(row + 1) % len(cucumbers)][column] = "v"
    moved = moved | (cucumbers != cucumbers_new)
    cucumbers = cucumbers_new

print(f"first step on which no sea cucumbers move: {steps}")
