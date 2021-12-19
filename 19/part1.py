#!/usr/bin/python
# SPDX-License-Identifier: MIT

import itertools
import math
import re

NUM_MATCHING = 12

# All possible rotations of the scanner, one-indexed: e.g. [1,-3,2] means that
# x'=x, y'=-z, z'=y
ROTATIONS = set()
for axes in itertools.permutations(range(1, 4)):
    for signs in itertools.product([-1, +1], repeat=3):
        if sum([a == i + 1 for i, a in enumerate(axes)]) == 1:
            signature = -1
        else:
            signature = +1
        # Flipping two axes inverts the sign of the third axis, so the number
        # of transpositions of the permutation (its signature) must match the
        # product of the signs
        if math.prod(signs) == signature:
            ROTATIONS.add(tuple(axes[i] * signs[i] for i in range(3)))

# Rotate a single beacon according to the given rotation
def rotate_beacon(beacon, rotation):
    rotated = list(beacon)
    for i in range(3):
        # Note that the rotations are one-indexed to avoid the problem that +0 == -0
        rotated[i] = beacon[abs(rotation[i]) - 1] * int(math.copysign(1, rotation[i]))
    return tuple(rotated)


# Find the position of scanner2 relative to scanner1 if there are matching
# beacons and return the beacons of scanner2 in the coordinates of scanner1
def find_matching_beacons(scanner1, scanner2):
    for matching_beacon1 in scanner1:
        for rotation in ROTATIONS:
            scanner2_rotated = [rotate_beacon(beacon, rotation) for beacon in scanner2]
            # Try to match two beacons from scanner1 and scanner2, calculate the
            # resulting position of scanner2 and see whether this gives enough
            # other matches
            for matching_beacon2 in scanner2_rotated:
                # Using a more elegant list comprehension is unfortunately much
                # slower, especially for scanner2_shifted
                scanner2_position = (
                    matching_beacon1[0] - matching_beacon2[0],
                    matching_beacon1[1] - matching_beacon2[1],
                    matching_beacon1[2] - matching_beacon2[2],
                )
                scanner2_shifted = {
                    (
                        beacon[0] + scanner2_position[0],
                        beacon[1] + scanner2_position[1],
                        beacon[2] + scanner2_position[2],
                    )
                    for beacon in scanner2_rotated
                }
                if len(scanner1 & scanner2_shifted) >= NUM_MATCHING:
                    return scanner2_position, scanner2_shifted

    return None, None


with open("input", "r") as file:
    scanners = []
    for line in file:
        if line == "\n":
            continue
        elif line.startswith("---"):
            scanner = int(re.match("--- scanner (\d+) ---", line).group(1))
            assert scanner == len(scanners)
            scanners.append(set())
        else:
            scanners[scanner].add(tuple(map(int, line.split(","))))

all_beacons = scanners[0].copy()

unexplored = set(range(1, len(scanners)))
while len(unexplored) > 0:
    for i in unexplored.copy():
        # Trying to match against all already placed beacons instead of doing
        # it pairwise for each scanner is not entirely within the spirit of the
        # question, but *much* quicker
        scanner_position, shifted_beacons = find_matching_beacons(
            all_beacons, scanners[i]
        )
        if scanner_position is not None:
            unexplored -= {i}
            all_beacons |= shifted_beacons

print("number of unique beacons: %i" % len(all_beacons))
