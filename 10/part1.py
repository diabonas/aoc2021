#!/usr/bin/python
# SPDX-License-Identifier: MIT

BRACKETS = {"(": ")", "[": "]", "{": "}", "<": ">"}

POINTS_ILLEGAL = {")": 3, "]": 57, "}": 1197, ">": 25137}

with open("input", "r") as file:
    navigation_subsystem = [line.strip() for line in file.readlines()]

syntax_error_score = 0
for line in navigation_subsystem:
    opening_brackets = []
    for character in line:
        if character in BRACKETS:
            opening_brackets.append(character)
        elif character != BRACKETS[opening_brackets.pop()]:
            syntax_error_score += POINTS_ILLEGAL[character]
            break

print(f"total syntax error score: {syntax_error_score}")
