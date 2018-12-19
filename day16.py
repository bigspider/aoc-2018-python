import sys
import time

inp = sys.stdin.readlines()

def addr(opcodes, status):
	A, B, C = opcodes[1:]
	result = status.copy()
	result[C] = status[A] + status[B]
	return result

def addi(opcodes, status):
	A, B, C = opcodes[1:]
	result = status.copy()
	result[C] = status[A] + B
	return result

def mulr(opcodes, status):
	A, B, C = opcodes[1:]
	result = status.copy()
	result[C] = status[A] * status[B]
	return result

def muli(opcodes, status):
	A, B, C = opcodes[1:]
	result = status.copy()
	result[C] = status[A] * B
	return result

def banr(opcodes, status):
	A, B, C = opcodes[1:]
	result = status.copy()
	result[C] = status[A] & status[B]
	return result

def bani(opcodes, status):
	A, B, C = opcodes[1:]
	result = status.copy()
	result[C] = status[A] & B
	return result

def borr(opcodes, status):
	A, B, C = opcodes[1:]
	result = status.copy()
	result[C] = status[A] | status[B]
	return result

def bori(opcodes, status):
	A, B, C = opcodes[1:]
	result = status.copy()
	result[C] = status[A] | B
	return result

def setr(opcodes, status):
	A, B, C = opcodes[1:]
	result = status.copy()
	result[C] = status[A]
	return result

def seti(opcodes, status):
	A, B, C = opcodes[1:]
	result = status.copy()
	result[C] = A
	return result

def gtir(opcodes, status):
	A, B, C = opcodes[1:]
	result = status.copy()
	result[C] = 1 if A > status[B] else 0
	return result

def gtri(opcodes, status):
	A, B, C = opcodes[1:]
	result = status.copy()
	result[C] = 1 if status[A] > B else 0
	return result

def gtrr(opcodes, status):
	A, B, C = opcodes[1:]
	result = status.copy()
	result[C] = 1 if status[A] > status[B] else 0
	return result

def eqir(opcodes, status):
	A, B, C = opcodes[1:]
	result = status.copy()
	result[C] = 1 if A == status[B] else 0
	return result

def eqri(opcodes, status):
	A, B, C = opcodes[1:]
	result = status.copy()
	result[C] = 1 if status[A] == B else 0
	return result

def eqrr(opcodes, status):
	A, B, C = opcodes[1:]
	result = status.copy()
	result[C] = 1 if status[A] == status[B] else 0
	return result


instructions = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]

decoder = {}

samples = []
i = 0
while inp[i].startswith("Before"):
	status_before = list(map(int, inp[i].replace("[", ",").replace("]", ",").split(",")[1:5]))
	opcodes = list(map(int, inp[i+1].split(" ")))
	status_after = list(map(int, inp[i+2].replace("[", ",").replace("]", ",").split(",")[1:5]))
	samples.append((status_before, opcodes, status_after))
	i += 4

program = [list(map(int, line.split(" "))) for line in inp[i+2:]]

# PART 1

count_part1 = 0
for sample in samples:
	status_before, opcodes, status_after = sample
	candidates = set(filter(lambda instr: instr(opcodes, status_before) == status_after, instructions))
	if len(candidates) >= 3:
		count_part1 += 1

print(count_part1)

# PART 2

while True:
	unknown_opcodes = { sample[1][0] for sample in samples }.difference(decoder.keys())
	
	if len(unknown_opcodes) == 0:
		break

	# For each unknown opcode, we check if any of the unused instructions is valid for _all_ samples with that opcode
	for code in unknown_opcodes:
		candidates = set(instructions).difference(decoder.values())
		for sample in filter(lambda s: s[1][0] == code, samples):
			status_before, opcodes, status_after = sample
			removed_candidates = { instr for instr in candidates if instr(opcodes, status_before) != status_after }
			candidates.difference_update(removed_candidates)
			
		if len(candidates) == 1:
			decoder[opcodes[0]] = candidates.pop()

status = [0] * 4
for opcodes in program:
	status = decoder[opcodes[0]](opcodes, status)

print(status[0])
