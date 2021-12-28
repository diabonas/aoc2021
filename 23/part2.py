#!/usr/bin/python
# SPDX-License-Identifier: MIT

import math
from functools import cache

TYPES = ["A", "B", "C", "D"]
ENERGIES = [1, 10, 100, 1000]

with open("input", "r") as file:
    diagram = file.readlines()

assert len(diagram) == 5
assert len(diagram[0]) == 14

diagram.insert(3, "  #D#C#B#A#")
diagram.insert(4, "  #D#B#A#C#")

HALLWAY_ROW = 1
HALLWAY_COLUMNS = [
    column
    for column in range(len(diagram[HALLWAY_ROW]))
    if diagram[HALLWAY_ROW][column] == "." and diagram[HALLWAY_ROW + 1][column] == "#"
]

ROOM_MAX_ROW = len(diagram)-2

initial_configuration = tuple(
    frozenset(
        [
            (row, column)
            for row in range(len(diagram))
            for column in range(len(diagram[row]))
            if diagram[row][column] == t
        ]
    )
    for t in TYPES
)


# Returns the type of the amphipod at the indicated position (0 for type A, 1
# for type B, ...)
def amphipod_type(configuration, amphipod):
    return [amphipod in positions for positions in configuration].index(True)


# Returns the x coordinate of the final room for the amphiphod at the indicated
# position
def final_room(configuration, amphipod):
    return 2 * amphipod_type(configuration, amphipod) + 3


# Returns a list of all spaces the amphipod at the indicated position can go to
# in the current configuration
def valid_new_spaces(configuration, amphipod):
    if amphipod[0] != HALLWAY_ROW and any(
        (i, amphipod[1]) in positions
        for i in range(HALLWAY_ROW + 1, amphipod[0])
        for positions in configuration
    ):
        # In a room and blocked by other amphipods closer to the door
        return []
    elif amphipod[0] != HALLWAY_ROW and all(
        amphipod[1] == final_room(configuration, (i, amphipod[1]))
        for i in range(amphipod[0], ROOM_MAX_ROW + 1)
    ):
        # Up to this space, the room is already filled with the correct
        # amphipods
        return []
    else:
        # Next occupied space left and right of the current x position in the
        # hallway
        hallway_occupied_left = max(
            (
                h
                for h in HALLWAY_COLUMNS
                for positions in configuration
                if (HALLWAY_ROW, h) in positions and h < amphipod[1]
            ),
            default=min(HALLWAY_COLUMNS) - 1,
        )
        hallway_occupied_right = min(
            (
                h
                for h in HALLWAY_COLUMNS
                for positions in configuration
                if (HALLWAY_ROW, h) in positions and h > amphipod[1]
            ),
            default=max(HALLWAY_COLUMNS) + 1,
        )
        hallway_reachable = range(hallway_occupied_left + 1, hallway_occupied_right)
        if amphipod[0] != HALLWAY_ROW:
            # Move from a room into the hallway. Note that we may be able to go
            # directly into the destination room, but this is equivalent to
            # going into the hallway and then going into the room (because the
            # way must be free anyway).
            return [(HALLWAY_ROW, h) for h in HALLWAY_COLUMNS if h in hallway_reachable]
        else:
            if final_room(configuration, amphipod) not in hallway_reachable:
                # From the hallway, we can only move into the destination room,
                # but the way is blocked at the moment
                return []
            elif any(
                (i, final_room(configuration, amphipod)) in positions
                and amphipod_type(
                    configuration, (i, final_room(configuration, amphipod))
                )
                != amphipod_type(configuration, amphipod)
                for positions in configuration
                for i in range(HALLWAY_ROW + 1, ROOM_MAX_ROW + 1)
            ):
                # The room still contains amphipods of the wrong type and
                # cannot be filled yet
                return []
            else:
                # Move as far into the room as we can go
                farthest = max(
                    (
                        i
                        for i in range(HALLWAY_ROW + 1, ROOM_MAX_ROW + 1)
                        if (i, final_room(configuration, amphipod))
                        not in configuration[amphipod_type(configuration, amphipod)]
                    )
                )
                return [(farthest, final_room(configuration, amphipod))]


# Returns the required energy for moving the amphipod at the given position to
# a new destination
def movement_energy(configuration, amphipod, destination):
    if amphipod[1] == destination[1]:
        # Move up or down inside a room
        return (
            abs(destination[0] - amphipod[0])
            * ENERGIES[amphipod_type(configuration, amphipod)]
        )
    else:
        # Move out of the room, then through the hallway and finally into the
        # new room
        return (
            (amphipod[0] - HALLWAY_ROW)
            + abs(destination[1] - amphipod[1])
            + (destination[0] - HALLWAY_ROW)
        ) * ENERGIES[amphipod_type(configuration, amphipod)]


# Moves the amphipod at the given position to a new destination, returns the
# new configuration and the required movement energy
def move(configuration, amphipod, destination):
    return tuple(
        [
            (positions | {destination}) - {amphipod}
            if amphipod in positions
            else positions
            for positions in configuration
        ]
    ), movement_energy(configuration, amphipod, destination)


# Returns the least energy required to organise the amphipods from the current
# configuration, given that we have already spent current_energy to get to this
# configuration
@cache
def least_energy(configuration):
    if all(
        amphipod[1] == final_room(configuration, amphipod)
        for positions in configuration
        for amphipod in positions
    ):
        return 0

    min_energy = math.inf
    for amphipod in (pos for positions in configuration for pos in positions):
        for destination in valid_new_spaces(configuration, amphipod):
            new_configuration, energy = move(configuration, amphipod, destination)
            energy += least_energy(new_configuration)
            min_energy = min(energy, min_energy)
    return min_energy


print(
    "least energy to organise the amphipods: %i" % least_energy(initial_configuration)
)
