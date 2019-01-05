import sys
import re
import time

class Group:
	def __init__(self, n_units, hit_points, attack_damage, attack_type, initiative, immune_to, weak_to, index=None, camp=None, boost=0):
		self.n_units = n_units
		self.n_alive_units = n_units
		
		self.hit_points = hit_points
		self.attack_damage = attack_damage
		self.attack_type = attack_type
		self.initiative = initiative
		self.immune_to = immune_to
		self.weak_to = weak_to
		
		self.index = index
		self.camp = camp
		self.attacking = None
		self.attacked_by = None
		self.boost = boost
		
	def effective_power(self):
		return self.n_alive_units * (self.attack_damage + self.boost)
	
	def __repr__(self):
		return f"camp={self.camp}, index={self.index}: n_units={self.n_units}, hit_point={self.hit_points}, attack_damage={self.attack_damage}, attack_type={self.attack_type}, initiative={self.initiative}, boost={self.boost}"


pattern = re.compile(r"^(\d+) units each with (\d+) hit points (\([a-z,; ]+\) )?with an attack that does (\d+) ([a-z]+) damage at initiative (\d+)$")
def read_groups(camp):
	groups = []
	index = 0
	while True:
		line = sys.stdin.readline().strip()
		if line == '':
			break
		
		re_groups = pattern.match(line).groups()		
		
		n_units = int(re_groups[0])
		hit_points = int(re_groups[1])
		description = re_groups[2]
		attack_damage = int(re_groups[3])
		attack_type = re_groups[4]
		initiative = int(re_groups[5])

		immune_to = set()
		weak_to = set()
		if description is not None:
			for part in description[1:-2].split("; "):
				effect, types = part.split(" to ")
				if effect == "immune":
					immune_to.update(types.split(", "))
				else:  # effect == "weak"
					weak_to.update(types.split(", "))
		
		groups.append(Group(n_units, hit_points, attack_damage, attack_type, initiative, immune_to, weak_to, index, camp=camp))
		index += 1
	return groups


def damage(attacking_group, defending_group):
	if attacking_group.attack_type in defending_group.immune_to:
		return 0
	elif attacking_group.attack_type in defending_group.weak_to:
		return 2 * attacking_group.effective_power()
	else:
		return attacking_group.effective_power()


def battle(groups, boost=0):
	for group in groups:
		group.n_alive_units = group.n_units
		if group.camp == 0:
			group.boost = boost
		
	while any(group.camp == 0 for group in groups) and any(group.camp == 1 for group in groups):
		stalemate = True
		
		for group in groups:
			group.attacking = None
			group.attacked_by = None

		# target selection
		for selecting_group in sorted(groups, key=lambda g: (-g.effective_power(), -g.initiative)):
			enemies = [g for g in groups if g.camp != selecting_group.camp and g.attacked_by is None]
			if len(enemies) == 0:
				continue
			
			best_target = max(enemies, key=lambda g: (damage(selecting_group, g), g.effective_power(), g.initiative))
			if damage(selecting_group, best_target) > 0:
				selecting_group.attacking = best_target
				best_target.attacked_by = selecting_group
		
		# attacking phase
		for group in sorted(groups, key=lambda g: -g.initiative):
			if group.n_alive_units > 0 and group.attacking is not None:
				attacked = group.attacking
				d = damage(group, attacked)
				n_killed_units = min(attacked.n_alive_units, d // attacked.hit_points)
				if n_killed_units > 0:
					stalemate = False
				#print(f"attacker: {group}")
				#print(f"defender: {attacked}")
				#print(f"damage: {d}, defending hit_points {attacked.hit_points}: {n_killed_units} units killed")
				attacked.n_alive_units = attacked.n_alive_units - n_killed_units
				
		
		# remove groups with 0 units left
		groups = [group for group in groups if group.n_alive_units > 0]

		if stalemate:
			# Combat did not end, but we are not done yet; consider it a win of the infection.
			# It seems to be a bug, instructions do not consider the stalemate possibility
			groups = [group for group in groups if group.camp == 1]  # simulate victory of infection

	return groups


input() # Ignore line
groups_0 = read_groups(0)
input() # Ignore line
groups_1 = read_groups(1)

all_groups = groups_0 + groups_1


#Part 1
groups_after = battle(all_groups)
print(sum(g.n_alive_units for g in groups_after))

#Part 2: binary search on the boost
min_boost = 1  # if boost < min_boost, immune system loses for sure
max_boost = None # if boost >= max_boost, immune system wins for sure; None means infinity

while max_boost is None or min_boost < max_boost:
	m_boost = 2 * min_boost if max_boost is None else (max_boost + min_boost)//2
	
	print(f"trying {m_boost}; [{min_boost}-{max_boost}]")
	
	groups_after = battle(all_groups, boost=m_boost)
	if list(groups_after)[0].camp == 0:
		max_boost = m_boost  # immune system won
	else:
		min_boost = m_boost + 1
	
	print(sum(g.n_alive_units for g in groups_after))

print(m_boost)
groups_after = battle(all_groups, m_boost)
print(sum(g.n_alive_units for g in groups_after))
	
