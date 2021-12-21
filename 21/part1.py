#!/usr/bin/python
# SPDX-License-Identifier: MIT

import re

WINNING_SCORE = 1000

starting_spaces = [None, None]
with open("input", "r") as file:
    for player in range(2):
        match = re.fullmatch(
            r"Player (\d) starting position: (\d+)", file.readline().strip()
        )
        assert int(match.group(1)) == player + 1
        starting_spaces[player] = int(match.group(2))
starting_spaces = tuple(starting_spaces)

spaces = list(starting_spaces)
scores = [0, 0]
rolled = 0
while max(scores) < WINNING_SCORE:
    for player in range(2):
        spaces[player] += 3 * (rolled + 2)
        if spaces[player] % 10 == 0:
            spaces[player] = 10
        else:
            spaces[player] %= 10
        scores[player] += spaces[player]
        rolled += 3
        if scores[player] >= WINNING_SCORE:
            break

print(
    "product of the score of the losing player and the number of dice rolls: %i"
    % (min(scores) * rolled)
)
