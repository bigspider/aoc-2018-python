import sys

def print_all(node):
	initial_node = node
	while True:
		print(node.value, end= " ")
		node = node.next_node
		
		if node == initial_node:
			break
	print()

class Node:
	def __init__(self, value, prev_node = None, next_node = None):
		self.value = value
		self.prev_node = prev_node
		self.next_node = next_node
	
	# Returns a reference to the node n positions backwards
	def prev(self, n):
		res = self
		for _ in range(n):
			res = res.prev_node
		return res
	
	
	def delete(self):
		self.prev_node.next_node = self.next_node
		self.next_node.prev_node = self.prev_node

def elf_game(last_marble_value):
	cur_marble = Node(0)
	cur_marble.next_node = cur_marble
	cur_marble.prev_node = cur_marble

	cur_player = 0
	scores = [0] * n_players

	for i in range(1, last_marble_value+1):
		if i % 23 != 0:
			new_prev = cur_marble.next_node
			new_next = new_prev.next_node
							
			cur_marble = Node(i, new_prev, new_next)
			new_prev.next_node = cur_marble
			new_next.prev_node = cur_marble
			
		else:
			scores[cur_player] += i
			removed_marble = cur_marble.prev(7)
			removed_marble.delete()
			scores[cur_player] += removed_marble.value
			cur_marble = removed_marble.next_node
		
		cur_player = (cur_player + 1) % n_players	
	return max(scores)

inp = input().split()

n_players = int(inp[0])
last_marble_value = int(inp[6])

print(elf_game(last_marble_value))
print(elf_game(last_marble_value * 100))
