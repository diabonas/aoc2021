#!/usr/bin/python
# SPDX-License-Identifier: MIT

import numpy as np

NUMBER_OF_DAYS = 256

with open("input", "r") as file:
    initial_state = list(map(int, file.readline().split(",")))

initial_ages = np.array([initial_state.count(age) for age in range(9)])

TRANSITION_MATRIX = np.array(
    [
        [0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
)

final_ages = np.linalg.matrix_power(TRANSITION_MATRIX, NUMBER_OF_DAYS).dot(initial_ages)
sum_lanternfish = sum(final_ages)

print(f"number of lanternfish after {NUMBER_OF_DAYS} days: {sum_lanternfish}")
