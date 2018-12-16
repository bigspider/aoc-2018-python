import sys
from collections import defaultdict

# Simulate 1 generation
def process(status, rules):
	snapshot = status.copy()
	min_i = min(snapshot.keys())
	max_i = max(snapshot.keys())
	
	for i in range(min_i-2, max_i+3):
		rule = (((snapshot[i-2]*2 + snapshot[i-1])*2 + snapshot[i])*2 + snapshot[i+1])*2 + snapshot[i+2]
		status[i] = rules[rule]
		if status[i] == 0:
			del status[i]

inp = sys.stdin.readlines()

initial_status = list(map(lambda c: 0 if c == "." else 1, inp[0].strip().split(" ")[2]))
status = defaultdict(int)

for i, st in enumerate(initial_status):
	if st == 1:
		status[i] = st

rules = [0] * 32
for line in inp[2:]:
	src, dst = map(lambda x: int(x.replace(".", "0").replace("#", "1"), 2), line.split(" => "))
	rules[src] = dst

for _ in range(20):
	process(status, rules)

res = sum(filter(lambda i: status[i] == 1, status.keys()))
print(res)

# Observation: after a number of iterations, the number of plants increase by 8 for each generation.
# Could be interesting to prove this, it doesn't seem obvious.
# Note: the difference per iteration is likely different for different inputs.
# We reach 2000 generations, then add 8 for each remaining generation.
n_generations = 50000000000
for _ in range(1980):
	process(status, rules)

res2 = sum(filter(lambda i: status[i] == 1, status.keys()))
print(res2 + 8*(n_generations - 2000))
	
