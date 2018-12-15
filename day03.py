import sys

SIZE = 1000

grid = [[0] * SIZE for i in range(SIZE)]

claims = []

for line in sys.stdin.readlines():
	_, rect = line.split(" @ ")
	coords, size = rect.split(": ")
	x, y = map(lambda t: int(t) - 1, coords.split(","))
	w, h = map(int, size.split("x"))
	
	claims.append((x, y, w, h))


for claim in claims:
	x, y, w, h = claim
	
	for i in range(x, x+w):
		for j in range(y, y+h):
			grid[i][j] += 1

res1 = 0
for i in range(0, SIZE):
	for j in range(0, SIZE):
		if grid[i][j] >= 2:
			res1 += 1

print(res1)


for ID, claim in enumerate(claims):
	x, y, w, h = claim
	
	intact = True
	for i in range(x, x+w):
		for j in range(y, y+h):
			if grid[i][j] != 1:
				intact = False
	
	if intact:
		print(ID + 1)
