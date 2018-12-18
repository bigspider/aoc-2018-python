# Code is ugly, unoptimized, and bad in many ways... but I had enough of this problem :)

import sys
from collections import deque

class Cell:
	def __init__(self, cell_type, hit_points=200):
		self.type = cell_type
		self.hit_points = hit_points


def print_grid(g):
	for line in g:
		for cell in line:
			print(cell.type, end="")
		print()

def neighbors(x, y):
	return[(x, y-1), (x-1, y), (x+1, y), (x, y+1)]

# returns a grid dist of the same size as g, where res[y][x] is the shortest path
# length between src and (x, y) in g, considering only "." as walkable. BFS from src.
def all_distances(g, src):
	width = len(g[0])
	height = len(g)
	src_x, src_y = src
	dist = [[float('inf')] * height for _ in range(width)]
	dist[src_y][src_x] = 0
	
	Q = deque([src])
	
	while(len(Q) > 0):
		node_x, node_y = Q.popleft()
		
		for x, y in neighbors(node_x, node_y):
			if g[y][x].type == ".":
				if dist[y][x] == float('inf'):
					Q.append((x, y))

				dist[y][x] = min(dist[y][x], dist[node_y][node_x] + 1)

	return dist

inp = sys.stdin.readlines()


def battle(inp, elf_power = 3, stop_if_elf_dies=False):
	width = len(inp[0].strip())
	height = len(inp)

	grid = [[None]*height for _ in range(width)]

	for row, line in enumerate(inp):
		for col, cell in enumerate(line.strip()):
			grid[row][col] = Cell(cell)


	all_elves_survived = True

	n_rounds = 0
	while True:
		active_unit_coords = []
		for y in range(height):
			for x in range(width):
				if grid[y][x].type in "GE":
					active_unit_coords.append((x, y))

		should_continue = False  # stop unless at least one movement or attack happened
		for unit_x, unit_y in active_unit_coords:
			if grid[unit_y][unit_x].type not in "GE":
				continue  # a unit was here, but was already killed previously in this round
			
			unit = grid[unit_y][unit_x]
			unit_type = grid[unit_y][unit_x].type
			opposite_type = "G" if unit_type == "E" else "E"
			
			opponents = [(x, y) for x in range(width) for y in range(height) if grid[y][x].type == opposite_type]
			
			if len(opponents) == 0: # no opponents, premature end
				should_continue = False
				break
			
			# all points in range of any opponent (including himself and invalid ones)
			all_points_in_range = set().union(*[neighbors(*opp) for opp in opponents])
			valid_points_in_range = set([p for p in all_points_in_range if grid[p[1]][p[0]].type == '.' or p == (unit_x, unit_y)])
			
			if len(valid_points_in_range) == 0:
				continue
			
			if (unit_x, unit_y) not in valid_points_in_range: # do not move if a target is already in range
				# Opponent not in range, try to get closer
				dist_from_unit = all_distances(grid, (unit_x, unit_y))
				
				nearest_distance = min(dist_from_unit[p[1]][p[0]] for p in valid_points_in_range)
				if nearest_distance != float("inf"):
					nearest_in_range = min(valid_points_in_range, key=lambda p: (dist_from_unit[p[1]][p[0]], p[1], p[0]))
					
					#print(f"Nearest target in range for {unit.type}({unit_x},{unit_y}) is {nearest_in_range[0]}, {nearest_in_range[1]}")
					
					dist_from_dest = all_distances(grid, nearest_in_range)
					next_position = min(neighbors(unit_x, unit_y), key=lambda p: (dist_from_dest[p[1]][p[0]], p[1], p[0]))
					
					# Do the move
					grid[next_position[1]][next_position[0]] = unit
					grid[unit_y][unit_x] = Cell(".")
					
					unit_x, unit_y = next_position
					
					should_continue = True


			# ATTAAAACK
			targets = {p for p in neighbors(unit_x, unit_y) if grid[p[1]][p[0]].type == opposite_type}
			if len(targets) > 0:
				chosen_target_coords = min(targets, key=lambda p: (grid[p[1]][p[0]].hit_points, p[1], p[0]))
				chosen_target = grid[chosen_target_coords[1]][chosen_target_coords[0]]
				
				hit_power = 3 if unit.type == "G" else elf_power
				chosen_target.hit_points -= hit_power
				
				#print(f"Unit {unit.type}({unit_x},{unit_y}) attacking {chosen_target_coords[0]}, {chosen_target_coords[1]}")
				
				if chosen_target.hit_points <= 0:
					if chosen_target.type == "E":
						all_elves_survived = False
						if stop_if_elf_dies:
							return None, None, False
					grid[chosen_target_coords[1]][chosen_target_coords[0]] = Cell('.')  # Unit killed
				
				should_continue = True
			
		#print_grid(grid)
			
		if not should_continue:
			break

		n_rounds += 1
	return grid, n_rounds, all_elves_survived


def outcome(grid, n_rounds):
	width = len(grid[0])
	height = len(grid)
	remaining_points = sum([grid[y][x].hit_points for x in range(width) for y in range(height) if grid[y][x].type in "GE"])
	return remaining_points * n_rounds


# PART 1

grid, n_rounds, _ = battle(inp)
print(outcome(grid, n_rounds))


# PART 2

# binary search on elf_power would be faster...
elf_power = 4
while True:
	grid, n_rounds, all_elves_survived = battle(inp, elf_power, True)
	if all_elves_survived:
		print(outcome(grid, n_rounds))
		break
	elf_power += 1
