#!/usr/bin/python
# SPDX-License-Identifier: MIT

with open("input", "r") as file:
    diagnostics = [line.strip() for line in file]

rates = {"gamma": "", "epsilon": ""}
for i in range(len(diagnostics[0])):
    bits = [d[i] for d in diagnostics]
    assert bits.count("0") != bits.count("1")
    if bits.count("1") > bits.count("0"):
        most_common = "1"
        least_common = "0"
    else:
        most_common = "0"
        least_common = "1"

    rates["gamma"] += most_common
    rates["epsilon"] += least_common

rates = {rate: int(rates[rate], 2) for rate in rates}

power_consumption = rates["gamma"] * rates["epsilon"]

print(f"power consumption: {power_consumption}")
