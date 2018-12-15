import sys
from collections import deque

def checksum_value(data):
	n_children = data.popleft()
	n_metadata = data.popleft()
	s = 0  # node checksum
	v = 0  # node value
	
	children_values = []
	for _ in range(n_children):
		child_s, child_v = checksum_value(data)
		s += child_s
		children_values.append(child_v)
	
	for _ in range(n_metadata):
		t = data.popleft()
		s += t
		if n_children == 0:
			v += t
		else:
			if 0 < t <= n_children:
				v += children_values[t-1]
	
	return s, v

inp = [int(x) for x in input().split()]

data = deque(inp)

checksum, value = checksum_value(data)

print(checksum)
print(value)


