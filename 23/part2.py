#!/usr/bin/python
# SPDX-License-Identifier: MIT

import itertools
import math

ROOM_SIZE = 4
ENERGY = {"A": 1, "B": 10, "C": 100, "D": 1000}

# x=0 is the hallway, x>0 are the rooms
# y=0 is the leftmost hallway space, y=10 is the rightmost one
FINAL_ROOM_X = {"A": 2, "B": 4, "C": 6, "D": 8}
HALLWAY_X = [0, 1, 3, 5, 7, 9, 10]

# Returns a list of all spaces the amphipod at the indicated position can go to
# in the current configuration
def valid_new_spaces(configuration, amphipod):
    if amphipod[1] != 0 and any(
        (amphipod[0], i) in configuration for i in range(amphipod[1])
    ):
        # In a room and blocked by other amphipods closer to the door
        return []
    elif amphipod[1] != 0 and all(
        amphipod[0] == FINAL_ROOM_X[configuration[(amphipod[0], i)]]
        for i in range(amphipod[1], ROOM_SIZE + 1)
    ):
        # Up to this space, the room is already filled with the correct
        # amphipods
        return []
    else:
        # Next occupied space left and right of the current x position in the
        # hallway
        hallway_occupied_left = max(
            (h for h in HALLWAY_X if (h, 0) in configuration and h < amphipod[0]),
            default=-1,
        )
        hallway_occupied_right = min(
            (h for h in HALLWAY_X if (h, 0) in configuration and h > amphipod[0]),
            default=11,
        )
        hallway_reachable = range(hallway_occupied_left + 1, hallway_occupied_right)
        if amphipod[1] != 0:
            # Move from a room into the hallway. Note that we may be able to go
            # directly into the destination room, but this is equivalent to
            # going into the hallway and then going into the room (because the
            # way must be free anyway).
            return {(h, 0) for h in HALLWAY_X if h in hallway_reachable}
        else:
            if FINAL_ROOM_X[configuration[amphipod]] not in hallway_reachable:
                # From the hallway, we can only move into the destination room,
                # but the way is blocked at the moment
                return []
            elif any(
                (FINAL_ROOM_X[configuration[amphipod]], i) in configuration
                and configuration[(FINAL_ROOM_X[configuration[amphipod]], i)]
                != configuration[amphipod]
                for i in range(1, ROOM_SIZE + 1)
            ):
                # The room still contains amphipods of the wrong type and
                # cannot be filled yet
                return []
            else:
                # Move as far into the room as we can go
                farthest = max(
                    (
                        i
                        for i in range(1, ROOM_SIZE + 1)
                        if (FINAL_ROOM_X[configuration[amphipod]], i)
                        not in configuration
                    )
                )
                return [(FINAL_ROOM_X[configuration[amphipod]], farthest)]


# Returns the required energy for moving the amphipod at the given position to
# a new destination
def movement_energy(configuration, amphipod, destination):
    if amphipod[0] == destination[0]:
        # Move up or down inside a room
        return abs(destination[1] - amphipod[1]) * ENERGY[configuration[amphipod]]
    else:
        # Move out of the room, then through the hallway and finally into the
        # new room
        return (
            amphipod[1] + abs(destination[0] - amphipod[0]) + destination[1]
        ) * ENERGY[configuration[amphipod]]


# Returns a lower bound for the cost of moving all antipods into their
# destination room
def swap_energy(configuration):
    return sum(
        movement_energy(configuration, pos, (FINAL_ROOM_X[configuration[pos]], 1))
        for pos in configuration
        if pos[0] != FINAL_ROOM_X[configuration[pos]]
    )


global_min_energy = math.inf
# Returns the least energy required to organise the amphipods from the current
# configuration, given that we have already spent current_energy to get to this
# configuration
def least_energy(configuration, energy=0):
    global global_min_energy

    if all(
        amphipod[0] == FINAL_ROOM_X[configuration[amphipod]]
        for amphipod in configuration
    ):
        return energy

    min_energy = math.inf
    for amphipod, destination in sorted(
        (
            movement
            for amphipod in configuration
            for movement in itertools.product(
                [amphipod], valid_new_spaces(configuration, amphipod)
            )
        ),
        key=lambda movement: movement_energy(configuration, movement[0], movement[1]),
    ):
        new_configuration = configuration.copy()
        new_configuration[destination] = new_configuration.pop(amphipod)
        new_energy = energy + movement_energy(configuration, amphipod, destination)

        if new_energy + swap_energy(new_configuration) > global_min_energy:
            # Even with the absolute minimum of necessary movement, we would be
            # worse than the best solution that we have currently found
            continue

        new_energy = least_energy(new_configuration, new_energy)
        min_energy = min(new_energy, min_energy)

        if min_energy < global_min_energy:
            # Globally keep track of the best solution we have found so far to
            # avoid further exploring unprofitable configurations
            global_min_energy = min_energy
            print(f"current best energy: {global_min_energy}")
    return min_energy


with open("input", "r") as file:
    diagram = file.readlines()
    assert len(diagram) == 5
    assert len(diagram[0]) == 14
    diagram.insert(3, "  #D#C#B#A#")
    diagram.insert(4, "  #D#B#A#C#")
    initial_configuration = {
        (x, y): diagram[y + 1][x + 1]
        for x in FINAL_ROOM_X.values()
        for y in range(1, ROOM_SIZE + 1)
    }

print(
    "least energy to organise the amphipods: %i" % least_energy(initial_configuration)
)
