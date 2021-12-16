#!/usr/bin/python
# SPDX-License-Identifier: MIT

from math import prod


def parse_packets(message):
    packet = {
        "version": int(message[:3], 2),
        "type": int(message[3:6], 2),
        "length": 0,
        "subpackets": [],
    }

    if packet["type"] == 4:  # literal value packet
        value = ""
        packet["length"] = 3 + 3  # version, type ID
        while True:
            value += message[packet["length"] + 1 : packet["length"] + 5]
            packet["length"] += 5
            if message[packet["length"] - 5] == "0":
                break
        packet["value"] = int(value, 2)
    else:  # operator packet
        length_type_id = message[6]
        match length_type_id:
            case "0":
                HEADER_LENGTH = 3 + 3 + 1 + 15  # version, type ID, length type ID, length
                total_subpacket_length = int(message[7:HEADER_LENGTH], 2)
                packet["length"] = HEADER_LENGTH
                while packet["length"] != HEADER_LENGTH + total_subpacket_length:
                    subpacket = parse_packets(message[packet["length"] :])
                    packet["subpackets"].append(subpacket)
                    packet["length"] += subpacket["length"]
            case "1":
                HEADER_LENGTH = 3 + 3 + 1 + 11  # version type ID, length type ID, length
                num_subpackets = int(message[7:HEADER_LENGTH], 2)
                packet["length"] = HEADER_LENGTH
                for s in range(num_subpackets):
                    subpacket = parse_packets(message[packet["length"] :])
                    packet["subpackets"].append(subpacket)
                    packet["length"] += subpacket["length"]
            case _:
                raise Exception("unknown length type ID", length_type_id)

    return packet


def sum_version_numbers(packet):
    return packet["version"] + sum(sum_version_numbers(p) for p in packet["subpackets"])


with open("input", "r") as file:
    # Prepend a 1 to make sure not to lose any leading zeros in the conversion,
    # e.g. in the "620080001611562C8802118E34" example
    message = bin(int("1" + file.readline(), 16))[3:]

packets = parse_packets(message)

print("sum of all version numbers: %i" % sum_version_numbers(packets))
