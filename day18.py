import sys

def evaluate(scan):
	final_trees = sum(row.count("|") for row in scan)
	final_lumber = sum(row.count("#") for row in scan)
	return final_trees * final_lumber

def encode(scan):
	return "".join(["".join(row) for row in scan])

def process(scan):
	width = len(scan[0])
	height = len(scan)
	scan_copy = [list(row) for row in scan]
	
	for y, row in enumerate(scan):
		for x, cell in enumerate(row):
			count_open = 0
			count_trees = 0
			count_lumber = 0
			for j in range(max(0, y - 1), 1 + min(height - 1, y + 1)):
				for i in range(max(0, x - 1), 1 + min(width - 1, x + 1)):
					if (i, j) != (x, y):
						if scan_copy[j][i] == ".":
							count_open += 1
						elif scan_copy[j][i] == "|":
							count_trees += 1
						else: # if scan_copy[j][i] == "#"
							count_lumber += 1
			if scan_copy[y][x] == ".":
				if count_trees >= 3:
					scan[y][x] = "|"
			elif scan_copy[y][x] == "|":
				if count_lumber >= 3:
					scan[y][x] = "#"				
			elif scan_copy[y][x] == "#":
				if count_lumber == 0 or count_trees == 0:
					scan[y][x] = "."


scan = [list(line.strip()) for line in sys.stdin.readlines()]

seen = {}  # record the index when a configuration was first found
values = [] # list of resource values
TARGET = 1000000000
for i in range(TARGET):
	process(scan)
	values.append(evaluate(scan))
	
	if i == 10-1:
		print(values[-1])  # PART 1
	
	code = encode(scan)
	
	if code in seen:
		# Found the period, shortcut computation
		first = seen[code]
		period = i - first
		print(values[first + (TARGET-1 - first) % period]) # PART 2
		break
	
	seen[code] = i

