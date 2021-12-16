#!/usr/bin/python
# SPDX-License-Identifier: MIT

BRACKETS = {"(": ")", "[": "]", "{": "}", "<": ">"}

POINTS_INCOMPLETE = {")": 1, "]": 2, "}": 3, ">": 4}

with open("input", "r") as file:
    navigation_subsystem = [line.strip() for line in file.readlines()]

scores = []
for line in navigation_subsystem:
    opening_brackets = []
    for character in line:
        if character in BRACKETS:
            opening_brackets.append(character)
        elif character != BRACKETS[opening_brackets.pop()]:
            break
    else:
        completion = [BRACKETS[c] for c in opening_brackets[::-1]]
        score = 0
        for character in completion:
            score = 5 * score + POINTS_INCOMPLETE[character]
        scores.append(score)

scores = sorted(scores)
middle_score = scores[len(scores) // 2]

print(f"middle score: {middle_score}")
