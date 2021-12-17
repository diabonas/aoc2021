#!/usr/bin/python
# SPDX-License-Identifier: MIT

import re

with open("input", "r") as file:
    match = re.fullmatch(
        r"target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)",
        file.readline().strip(),
    )
    target = [
        (int(match.group(1)), int(match.group(2))),
        (int(match.group(3)), int(match.group(4))),
    ]
    assert target[0][0] <= target[0][1]
    assert target[1][0] <= target[1][1]

# Rough borders for the area we need to consider: if
# abs(position[0])>max_area[0] or position[1]<-max_area[1], further steps will
# never get back into the area again, and the target is fully contained in this
# area, so we can stop. This could be refined more, but at the expense of
# having to do case analysis regarding the signs of the target coordinates.
max_area = [
    max(abs(target[0][0]), abs(target[0][1])),
    max(abs(target[1][0]), abs(target[1][1])),
]

num_initial_velocities = 0

initial_velocity = [None] * 2
# Faster velocities already leave the target area in the first step
for initial_velocity[0] in range(-max_area[0], max_area[0] + 1):
    for initial_velocity[1] in range(-max_area[1], max_area[1] + 1):
        position = [0, 0]
        velocity = initial_velocity.copy()
        # Note that there is no upper bound on position[1] since we can shoot
        # as high as we want
        while abs(position[0]) <= max_area[0] and position[1] >= -max_area[1]:
            position[0] += velocity[0]
            position[1] += velocity[1]
            if velocity[0] > 0:
                velocity[0] -= 1
            elif velocity[0] < 0:
                velocity[0] += 1
            velocity[1] -= 1

            if (
                position[0] >= target[0][0]
                and position[0] <= target[0][1]
                and position[1] >= target[1][0]
                and position[1] <= target[1][1]
            ):
                num_initial_velocities += 1
                break

print(
    f"number of distinct initial velocities to reach the target: {num_initial_velocities}"
)
