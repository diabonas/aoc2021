#!/usr/bin/python
# SPDX-License-Identifier: MIT

import copy
import json


# Access the element of a snailfish number given by the position, e.g.
# position=[0,1] gives the second element of the first element of number etc.
def get_element_at_position(number, position):
    if len(position) == 0:
        return number
    else:
        return get_element_at_position(number[position[0]], position[1:])


# Find a nested pair according to the rules for exploding a snailfish number
# and return its position, or None if there is no such pair
def find_nested_pair(number, position=[]):
    if isinstance(number, int):
        return None
    elif len(position) < 4:
        for i in [0, 1]:
            pair = find_nested_pair(number[i], position + [i])
            if pair is not None:
                return pair
        return None
    elif (
        len(position) == 4 and isinstance(number[0], int) and isinstance(number[1], int)
    ):
        return position
    else:
        return None


# Find the positions of the regular numbers adjacent to a given position: the
# first element of the return value is the position of the left regular number
# (or None if there is none), the second one is the right regular number
def find_adjacent_regulars(number, position):
    adjacents = [None, None]
    for left in [0, 1]:
        # If we are at the left-most (right-most) element, there is no adjacent
        # regular number
        if all(p == left for p in position):
            continue

        # Find the deepest position where we can go into the desired direction
        deepest = len(position) - position[::-1].index(1 - left) - 1
        position_regular = position[:deepest]
        regular = get_element_at_position(number, position_regular)

        # Go into the desired direction
        position_regular += [left]
        regular = regular[left]

        # Now we need to go into the opposite direction to find the element
        # that is directly adjacent
        while not isinstance(regular, int):
            position_regular += [1 - left]
            regular = regular[1 - left]

        adjacents[left] = position_regular

    return adjacents


# Explode a snailfish number in-place according to the rules, returns if an
# explosion has taken place or not
def explode(number):
    position_pair = find_nested_pair(number)
    if position_pair is not None:
        pair = get_element_at_position(number, position_pair)
        adjacents = find_adjacent_regulars(number, position_pair)
        for i, adjacent in enumerate(adjacents):
            if adjacent is not None:
                get_element_at_position(number, adjacent[:-1])[adjacent[-1]] += pair[i]
        get_element_at_position(number, position_pair[:-1])[position_pair[-1]] = 0
        return True
    else:
        return False


# Find regular numbers greater or equal to 10 according to the rules for
# splitting a snailfish number
def find_big_regular(number, position=[]):
    if isinstance(number, int):
        if number >= 10:
            return position
        else:
            return None
    else:
        for i in [0, 1]:
            big = find_big_regular(number[i], position + [i])
            if big is not None:
                return big
        return None


# Split a snailfish number in-place according to the rules, returns if a split
# has taken place or not
def split(number):
    position_big = find_big_regular(number)
    if position_big is not None:
        big = get_element_at_position(number, position_big)
        get_element_at_position(number, position_big[:-1])[position_big[-1]] = [
            big // 2,
            big - big // 2,
        ]
        return True
    else:
        return False


# Iteratively reduce a snailfish number in-place according to the rules
def reduce(number):
    reduced = True
    while reduced:
        reduced = explode(number)
        if reduced:
            # Always explode first if possible
            continue
        reduced = split(number)
    return number


# Add two snailfish numbers according to the rules, return the reduced result
def add(a, b):
    # Further operations should not modify the original numbers added, so we
    # need to copy them because reduce works in-place
    return reduce([copy.deepcopy(a), copy.deepcopy(b)])


# Calculate the magnitude of a snailfish number according to the rules
def magnitude(number):
    if isinstance(number, int):
        return number
    else:
        return 3 * magnitude(number[0]) + 2 * magnitude(number[1])


with open("input", "r") as file:
    numbers = [json.loads(line) for line in file]

result = numbers[0]
for number in numbers[1:]:
    result = add(result, number)

print("magnitude of the sum of all snailfish numbers: %i" % magnitude(result))
