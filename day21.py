import sys

def addr(params, status):
	A, B, C = params
	result = status.copy()
	result[C] = status[A] + status[B]
	return result

def addi(params, status):
	A, B, C = params
	result = status.copy()
	result[C] = status[A] + B
	return result

def mulr(params, status):
	A, B, C = params
	result = status.copy()
	result[C] = status[A] * status[B]
	return result

def muli(params, status):
	A, B, C = params
	result = status.copy()
	result[C] = status[A] * B
	return result

def banr(params, status):
	A, B, C = params
	result = status.copy()
	result[C] = status[A] & status[B]
	return result

def bani(params, status):
	A, B, C = params
	result = status.copy()
	result[C] = status[A] & B
	return result

def borr(params, status):
	A, B, C = params
	result = status.copy()
	result[C] = status[A] | status[B]
	return result

def bori(params, status):
	A, B, C = params
	result = status.copy()
	result[C] = status[A] | B
	return result

def setr(params, status):
	A, B, C = params
	result = status.copy()
	result[C] = status[A]
	return result

def seti(params, status):
	A, B, C = params
	result = status.copy()
	result[C] = A
	return result

def gtir(params, status):
	A, B, C = params
	result = status.copy()
	result[C] = 1 if A > status[B] else 0
	return result

def gtri(params, status):
	A, B, C = params
	result = status.copy()
	result[C] = 1 if status[A] > B else 0
	return result

def gtrr(params, status):
	A, B, C = params
	result = status.copy()
	result[C] = 1 if status[A] > status[B] else 0
	return result

def eqir(params, status):
	A, B, C = params
	result = status.copy()
	result[C] = 1 if A == status[B] else 0
	return result

def eqri(params, status):
	A, B, C = params
	result = status.copy()
	result[C] = 1 if status[A] == B else 0
	return result

def eqrr(params, status):
	A, B, C = params
	result = status.copy()
	result[C] = 1 if status[A] == status[B] else 0
	return result



# Additional istruction

def shri(params, status):
	A, B, C = params
	result = status.copy()
	result[C] = status[A] >> B
	return result


instructions = {
	"addr": addr, "addi": addi, "mulr": mulr, "muli": muli, "banr": banr, "bani": bani,
	"borr": borr, "bori": bori, "setr": setr, "seti": seti, "gtir": gtir, "gtri": gtri,
	"gtrr": gtrr, "eqir": eqir, "eqri": eqri, "eqrr": eqrr,
	"shri": shri  # ADDED INSTRUCTION 
}

inp = sys.stdin.readlines()

ip_index = int(inp[0].split(" ")[1])

program = []
for line in inp[1:]:
	parts = line.split(" ")
	params = [int(x) for x in parts[1:]]
	program.append((parts[0], params))

registers = [0, 0, 0, 0, 0, 0]


# Optimize the program using the new shri instruction (not needed for part 1)
# See input21-annotated.in for explanation. It makes the program thousands of times faster,
# and that's enough.
program[17] = ("shri", [3, 8, 3])
program[18] = ("seti", [7, 0, 1])

# Interpreter never halts, it prints all the values that would make the input program halt.
# First and last value before halting are the answers to part1 and part2.

halting_values = set()
while True:
	ip = registers[ip_index]
	
	if ip < 0 or ip >= len(program):
		break
	
	if ip == 28 and registers[4] not in halting_values:
		print(registers[4], end=" ")
		sys.stdout.flush()
		halting_values.add(registers[4])
	
	instr_name, params = program[ip]
	registers = instructions[instr_name](params, registers)		
	registers[ip_index] += 1
