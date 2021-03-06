#!/usr/bin/python
# SPDX-License-Identifier: MIT

import numpy as np

STEPS = 50

with open("input", "r") as file:
    algorithm = file.readline().strip()
    assert len(algorithm) == 512
    assert file.readline() == "\n"
    input_image = np.array([list(line.strip()) for line in file])

# The value that the rest of the infinite image is filled with
infinite_value = "."

input_image = np.pad(input_image, 1, "constant", constant_values=infinite_value)
for step in range(STEPS):
    input_image = np.pad(input_image, 1, "constant", constant_values=infinite_value)
    output_image = np.copy(input_image)
    for row in range(1, len(input_image) - 1):
        for column in range(1, len(input_image[row]) - 1):
            number = np.concatenate(
                input_image[row - 1 : row + 2, column - 1 : column + 2]
            )
            number = "".join(number).replace(".", "0").replace("#", "1")
            number = int(number, 2)
            output_image[row][column] = algorithm[number]

    # In the rest of the infinite image, all pixels are surrounded by the same
    # of their kind, so they change to either algorithm[0] or algorithm[511]
    infinite_value = algorithm[
        int(infinite_value.replace(".", "0").replace("#", "1") * 9, 2)
    ]
    output_image[[0, -1], :] = infinite_value
    output_image[:, [0, -1]] = infinite_value

    input_image = output_image

# There should be only finitely many lit pixels after the last step
assert infinite_value == "."

print(
    "number of lit pixels in the output image: %i"
    % np.count_nonzero(output_image == "#")
)
