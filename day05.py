import sys

def reacts(x, y):
	return x != y and x.upper() == y.upper()

def react(polymer, removed_type=None):
	cur = []
	for c in inp:
		if removed_type is None or c.upper() != removed_type.upper():
			cur.append(c)
			
			if len(cur) >= 2 and reacts(cur[-1], cur[-2]):
				cur.pop()
				cur.pop()
	return "".join(cur)


inp = input()

print(len(react(inp)))

print(min(len(react(inp, unit_type)) for unit_type in set(inp.upper())))
