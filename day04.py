import sys
from collections import defaultdict

inp = sorted(sys.stdin.readlines())

guard_ids = set()
sleepytimes = defaultdict(lambda: [0] * 60)
sleepyminutescount = defaultdict(lambda: 0)


for line in inp:
	pieces = line.split()
	minute = int(pieces[1][3:5])
		
	if pieces[2] == 'Guard':
		guard_id = int(pieces[3][1:])
		guard_ids.add(guard_id)
	elif pieces[2] == 'falls':
		sleep_start = minute
	elif pieces[2] == 'wakes':
		sleep_end = minute
		sleepyminutescount[guard_id] += sleep_end - sleep_start
		for i in range(sleep_start, sleep_end):
			sleepytimes[guard_id][i] += 1

sleepiest_id = max(guard_ids, key=lambda x: sleepyminutescount[x])
sleepiest_time = max(range(0, 60), key=lambda i: sleepytimes[sleepiest_id][i])

print(sleepiest_id * sleepiest_time)

max_found = -1
part2_guard_id = None
part2_minute = None

for guard_id in guard_ids:
	for i in range(0, 60):
		if sleepytimes[guard_id][i] > max_found:
			max_found = sleepytimes[guard_id][i]
			part2_guard_id = guard_id
			part2_minute = i

print(part2_guard_id * part2_minute)
