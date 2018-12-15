import sys
from collections import defaultdict

tasks = set()
succ = defaultdict(set)  # succ[i] is the set of predecessors
indegree = defaultdict(lambda: 0)

for line in sys.stdin.readlines():
	parts = line.split()
	src = parts[1]
	dst = parts[7]
	tasks.update([src, dst])
	indegree[dst] += 1
	succ[src].add(dst)

indegree_copy = indegree.copy()

available_tasks = { task for task in tasks if indegree[task] == 0 }

while len(available_tasks) > 0:
	task = min(available_tasks) # ain't nobody got time for a priority queue :P
	print(task, end="")

	for dest in succ[task]:
		indegree[dest] -= 1
		if indegree[dest] == 0:
			available_tasks.add(dest)
	
	available_tasks.remove(task)
print()


# PART 2

N_WORKERS = 5

worker_end_time = [0] * N_WORKERS
task_end_time = {}

indegree = indegree_copy
available_tasks = { task for task in tasks if indegree[task] == 0 }
task_start_time_bound = defaultdict(lambda: 0)  # lower bound for the start time of a task

while len(available_tasks) > 0:
	
	time_next_available_worker = min(worker_end_time)
	next_worker = min(range(N_WORKERS), key=lambda i: worker_end_time[i])
		
	# Find the first available task, breaking ties lexicographically
	task = min(available_tasks, key=lambda task: (max(worker_end_time[next_worker], task_start_time_bound[task]), task))

	task_end_time = max(worker_end_time[next_worker], task_start_time_bound[task]) + 61 + ord(task) - ord('A')
	worker_end_time[next_worker] = task_end_time

	for dest in succ[task]:
		indegree[dest] -= 1
		if indegree[dest] == 0:
			available_tasks.add(dest)
		
		task_start_time_bound[dest] = max(task_start_time_bound[dest], task_end_time) # +1 goes here?
	
	available_tasks.remove(task)

print(max(worker_end_time))
