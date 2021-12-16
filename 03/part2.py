#!/usr/bin/python
# SPDX-License-Identifier: MIT

with open("input", "r") as file:
    diagnostics = [line.strip() for line in file]

ratings = {"oxygen": diagnostics, "co2": diagnostics}
for rating in ratings:
    for i in range(len(diagnostics[0])):
        bits = [d[i] for d in ratings[rating]]
        if bits.count("1") >= bits.count("0"):
            most_common = "1"
            least_common = "0"
        else:
            most_common = "0"
            least_common = "1"

        if rating == "oxygen":
            keep = most_common
        else:
            keep = least_common

        ratings[rating] = [d for d in ratings[rating] if d[i] == keep]

        if len(ratings[rating]) == 1:
            ratings[rating] = int(ratings[rating].pop(), 2)
            break

life_support_rating = ratings["oxygen"] * ratings["co2"]

print(f"life support rating: {life_support_rating}")
