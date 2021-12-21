#!/usr/bin/python
# SPDX-License-Identifier: MIT

import itertools
import re
from functools import cache

WINNING_SCORE = 21

starting_spaces = [None, None]
with open("input", "r") as file:
    for player in range(2):
        match = re.fullmatch(
            r"Player (\d) starting position: (\d+)", file.readline().strip()
        )
        assert int(match.group(1)) == player + 1
        starting_spaces[player] = int(match.group(2))
starting_spaces = tuple(starting_spaces)

# Returns in how many universes each player wins if they are at their current
# positions and scores if it is the first player's turn
@cache
def winning_games(positions, scores=(0, 0)):
    assert max(scores) < WINNING_SCORE

    winning = (0, 0)
    # Summing up the dice and iterating over the sum (from 3 to 9), multiplying
    # the won games by the time these sums can appear (1,3,6,7,6,3,1), makes it
    # possible to run the recursion in a couple of seconds even without
    # memoisation. However since we are using functools.cache, the program
    # returns almost instantly anyway.
    for dice in itertools.product(range(1, 4), repeat=3):
        position_new = positions[0] + sum(dice)
        if position_new % 10 == 0:
            position_new = 10
        else:
            position_new %= 10
        positions_new = (position_new, positions[1])
        scores_new = (scores[0] + positions_new[0], scores[1])

        if scores_new[0] >= WINNING_SCORE:
            winning = (winning[0] + 1, winning[1])
        else:
            # Switch the first and second player because it is now the other
            # player's turn
            won = winning_games(positions_new[::-1], scores_new[::-1])
            winning = (winning[0] + won[1], winning[1] + won[0])

    return winning


print(
    "number of games won by the most successful player: %i"
    % max(winning_games(starting_spaces))
)
