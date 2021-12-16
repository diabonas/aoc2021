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

    if any(current_path.count(c) > 1 for c in current_path if c.islower()):
        # We have already visited a small cave twice, so only visit neighbours
        # that are big or not in the current path yet
        return sum(
            number_of_paths(n, current_path)
            for n in neighbours
            if n.isupper() or n not in current_path
        )
    else:
        # No small cave has been visited twice yet, we can go everywhere except
        # back to "start"
        return sum(number_of_paths(n, current_path) for n in neighbours if n != "start")


with open("input", "r") as file:
    connections = [set(line.strip().split("-")) for line in file.readlines()]

print("number of paths through the cave system: %i" % number_of_paths())
