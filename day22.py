import sys
	
def can_enter(region_type, equip):
	return region_type != equip

def geological_index(coords):
	global gi, target, depth
	if coords not in gi:
		x, y = coords
		if (x, y) == (0, 0) or (x, y) == target:
			res = 0
		elif y == 0:
			res = x * 16807
		elif x == 0:
			res = y * 48271
		else:
			geological_index((x - 1, y))
			geological_index((x, y-1))
			res = gi[(x - 1, y)] * gi[(x, y-1)]

		res = (res + depth) % 20183
		gi[coords] = res

	return gi[coords] % 3


# Cost of the edge between node1 and node2 (assuming there is one)
def weight(node1, node2):
	((x1, y1), equip1) = node1
	((x2, y2), equip2) = node2
	
	if (x1, y1) == (x2, y2):
		# just switching equipment 
		return 7 if equip1 != equip2 else 0
	elif abs(x1 - x2) + abs(y1 - y2) == 1 and equip1 == equip2:
		# moving to near square, assuming it is allowed
		return 1
	else:
		return None  # there is no edge

def neighbors(node, gi):
	global MAX_X, MAX_Y
	((x, y), equip) = node
	res = []
	if x > 0 and can_enter(geological_index((x - 1, y)), equip):
		res.append(((x - 1, y), equip))
	if y > 0 and can_enter(geological_index((x, y - 1)), equip):
		res.append(((x, y - 1), equip))
	if x < MAX_X and can_enter(geological_index((x + 1, y)), equip):
		res.append(((x + 1, y), equip))
	if y < MAX_Y and can_enter(geological_index((x, y + 1)), equip):
		res.append(((x, y + 1), equip))
	if can_enter(geological_index((x, y)), (equip + 1) % 3):
		res.append(((x, y), (equip + 1) % 3))
	if can_enter(geological_index((x, y)), (equip + 2) % 3):
		res.append(((x, y), (equip + 2) % 3))
	return res


inp = sys.stdin.readlines()
depth = int(inp[0].split()[1])
width, height = map(int, inp[1].split()[1].split(","))
target = (width, height)

gi = {} # geological index mod 20183

print(sum(geological_index((x, y)) for x in range(width+1) for y in range(height+1)))

# make a graph, where a "node" is a pair (coordinates, equipment),
# where equipment is 0 (neither), 1 (torch), 2 (climbing gear)
root = ((0, 0), 1)
dist = {root: 0}
target_node = (target, 1)
q = {root}  # priority queue would be faster

# Pruning strategy: we forbid nodes too much to the right or bottom of target.
# Given that inputs are pseudorandom, it works with high probability.
# Better would be to improve Dijkstra with a priority queue.
MAX_X = width + 100
MAX_Y = height + 100


while len(q) > 0:
	node = min(q, key=lambda n: dist[n])
	q.remove(node)

	if node == target_node:
		break  # distance to target is found
	
	for neighbor_node in neighbors(node, gi):
		if neighbor_node not in dist:
			q.add(neighbor_node)  # previously undiscovered node
		dist[neighbor_node] = min(dist.get(neighbor_node, float('inf')), dist[node] + weight(node, neighbor_node))

print(dist[target_node])
