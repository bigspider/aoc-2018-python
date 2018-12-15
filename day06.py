import sys

def manh(p1, p2):
	return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

inp = [list(map(int, line.split(", "))) for line in sys.stdin.readlines() if "," in line]

max_x = max(point[0] for point in inp)
max_y = max(point[1] for point in inp)

grid = [[None] * (max_y + 1) for i in range(max_x + 1)]

counts = [0] * len(inp)

safe_count = 0

for x in range(max_x + 1):
	for y in range(max_y + 1):
		min_dist = float("inf")
		min_count = 0
		min_idx = None
		
		total_manh_distance = 0
		
		for idx, point in enumerate(inp):
			dist = manh((x, y), point)
			total_manh_distance += dist
			if dist < min_dist:
				min_dist = dist
				min_count = 1
				min_idx = idx
			elif dist == min_dist:
				min_count += 1
		
		if min_count == 1:
			grid[x][y] = min_idx
			counts[min_idx] += 1
		
		if total_manh_distance < 10000:
			safe_count += 1


# Input coordinates have infinite area if they "dominate" a border point
border_points = [(x, 0) for x in range(0, max_x + 1)] +\
				[(x, max_y) for x in range(0, max_x + 1)] +\
				[(0, y) for y in range(1, max_y + 1)] +\
				[(max_x, y) for y in range(1, max_y + 1)]

for x, y in border_points:
	i = grid[x][y]
	if i is not None:
		counts[i] = -1

print(max(counts))
print(safe_count)
