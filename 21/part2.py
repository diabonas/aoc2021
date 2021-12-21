#!/usr/bin/python
# SPDX-License-Identifier: MIT

import itertools
import re

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

won_games = {}
# Returns in how many universes each player wins if they are at their current
# positions and scores if it is the first player's turn
def winning_games(positions, scores=(0, 0)):
    assert max(scores) < WINNING_SCORE

    winning = (0, 0)
    for dice in itertools.product(range(1, 4), repeat=3):
        position_new = positions[0] + sum(dice)
        if position_new % 10 == 0:
            position_new = 10
        else:
            position_new %= 10
        positions_new = (position_new, positions[1])
        scores_new = (scores[0] + positions_new[0], scores[1])

        if scores_new[0] >= 21:
            winning = (winning[0] + 1, winning[1])
        else:
            # Switch the first and second player because it is now the other
            # player's turn
            new_situation = (positions_new[::-1], scores_new[::-1])
            if new_situation not in won_games:
                won_games[new_situation] = winning_games(*new_situation)
            winning = (
                winning[0] + won_games[new_situation][1],
                winning[1] + won_games[new_situation][0],
            )

    return winning


print(
    "number of won games by the most successful player: %i"
    % max(winning_games(starting_spaces))
)
