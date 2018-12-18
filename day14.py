import sys

inp_str = input().strip()
inp = int(inp_str)
len_inp = len(inp_str)

recipes = [3, 7]

pos = [0, 1]

found_pos = None
while len(recipes) < inp + 10 or found_pos is None:
	s = recipes[pos[0]] + recipes[pos[1]]
	past_len = len(recipes)
	if s < 10:
		recipes.append(s)
	else:
		recipes.extend([int(s/10), s % 10])

	for elf in range(2):
		pos[elf] = (pos[elf] + recipes[pos[elf]] + 1) % len(recipes)

		for i in range(past_len, len(recipes)):
			if found_pos is None:
				if inp_str == "".join(map(str, recipes[i-len_inp:i])):
					found_pos = i - len_inp

print("".join(map(str, recipes[inp:inp+10])))
print(found_pos)
