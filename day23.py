import sys
import re
from random import randint

def manh_dist(point1, point2):
	return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1]) + abs(point1[2] - point2[2])

# returns the 8 corners of the cube of coordinates in range for the bot 
def corners(bot):
	r = bot[3]
	res = []
		
	for dx in [-r, r]:
		for dy in [-r, r]:
			for dz in [-r, r]:
				res.append((bot[0]+dx, bot[1]+dy, bot[2]+dz))
	return res

pattern = re.compile(r"^pos=<([-]?\d+),([-]?\d+),([-]?\d+)>, r=(\d+)$")
nanobots = []

for line in sys.stdin.readlines():
	x, y, z, r = map(int, pattern.match(line.strip()).groups())
	nanobots.append((x, y, z, r))

max_r_bot = max(nanobots, key=lambda bot: bot[3])
print(len([bot for bot in nanobots if manh_dist(max_r_bot, bot) <= max_r_bot[3]]))

all_corners = set().union([(0, 0, 0)], *[corners(bot) for bot in nanobots])
best_coverage = -1
best_dist = None
best_p = None

# Find initial decent solution
for p in all_corners:
	coverage = len([bot for bot in nanobots if manh_dist(p, bot) <= bot[3]])
	dist = manh_dist(p, (0, 0, 0))
	if coverage > best_coverage or (coverage == best_coverage and dist < best_dist):
		best_coverage = coverage
		best_p = p
		best_dist = manh_dist(p, (0, 0, 0))
		print(best_coverage)
		print("%d,%d,%d" % best_p)
		print(best_dist)

print("Starting local search")

# improve it with local search/annealing
max_displacement = 1 << 20
no_improvement_count = 0
while True:
	if no_improvement_count > 10000:
		no_improvement_count = 0
		max_displacement /= 2
		if max_displacement < 1:
			break

	dx = randint(-max_displacement, max_displacement)
	dy = randint(-max_displacement, max_displacement)
	dz = randint(-max_displacement, max_displacement)
	p = (best_p[0]+dx, best_p[1]+dy, best_p[2]+dz)
	coverage = len([bot for bot in nanobots if manh_dist(p, bot) <= bot[3]])
	dist = manh_dist(p, (0, 0, 0))
	if coverage > best_coverage or (coverage == best_coverage and dist < best_dist) or (coverage == best_coverage and dist == best_dist and p < best_p):
		best_coverage = coverage
		best_p = p
		best_dist = manh_dist(p, (0, 0, 0))
		print(best_coverage)
		print("%d,%d,%d" % best_p)
		print(best_dist)
		no_improvement_count = 0
	
	no_improvement_count += 1
