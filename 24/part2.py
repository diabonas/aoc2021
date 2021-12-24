#!/usr/bin/python
# SPDX-License-Identifier: MIT


def parse_line(line):
    line = line.split()
    assert line[0] in ["inp", "add", "mul", "div", "mod", "eql"]
    if line[0] == "inp":
        assert len(line) == 2
    else:
        assert len(line) == 3
    return {
        "instruction": line[0],
        "operands": [o if o in ["w", "x", "y", "z"] else int(o) for o in line[1:]],
    }


def run_program(program, inputs):
    inputs = inputs.copy()
    variables = {"w": 0, "x": 0, "y": 0, "z": 0}
    for instruction in program:
        if instruction["instruction"] == "inp":
            assert len(instruction["operands"]) == 1
            assert instruction["operands"][0] in variables
            assert len(inputs) > 0
            variables[instruction["operands"][0]] = inputs.pop(0)
        else:
            assert len(instruction["operands"]) == 2
            assert instruction["operands"][0] in variables
            operands = [
                variables[o] if o in variables else o for o in instruction["operands"]
            ]
            match instruction["instruction"]:
                case "add":
                    variables[instruction["operands"][0]] = operands[0] + operands[1]
                case "mul":
                    variables[instruction["operands"][0]] = operands[0] * operands[1]
                case "div":
                    assert operands[1] != 0
                    variables[instruction["operands"][0]] = int(
                        operands[0] / operands[1]
                    )
                case "mod":
                    assert operands[0] >= 0
                    assert operands[1] > 0
                    variables[instruction["operands"][0]] = operands[0] % operands[1]
                case "eql":
                    variables[instruction["operands"][0]] = int(
                        operands[0] == operands[1]
                    )
                case _:
                    raise Exception("unknown instruction", instruction)
    return variables


with open("input", "r") as file:
    program = list(map(parse_line, file))

# The number of possible model numbers is too large to feasibly brute-force the
# problem and the problem is too hard to analytically solve for general
# programs. However, the input programs have a very particular structure that
# can be exploited to solve the problem. Check that the input actually has the
# expected form.
assert len(program) == 14 * 18
assert all(i == {"instruction": "inp", "operands": ["w"]} for i in program[::18])
assert all(i == {"instruction": "mul", "operands": ["x", 0]} for i in program[1::18])
assert all(i == {"instruction": "add", "operands": ["x", "z"]} for i in program[2::18])
assert all(i == {"instruction": "mod", "operands": ["x", 26]} for i in program[3::18])
assert all(
    i["instruction"] == "div" and i["operands"][0] == "z" for i in program[4::18]
)
assert all(
    i["instruction"] == "add" and i["operands"][0] == "x" for i in program[5::18]
)
assert all(i == {"instruction": "eql", "operands": ["x", "w"]} for i in program[6::18])
assert all(i == {"instruction": "eql", "operands": ["x", 0]} for i in program[7::18])
assert all(i == {"instruction": "mul", "operands": ["y", 0]} for i in program[8::18])
assert all(i == {"instruction": "add", "operands": ["y", 25]} for i in program[9::18])
assert all(i == {"instruction": "mul", "operands": ["y", "x"]} for i in program[10::18])
assert all(i == {"instruction": "add", "operands": ["y", 1]} for i in program[11::18])
assert all(i == {"instruction": "mul", "operands": ["z", "y"]} for i in program[12::18])
assert all(i == {"instruction": "mul", "operands": ["y", 0]} for i in program[13::18])
assert all(i == {"instruction": "add", "operands": ["y", "w"]} for i in program[14::18])
assert all(
    i["instruction"] == "add" and i["operands"][0] == "y" for i in program[15::18]
)
assert all(i == {"instruction": "mul", "operands": ["y", "x"]} for i in program[16::18])
assert all(i == {"instruction": "add", "operands": ["z", "y"]} for i in program[17::18])

# These coefficients are the only varying parts of the input
divisors_z = [i["operands"][1] for i in program[4::18]]
offset_x = [i["operands"][1] for i in program[5::18]]
offset_d = [i["operands"][1] for i in program[15::18]]

assert all(d in [1, 26] for d in divisors_z)
assert all(offset_x[pos] < 0 for pos in range(len(offset_x)) if divisors_z[pos] == 26)

# These are the calculations that the program makes condensed into a single
# function
def calculate_z(model_number):
    x = z = 0
    for pos, digit in enumerate(model_number):
        x = int((z % 26 + offset_x[pos]) != digit)
        z = z // divisors_z[pos] * (25 * x + 1) + (digit + offset_d[pos]) * x
    return z


# From the structure of the above function, we obtain that valid model_number numbers
# have pairs of matching digits that differ by a constant offset
constraints = []
matching_digits = []
for pos, divisor in enumerate(divisors_z):
    if divisor == 1:
        matching_digits.append(pos)
    else:
        pair = (matching_digits.pop(), pos)
        difference = offset_d[pair[0]] + offset_x[pair[1]]
        constraints.append((pair, difference))
assert len(matching_digits) == 0

# Make the most significant digits as small as possible while fulfilling the
# calculated constraints
model_number = [1] * 14
for pair, difference in constraints:
    if difference > 0:
        model_number[pair[1]] = model_number[pair[0]] + difference
    else:
        model_number[pair[0]] = model_number[pair[1]] - difference

assert all(digit in range(1, 10) for digit in model_number)
assert run_program(program, model_number)["z"] == 0
assert calculate_z(model_number) == 0

model_number = "".join(str(digit) for digit in model_number)

print(f"smallest valid model number: {model_number}")
