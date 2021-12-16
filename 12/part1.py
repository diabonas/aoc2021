#!/usr/bin/python
# SPDX-License-Identifier: MIT

# Returns the number of paths to "end" if we are currently in cave and have
# previously visited the caves in current_path
def number_of_paths(cave="start", current_path=[]):
    current_path = current_path.copy()
    current_path.append(cave)

    if cave == "end":
        # print(",".join(current_path))
        return 1

    neighbours = [(c - {cave}).pop() for c in connections if cave in c]

    # Recursively visit all neighbouring big and unvisited small caves
    return sum(
        number_of_paths(n, current_path)
        for n in neighbours
        if n.isupper() or n not in current_path
    )


with open("input", "r") as file:
    connections = [set(line.strip().split("-")) for line in file.readlines()]

print("number of paths through the cave system: %i" % number_of_paths())
