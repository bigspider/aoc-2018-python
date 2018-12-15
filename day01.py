import sys

numbers = list(map(int, sys.stdin.readlines()))

print(sum(numbers))

seen = {0}
s = 0
found = False
import time
while not found:
    for n in numbers:
        s += n
        if s in seen:
            print(s)
            found = True
            break
        seen.add(s)
