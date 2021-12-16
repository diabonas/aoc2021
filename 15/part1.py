#!/usr/bin/python
# SPDX-License-Identifier: MIT

import math
from queue import PriorityQueue


def dijkstra(risk_levels):
    size = len(risk_levels)
    assert all(len(row) == size for row in risk_levels)

    start = (0, 0)
    end = (size - 1, size - 1)

    # risk holds the current best total risk from the start to the respective
    # position
    risk = [[math.inf] * size for row in range(size)]
    risk[start[0]][start[1]] = 0

    # prev is the previous position on the best path to the respective
    # position (allowing to iteratively reconstruct the best path)
    # prev = [[None] * size for row in range(size)]

    # visited is True if we have found the final total risk from the start to
    # the respective position
    visited = [[False] * size for row in range(size)]

    risk[start[0]][start[1]] = 0

    queue = PriorityQueue()
    queue.put((risk[start[0]][start[1]], start))

    while not queue.empty():
        # This is the unexplored position with the lowest risk from the start.
        # There can be no better total risk than that, so mark as visited.
        (current_risk, current_pos) = queue.get()
        visited[current_pos[0]][current_pos[1]] = True

        # Since we are only interested in the total risk to the lower right
        # corner, we can finish early if we have found it
        if current_pos == end:
            break

        # Look at the orthogonally adjacent neighbours of the current position
        # and update their risks
        for diff in {(-1, 0), (0, -1), (1, 0), (0, 1)}:
            neighbour = (current_pos[0] + diff[0], current_pos[1] + diff[1])
            # Skip if we are at the edge of the cavern or we have already found
            # the final risk for this neighbour
            if (
                neighbour[0] not in range(size)
                or neighbour[1] not in range(size)
                or visited[neighbour[0]][neighbour[1]]
            ):
                continue

            # See if we can do better for the risk of this neighbour by
            # accessing it via current_pos
            alt = current_risk + risk_levels[neighbour[0]][neighbour[1]]
            if alt < risk[neighbour[0]][neighbour[1]]:
                risk[neighbour[0]][neighbour[1]] = alt
                # prev[neighbour[0]][neighbour[1]] = current_pos
                queue.put((alt, neighbour))

    return risk[end[0]][end[1]]


with open("input", "r") as file:
    risk_levels = [[int(l) for l in line.strip()] for line in file.readlines()]

print(
    "lowest total risk from the top left to the bottom right: %i"
    % dijkstra(risk_levels)
)
