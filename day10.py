import sys
from collections import defaultdict

class Point:
	def __init__(self, x, y, vx, vy):
		self.x = x
		self.y = y
		self.vx = vx
		self.vy = vy
	def move(self):
		self.x += self.vx
		self.y += self.vy

points = []
sky = defaultdict(lambda: 0)  # pair of coordinates to # of points
for line in sys.stdin.readlines():
	parts = line.replace("<", ">").split(">")
	x, y = [int(t) for t in parts[1].split(",")]
	vx, vy = [int(t) for t in parts[3].split(",")]
	points.append(Point(x, y, vx, vy))
	sky[(x, y)] += 1

n_seconds = 0
while True:
	#count the number of points that are not adjacent to any point
	n_lonely = 0
	for p in points:
		x = p.x
		y = p.y
		if sky[(x-1, y-1)] + sky[(x, y-1)] + sky[(x+1, y-1)] + sky[(x-1, y)] + sky[(x+1, y)] + sky[(x-1, y+1)] + sky[(x, y+1)] + sky[(x+1, y+1)] == 0:
			n_lonely += 1

	if n_lonely == 0:
		break  # no lonely points, it's probably the right time!
	
	for p in points:
		sky[(p.x, p.y)] -= 1
		if sky[(p.x, p.y)] == 0:
			del sky[(p.x, p.y)]  # make sure we free up unused memory
		p.move()
		sky[(p.x, p.y)] += 1

	n_seconds += 1


# Find bounding box
min_x = float("inf")
max_x = -float("inf")
min_y = float("inf")
max_y = -float("inf")
for p in points:
	min_x = min(min_x, p.x)
	max_x = max(max_x, p.x)
	min_y = min(min_y, p.y)
	max_y = max(max_y, p.y)

for y in range(min_y, max_y + 1):
	for x in range(min_x, max_x + 1):
		if  sky[(x, y)] > 0: 
			print("#", end="")
		else:
			print(".", end="")
	print()

print("Waited %s seconds" % n_seconds) 
