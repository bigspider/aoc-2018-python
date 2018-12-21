import sys
from collections import defaultdict

space = defaultdict(lambda: ".")

for line in sys.stdin.readlines():
	left, right = line.split(", ")
	first_coord = int(left.split("=")[1])
	second_range = right.split("=")[1]
	range_start, range_end = [int(x) for x in second_range.split("..")]
	if left[0] == 'x':
		for y in range(range_start, range_end+1):
			space[(first_coord, y)] = "#"
	else:
		for x in range(range_start, range_end+1):
			space[(x, first_coord)] = "#"

min_y = min(coord[1] for coord in space.keys())
max_y = max(coord[1] for coord in space.keys())

space[(500, 0)] = "+"

# Water types:
# |     flowing down (possibly empty below)
# H     cannot flow down, might flow left or right
# R     cannot flow down or left, might flow to the right 
# L     cannot flow down or right, might flow to the left
# ~     settled

active_cells = {(500, 0)}  # set of cells that need to be processed
while len(active_cells) > 0:
	x, y = active_cells.pop()  # make (x, y) inactive, unless a rule makes it active again

	def update(coords, val):
		global active_cells
		space[coords] = val
		x, y = coords
		# activate cells that might be affected by the update
		active_cells.update([(x, y), (x, y-1), (x-1, y), (x+1, y)])
	
	if y < max_y and space[(x, y)] in "|+":
		# Vertical rules: can water flow down?
		if space[(x, y+1)] == ".":
			update((x, y+1), "|")
		elif space[(x, y+1)] in "#~":
			update((x, y), "H")
	
	# HORIZONTAL RULES
	# water spreading horizontally
	if space[(x, y)] in "HLR":
		if space[(x+1, y)] == ".": 
			update((x+1, y), "|")
		if space[(x-1, y)] == ".":
			update((x-1, y), "|")

	# "settledness" of water spreads horizontally
	if space[(x, y)] in "HLR" and (space[(x-1, y)] == "~" or space[(x+1, y)] == "~"):
		update((x, y), "~")

	# water on flat chooses a direction if it finds a wall
	if space[(x, y)] == "H" and space[(x+1, y)] == "#":
		update((x, y), "L")
	if space[(x, y)] == "H" and space[(x-1, y)] == "#":
		update((x, y), "R")

	# direction infects other undecided water
	if space[(x, y)] == "R" and space[(x+1, y)] == "H":
		update((x+1, y), "R")
	if space[(x, y)] == "L" and space[(x-1, y)] == "H":
		update((x-1, y), "L")

	# water might settle if it finds a wall
	if space[(x, y)] == "R" and space[(x+1, y)] == "#":
		update((x, y), "~")
	if space[(x, y)] == "L" and space[(x-1, y)] == "#":
		update((x, y), "~")
	
	# RL is a settle
	if space[(x, y)] == "R" and space[(x+1, y)] == "L":
		update((x, y), "~")
		update((x+1, y), "~")

print(len([cell for (x, y), cell in space.items() if cell in "|HLR~" and min_y <= y <= max_y]))

print(len([cell for cell in space.values() if cell == "~"]))


# Code to see the computed map, quite fun to watch :)
#min_x = min(coord[0] for coord in space.keys())
#max_x = max(coord[0] for coord in space.keys())
#for y in range(0, max_y + 1):
#	for x in range(min_x, max_x + 1):
#		print(space[(x, y)], end="")
#	print()



