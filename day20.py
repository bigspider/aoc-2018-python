import sys

inp = input().strip()[1:-1]

d = { # direction vectors
	"N": (0, -1),
	"S": (0, 1),
	"W": (-1, 0),
	"E": (1, 0)
}

x = y = 0
pos = [(0, 0)]  # stack of positions, to keep track when nesting
dist = {(0, 0): 0}  # shortest distances for each room
max_dist = 0
for c in inp:
	if c in "NSWE":
		direction = d[c]
		prev_dist = dist[(x, y)]
		x += direction[0]
		y += direction[1]
		dist[(x, y)] = min(dist.get((x, y), float("inf")), prev_dist + 1)
		max_dist = max(max_dist, dist[(x, y)])
	elif c == "(":
		pos.append((x, y))
	elif c == "|":
		x, y = pos[-1]
	elif c == ")":
		pos.pop()
		x, y == pos[-1]

print(max_dist)
print(len([x for x in dist.values() if x >= 1000]))
