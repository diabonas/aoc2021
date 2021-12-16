#!/usr/bin/python
# SPDX-License-Identifier: MIT

import sys


def mark(board, number):
    for row in board:
        for column in row:
            if column["number"] == number:
                column["marked"] = True


def isbingo(board):
    for row in board:
        if all(column["marked"] for column in row):
            return True

    for y in range(len(board[0])):
        column = [row[y] for row in board]
        if all(row["marked"] for row in column):
            return True

    return False


with open("input", "r") as file:
    drawn = list(map(int, file.readline().split(",")))
    boards = []
    while file.readline() == "\n":
        boards.append(
            [
                [{"number": int(n), "marked": False} for n in line.split()]
                for line in (file.readline() for i in range(5))
            ]
        )

for called in drawn:
    for board in boards:
        mark(board, called)
        if isbingo(board):
            unmarked = sum(
                x["number"] for y in board for x in y if x["marked"] is False
            )
            score = unmarked * called
            print(f"final score of the first winning board: {score}")
            sys.exit()
