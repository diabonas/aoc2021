#!/usr/bin/python
# SPDX-License-Identifier: MIT

import math
import re


def parse_line(line):
    match = re.fullmatch(
        r"(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)",
        line.strip(),
    )
    step = {
        "on": match.group(1) == "on",
        "dimensions": [
            range(int(match.group(2)), int(match.group(3)) + 1),
            range(int(match.group(4)), int(match.group(5)) + 1),
            range(int(match.group(6)), int(match.group(7)) + 1),
        ],
    }
    return step


def size(cuboid):
    return math.prod(len(cuboid["dimensions"][i]) for i in range(3))


# Returns the dimensions of the overlaps between two cuboids (which is another
# cuboid), or None if there is no overlap
def overlap(cuboid1, cuboid2):
    overlaps = [
        # Calculate the intersection of two intervals
        range(
            max(cuboid1["dimensions"][i][0], cuboid2["dimensions"][i][0]),
            min(cuboid1["dimensions"][i][-1], cuboid2["dimensions"][i][-1]) + 1,
        )
        for i in range(3)
    ]
    if any(len(overlap) == 0 for overlap in overlaps):
        return None
    else:
        return overlaps


# Count the cubes that are turned on after executing the given steps
def cubes_count(steps):
    count = 0
    for step_num, step in enumerate(steps):
        if step["on"]:
            count += size(step)

        # Calculate all overlaps with previous cuboids
        overlaps = []
        for cuboid in steps[:step_num]:
            restricted = overlap(cuboid, step)
            if restricted is not None:
                overlaps.append({"on": cuboid["on"], "dimensions": restricted})

        # Calculate the number of cubes in the overlap that are on. These need
        # to be substracted, either because we are turning them off in the
        # current step, or because we have double-counted them when turning the
        # current cuboid on.
        if len(overlaps) > 0:
            count -= cubes_count(overlaps)
    return count


with open("input", "r") as file:
    steps = list(map(parse_line, file))

print("number of turned on cubes: %i" % cubes_count(steps))
