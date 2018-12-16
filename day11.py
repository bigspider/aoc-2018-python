import sys
from collections import defaultdict
import itertools

sn = int(input())

grid = defaultdict(int)
grid_sum = defaultdict(int)  # prefix sum

# find the sum of any subrectangle in O(1), given the prefix sum
def sum_rect(prefix_sum, a, b, c, d):
	return prefix_sum[(c, d)] - prefix_sum[(a - 1, d)] - prefix_sum[(c, b - 1)] + prefix_sum[(a - 1, b - 1)]

for x in range(1, 301):
	for y in range(1, 301):
		rackID = x + 10
		pl = ((rackID * y) + sn) * rackID
		pl = int(pl/100) % 10 - 5
		grid[(x, y)] = pl

for x in range(1, 301):
	for y in range(1, 301):
		grid_sum[(x, y)] = grid_sum[(x-1, y)] + grid_sum[(x, y-1)] - grid_sum[(x-1, y-1)] + grid[(x, y)]


# Some functional fun :P
res_x, res_y = max(itertools.product(range(1, 299), repeat=2), key=lambda point: sum_rect(grid_sum, point[0], point[1], point[0]+2, point[1]+2))
print("%s,%s" % (res_x, res_y))

best_sum = -float("inf")
best_triple = None
for size in range(1, 300):
	for x in range(1, 301 - size):
		for y in range(1, 301 - size):
			s = sum_rect(grid_sum, x, y, x+size-1, y+size-1)
			if s > best_sum:
				best_sum = s
				best_triple = (x, y, size)

print("%s,%s,%s" % best_triple)
