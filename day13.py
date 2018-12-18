import sys

class Cart:
	def __init__(self, x, y, direction, turnstate = 0, dead = False):
		self.x = x
		self.y = y
		self.direction = direction
		self.turnstate = turnstate
		self.dead = dead
	def __repr__(self):
		return "Cart(%s, %s, %s, %s)" % (self.x, self.y, self.direction, self.turnstate)

inp = sys.stdin.readlines()

width = max(len(line.strip()) for line in inp)
height = len(inp)

# just the track, without cars 
track = [[None]*height for _ in range(width)] 

# list of cars
carts = []

change = {
  ">": (1, 0),
  "v": (0, 1),
  "<": (-1, 0),
  "^": (0, -1)
}

# deviation[i][cur] is the new direction if the turnstate is i and direction cur
deviation = {
  0: { # TURN LEFT
    ">": "^",
    "v": ">",
    "<": "v",
    "^": "<"
  },
  1: { ">": ">", "v": "v", "<": "<", "^": "^" },
  2: { # TURN RIGHT
    ">": "v",
    "v": "<",
    "<": "^",
    "^": ">"
  }
}

# turn[char][cur] is the new direction for turns, if current direction is cur
turn = {
 "/": {
    ">": "^",
    "v": "<",
    "<": "v",
    "^": ">"
 },
 "\\": {
    ">": "v",
    "v": ">",
    "<": "^",
    "^": "<"	
 }
}

for row, line in enumerate(inp):
	for col, char in enumerate(line.rstrip()):
		if char in "|^v":
			track[col][row] = "|"
		elif char in "-<>":
			track[col][row] = "-"
		elif char in "/\\+":
			track[col][row] = char
		
		if char in "<>^v":
			carts.append(Cart(col, row, char))

first_collision_found = False
epochs = 0
while len([c for c in carts if not c.dead]) > 1:
	carts_copy = sorted(carts, key=lambda cart: (cart.y, cart.x))
	for cart in carts_copy:
		if cart.dead:
			continue
		dx, dy = change[cart.direction]
		new_x = cart.x + dx
		new_y = cart.y + dy
				
		dest_cell = track[new_x][new_y]

		crashing_carts = [other_cart for other_cart in carts_copy if not other_cart.dead and other_cart.x == new_x and other_cart.y == new_y]
		for crashing_cart in crashing_carts:
			cart.dead = True
			crashing_cart.dead = True
			if not first_collision_found:
				print("%s,%s" % (new_x, new_y))
				first_collision_found = True

		if dest_cell == "+":
			new_direction = deviation[cart.turnstate][cart.direction]
			new_turnstate = (cart.turnstate + 1) % 3
		elif dest_cell in "/\\":
			new_direction = turn[dest_cell][cart.direction]
			new_turnstate = cart.turnstate
		else:
			new_direction = cart.direction
			new_turnstate = cart.turnstate
		
		cart.x, cart.y, cart.direction, cart.turnstate = (new_x, new_y, new_direction, new_turnstate)

for cart in carts:
	if not cart.dead:
		print("%s,%s" % (cart.x, cart.y))
