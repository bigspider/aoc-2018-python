import sys
from collections import Counter
from itertools import combinations

inp = sys.stdin.readlines()

counters = list(map(Counter, inp))
frequency_counters = list(map(lambda counter: Counter(counter.values()), counters))

count_2 = len([1 for fcounter in frequency_counters if fcounter[2] > 0])
count_3 = len([1 for fcounter in frequency_counters if fcounter[3] > 0])

print(count_2 * count_3)

for line1, line2 in combinations(inp, 2):
    res = [line1[i] for i in range(len(line1)) if line1[i] == line2[i]]
    if len(res) == len(line1) - 1:
        print("".join(res))
        break
