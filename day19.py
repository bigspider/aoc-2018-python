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


def divisorsum(n):
    return sum(i for i in range(1, n+1) if n % i == 0)


instructions = {
	"addr": addr, "addi": addi, "mulr": mulr, "muli": muli, "banr": banr, "bani": bani,
	"borr": borr, "bori": bori, "setr": setr, "seti": seti, "gtir": gtir, "gtri": gtri,
	"gtrr": gtrr, "eqir": eqir, "eqri": eqri, "eqrr": eqrr
}

inp = sys.stdin.readlines()

ip_index = int(inp[0].split(" ")[1])

program = []
for line in inp[1:]:
	parts = line.split(" ")
	params = [int(x) for x in parts[1:]]
	program.append((parts[0], params))

registers = [0]*6
while True:
	ip = registers[ip_index]
	
	if ip < 0 or ip >= len(program):
		break
	
	instr_name, params = program[ip]
	
	registers = instructions[instr_name](params, registers)
	
	registers[ip_index] += 1

print(registers[0])


# PART 2: the input program computes a number in register #3, and then it
# (very inefficiently) computes its sum of divisors.
# The input number is ready when ip == 34, so we only run the program until then.

registers = [1, 0, 0, 0, 0, 0]
while True:
	ip = registers[ip_index]
	
	if ip == 34:
		break;
	
	instr_name, params = program[ip]
	
	registers = instructions[instr_name](params, registers)
		
	registers[ip_index] += 1

print(divisorsum(registers[3]))
