#!/usr/bin/python
# SPDX-License-Identifier: MIT

import itertools

STEPS = 10

with open("input", "r") as file:
    template = file.readline().strip()
    assert file.readline() == "\n"
    rules = {pair: new for pair, new in (line.strip().split(" -> ") for line in file)}

# Collect all polymers that occur anywhere in the template or the rules
polymers = set(template) | set(p for rule in rules for p in rule) | set(rules.values())

# The rules should be complete and specifiy an insertion for every possible
# combination of polymers
assert all(p[0] + p[1] in rules for p in itertools.product(polymers, repeat=2))

# Instead of storing the whole huge string, we count how many times each pair
# occurs per step
pairs = {rule: 0 for rule in rules}
for pair in itertools.pairwise(template):
    pairs["".join(pair)] += 1

for step in range(STEPS):
    pairs_next = {rule: 0 for rule in rules}
    # For each existing pair, insert the new polymer in the middle to create
    # two new pairs
    for pair in pairs:
        pairs_next[pair[0] + rules[pair]] += pairs[pair]
        pairs_next[rules[pair] + pair[1]] += pairs[pair]
    pairs = pairs_next

# To count the number of polymers, look how many pairs containing the polymer
# exist. Pairs containing the same polymer twice are counted twice.
counts = {
    polymer: sum(pairs[p] * p.count(polymer) for p in pairs) for polymer in polymers
}
# The polymers at the beginning and the end never change and are only counted
# as part of one pair, increase their count to make them consistent with the
# others
counts[template[0]] += 1
counts[template[-1]] += 1
# Now we have double-counted every polymer, divide by 2 to get the final answer
counts = {polymer: counts[polymer] // 2 for polymer in polymers}

most_common = max(counts[polymer] for polymer in polymers)
least_common = min(counts[polymer] for polymer in polymers)
difference = most_common - least_common

print(
    f"difference between the quantities of the most and least common element: {difference}"
)
