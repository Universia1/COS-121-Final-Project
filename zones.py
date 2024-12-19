from player_data import *
from final_project_gameTools import *
		
# this file contains all functions relating to the 5 zones in the game: town square, shop, tavern, cave, final dungeon
# there is also a function for using items (applied to using items inside and outside of battle), a battle function for regular enemies in the cave, a battle function for the final boss fight, a function for validating action/decision inputs (not used very much because it was implemented later into the coding process), a function for selecting enemy spawns in the cave depending on a 1:3 rng roll, and a function that maintains shop's item stock (if an item is bought, the remaining buyable number of that item is permenantly reduced until the player sells an item to the shop)
		
# function for using items in battle and in town square before battle
# parameters: player
# returns: nothing
def useItem(player):
	print("Which item will you use? (Enter 'cancel' if you don't want to use an item)")
	if "shield" in player["inventory"]:
		player["def"] += 10
		print("The shield automatically increases your def to 10. It is not a consumable item.")
	options = []
	for item in player["inventory"]:
		options.append(item)
	options.append("cancel")
	decision = getValidInput(options)
	item_choice = decision
	while True:
		if item_choice == "cancel":
			print("You decided to not use an item.")
			return player
		if item_choice == "health potion" and item_choice in player["inventory"]:
			num_used = int(input(f"How many {item_choice}s do you want to use? (Enter '0' to cancel): "))
			if num_used == 0:
				print(f"You decided to not use a(n) {item_choice}.")
				break
			elif num_used > 0 and player["inventory"][item_choice] > 0:
				heal_amount = 15 * num_used
				player["HP"] = min(player["HP"] + heal_amount, player["maxHP"])  # heal without exceeding max HP
				print(f"You used {num_used} {item_choice}(s) and healed {heal_amount} HP!")
				player["inventory"][item_choice] -= num_used
				if player["inventory"][item_choice] == 0:
					del player["inventory"][item_choice]
				break
		elif item_choice == "atk up" and item_choice in player["inventory"]:
			num_used = int(input(f"How many {item_choice}s do you want to use? (Enter '0' to cancel): "))
			if num_used == 0:
				print(f"You decided to not use a(n) {item_choice}.")
				break
			elif num_used > 0 and player["inventory"][item_choice] > 0:
				player["atk"] += 5 * num_used
				print(f"You used {num_used} {item_choice}(s) and your atk was increased by {5 * num_used} points!")
				player["inventory"][item_choice] -= num_used
				if player["inventory"][item_choice] == 0:
					del player["inventory"][item_choice]
				break
		elif item_choice == "def up" and item_choice in player["inventory"]:
			num_used = int(input(f"How many {item_choice}s do you want to use? (Enter '0' to cancel): "))
			if num_used == 0:
				print(f"You decided to not use a(n) {item_choice}.")
				break
			elif num_used > 0 and player["inventory"][item_choice] > 0:
				player["def"] += 5 * num_used
				print(f"You used {num_used} {item_choice}(s) and your def was increased by {5 * num_used} points!")
				player["inventory"][item_choice] -= num_used
				if player["inventory"][item_choice] == 0:
					del player["inventory"][item_choice]
				break
		elif item_choice == "maxhp up" and item_choice in player["inventory"]:
			num_used = int(input(f"How many {item_choice}s do you want to use? (Enter '0' to cancel): "))
			if num_used == 0:
				print(f"You decided to not use a(n) {item_choice}.")
			elif num_used > 0 and player["inventory"][item_choice] > 0:
				player["maxHP"] += 10 * num_used
				print(f"You used {num_used} {item_choice}(s) and your max HP was increased by {10 * num_used}!")
				player["inventory"][item_choice] -= num_used
				if player["inventory"][item_choice] == 0:
					del player["inventory"][item_choice]
				break
			else:
					print("Invalid input. Try again.")
					continue			
	return player

# battle sequence that will be used throughout the cave
# parameters: world, player
# returns: player (for updating player["HP"])		
def battle(player, enemy):
	print(f"\nA {enemy['name']} appears!")
	enemy_hp = int(enemy["hp"])  # make sure hp is an int
	enemy_maxhp = int(enemy["maxhp"]) # do the same for maxhp
	if "blade of cinders" in player["held_weapon"]:
		enemy_maxhp += 20
		enemy_hp += 20
	while enemy_hp > 0 and player["HP"] > 0:
		print(f"\n{player['name']}'s HP: {player['HP']}/{player['maxHP']}")
		print(f"{enemy['name']}'s HP: {enemy_hp}/{enemy_maxhp}")
		action = input("What will you do? (1: Attack; 2: Use item): ").strip().lower()
		if "shield" in player["inventory"]:
			player["def"] = 10
		weapon_dmg = 0
		if "basic stick" in player["held_weapon"]:
			weapon_dmg = 3 
		if "blade of cinders" in player["held_weapon"]:
			weapon_dmg = 15
		if "celestial blade" in player["held_weapon"]:
			weapon_dmg = 30
		if action == "1":
			if "blade of cinders" not in player["held_weapon"]:
				atk_dmg = diceRoll("2d6")
				atk_dmg = sum(atk_dmg) + weapon_dmg + player["atk"] # take the sum of the values inside rolls_list, convert to int and then add the base weapon dmg and player's base dmg (0 if no atk ups have been used) to calculate total atk dmg
				enemy_hp -= atk_dmg
			elif "blade of cinders" in player["held_weapon"]:
				atk_dmg = diceRoll("5d4")
				atk_dmg = sum(atk_dmg) + player["atk"]
				enemy_hp -= atk_dmg
			print(f"You attack and deal {atk_dmg} damage to the {enemy['name']}!")
		elif action == "2":
			if not player["inventory"]:
				print("You have no usable items! Returning to menu.")
				continue
			print("\nYour availble items:")
			for item, quantity in player["inventory"].items():
				print(f"   {item.capitalize()} (x{quantity})")
			use_item = input("will you use an item? (Y/N): ").strip().lower()
			if use_item == "y":
				player = useItem(player)
			elif use_item == "n":
				print("You decided to not use any items.")
				continue
		if enemy_hp <= 0:
			print(f"You defeated the {enemy['name']}!")
			print(f"You gained {enemy['reward']} G!")
			player["current_G"] += enemy["reward"]
			player["enemy_slain"] += 1
			break
		# enemy's turn
		enemy_atk_roll = random.randint(1,3)
		if enemy_atk_roll == 1:
			if "blade of cinders" not in player["held_weapon"]:
				enemy_atk_dmg = diceRoll("2d10")
				enemy_atk_dmg = sum(enemy_atk_dmg)
			elif "blade of cinders" in player["held_weapon"]:
				enemy_atk_dmg = diceRoll("3d10")
				enemy_atk_dmg = sum(enemy_atk_dmg)
			if enemy_atk_dmg < player["def"]:
				player["HP"] -= 0
				print(f"The {enemy['name']} attacks for {enemy_atk_dmg} damage, but your sheer toughness blocks all the damage!")
			elif enemy_atk_dmg > player["def"]:
				player["HP"] -= enemy_atk_dmg - player["def"]
				print(f"The {enemy['name']} attacks and deals {enemy_atk_dmg - player['def']} damage!")
		else:
			print(f"The {enemy['name']} tries to attack but misses!")
		if player["HP"] <= 0:
			print(f"The {enemy['name']} defeated you.")
			player["HP"] = 0
			return
	player["HP"] = player["HP"]
	return player

# enter player into the town square
# from here, player can choose to go to the tavern, shop, cave, ominous dungeon, sky fortress,
# or the final dungeon (once the key to open the dungeon is in the player's inventory).
# parameters: world
# returns the whole function
def showTown(world, player):
	print("\nYou are in the main town square, this is your home base.")
	print("\nAround you, there is a tavern where you can fully restore your HP for 20G and a shop to buy/sell items.")
	if "blade of cinders" not in player["held_weapon"]:
		print("\nTo the East there is a cave said to hold the fabled 'Blade of Cinders'.")
	else:
		print("\nTo the East lies the cave where you got the Blade of Cinders.\nYou can still travel there and explore, but beware: the enemies there have become stronger!")
	print("To the West, there is an ominous dungeon.")
	while True:
		movement_input = input("Where will you go? (Tavern, Shop, East, or West) (Enter 'use item' to use items): ")
		movement_input = movement_input.strip().lower()
		if movement_input == "use item":
			if not player["inventory"]:
				print("You don't have any items in your inventory!")
			else:
				print("\nYour availble items:")
				for item, quantity in player["inventory"].items():
					print(f"   {item.capitalize()} (x{quantity})")
				use_item = input("will you use an item? (Y/N): ").strip().lower()
				if use_item == "y":
					useItem(player)
					continue
				elif use_item == "n":
					print("You decided to not use any items.")
					break
		elif movement_input == "tavern":
			world["loc"] = "tavern"
			break
		elif movement_input == "shop":
			world["loc"] = "shop"
			break
		elif movement_input == "east":
			world["loc"] = "mysterious_cavern"
			break
		elif movement_input == "west":
			world["loc"] = "ominous_dungeon"
			break
		else:
			print("Invalid action. Try again.") 
	return
	
def selectEnemy(enemy_list, enemy_spawn):
	cave_enemy = {
		"1": "bat",
		"2": "skeleton",
		"3": "spider"
	}	
	enemy_name = cave_enemy[enemy_spawn]
	if enemy_name:
		return enemy_list[enemy_name]
	return None
	
# if player chooses to go to the cavern, this function will run in main()
# contains all information about the cavern:
# rng for enemy spawns; 1=bat, 2=skeleton, 3=spider, 4=none (instead, there will be a small chest containing a health pot)
# 3 rooms, the last room will contain a chest w/ blade of cinders
# parameters: world
# returns the whole function
def showCavern(world, player):
	print("\nYou travel Eastward and safely arrive at the mysterious cave.")
	# confirm entering the cave
	while True:
		enter = input("Will you enter the cave? (Y/N): ").strip().lower()
		if enter == "y":
			print("\nYou enter the cavern and find yourself in a dark chamber with stalagmites rising from the ground.")
			break
		elif enter == "n":
			print("You return to the town square.")
			world["loc"] = "town_square"
			return
		else:
			print("Invalid action. Try again.")

	# initialize room navigation
	current_room = 1
	max_rooms = 4

	# read enemy data once before the loop
	with open("avail_enemies.csv", "r") as file: # open avail_enemies.csv, read it, and close it all in one command
		enemy_list = {}
		for line in file.read().strip().split("\n")[1:]:
			loc, name, maxhp, reward = line.split(",")
			enemy_list[name] = {
				"name": name, 
				"loc": loc, 
				"maxhp": int(maxhp),
				"hp": int(maxhp),
				"reward": int(reward)
			}
	while current_room <= max_rooms:
		print(f"\nYou are in cavern room {current_room}.")
		if current_room == max_rooms:
			# final room
			print("\nYou step into the final room and see a glowing sword on a pedestal.")
			if "blade of cinders" in player["held_weapon"]:
				print("You already obatined the Blade of Cinders. A strange magic warps you back to the town square.")
				world["loc"] = "town_square"
				return
			else:
				while True:
					print("You walk up to the pedestal and see there is an engraving that reads: \nHere rests the legendary Blade of Cinders. Only the hero of fate can lift it from this pedestal.")
					take_sword = input("Will you take the Blade of Cinders? (Y/N): ").strip().lower()
					if take_sword == "y":
						print("You drop your basic stick and lift the Blade of Cinders from its pedestal!")
						print(f"{player['name']} obtained the Blade of Cinders!")
						player["held_weapon"] = ["blade of cinders"]
						print("You feel a strange magic warp you back to the town square.")
						world["loc"] = "town_square"
						return
					elif take_sword == "n":
						print("You leave the Blade of Cinders and return to the previous room.")
						current_room -= 1
						break
					else:
						print("Invalid action. Try again.")
		else:
			# room logic for rooms 1-3
			spawn_roll = diceRoll("1d4")[0]
			if spawn_roll == 4:
				print("You find a chest containing a health potion!")
				if "health potion" in player["inventory"]:
					player["inventory"]["health potion"] += 1
				else:
					player["inventory"]["health potion"] = 1
				print(f"You now have {player['inventory']['health potion']} health potion(s) in your inventory.")
				while True:
					next_step = input("What will you do? (1: Go deeper, 2: Return to town): ").strip()
					if next_step == "1":
						current_room += 1
						break
					elif next_step == "2":
							print("You return to the town square.")
							world["loc"] = "town_square"
							return
					else:
						print("Invalid action. Try again.")
			else:
				enemy = selectEnemy(enemy_list, str(spawn_roll))
				if enemy:
					battle(player, enemy)
					if player["HP"] <= 0:
						return  # exit function if the player dies
					# room navigation
					while True:
						next_step = input("What will you do? (1: Go deeper, 2: Return to town): ").strip()
						if next_step == "1":
							current_room += 1
							break
						elif next_step == "2":
								print("You return to the town square.")
								world["loc"] = "town_square"
								return
						else:
							print("Invalid action. Try again.")
							
def getValidInput(choices):
	while True:
		print("Available options:")
		for options in choices:
			print(f"   {options}")
		decision = input(": ").strip().lower()
		if decision in choices:
			return decision
		else: 
			print("Invalid option. Try again.")

# initializes the shop's stock so that it doesn't restock on every instance
def initializeShopStock():
	return {
	"health potion": 999,
	"atk up": 5,
	"def up": 5,
	"maxhp up": 5,
	"shield": 1
	}
		
shop_stock = initializeShopStock()

# function that enables player to buy/sell items
# player can't sell items to shop if it results in exceeding the max stock																				# parameters: world, player
# returns: nothing												
def showShop(world, player):
	print("You enter the shop and see shelves lined with all sorts of items and potions.")
	print("The shopkeeper greets you warmly and then asks if you will buy or sell.")
	
	item_prices = {
		"health potion": 5,
		"atk up": 20,
		"def up": 25,
		"maxhp up": 30,
		"shield": 60
	}
	
	max_shop_stock = {
		"health potion": 999,
		"atk up": 5,
		"def up": 10,
		"maxhp up": 10,
		"shield": 1
	}
	
	while True:
		shop_action = input("What will you do? (1: Buy; 2: Sell; 3: Leave): ") 
		if shop_action == "1": # if player chooses to buy
			print(f"\nYour G: {player['current_G']}")
			print("Available items:")
			for item, quantity in shop_stock.items():
				print(f"{item.capitalize()} - {item_prices[item]}G (x{quantity})")
			buy_item = input("Which item will you buy? (Enter name or 'cancel' to leave): ").strip().lower()
			if buy_item in shop_stock and shop_stock[buy_item] > 0:
				while True: # so player atk doesn't scale infinitely, limit atk ups but make potions practically unlimited
					try:
						quantity = int(input(f"How many {buy_item}s would you like to buy? (Available: {shop_stock[buy_item]}): "))
						total_cost = item_prices[buy_item] * quantity
						if quantity <= 0:
							print("That's an invalid quantity. Enter quantity again.")
						elif quantity > shop_stock[buy_item]:
							print("There is not enough of that item in stock. Try again.")
						elif player["current_G"] < total_cost:
							print("You don't have enough G. Returning to the main shop menu.")
							break
						else:
							# complete the transaction
							shop_stock[buy_item] -= quantity
							player["current_G"] -= total_cost
							if buy_item in player["inventory"]:
								player["inventory"][buy_item] += quantity
							else:
								player["inventory"][buy_item] = quantity
							print(f"You purchased {quantity} {buy_item}(s) for {total_cost}G!")
							print(f"G left: {player['current_G']}")
							break
					except ValueError:
						print("Invaild input. Please enter a number.")
			elif buy_item == "cancel":
				print("You decide not to buy any items.")
			else:
				print("Invalid action. Try again.")
						
		elif shop_action == "2": # if player chooses to sell
			print("\nYour inventory:")
			for item, quantity in player["inventory"].items():
				print(f"{item.capitalize()} x{quantity}")
			print("Which item wll you sell? (Enter name or 'cancel' to leave menu): ")
			options = []
			for item in player["inventory"]:
				options.append(item)
			options.append("cancel")
			decision = getValidInput(options)
			if decision == "cancel":
				print("You decide not to sell anything.")
				continue
			sell_item = decision
			if sell_item not in player["inventory"] or player["inventory"][sell_item] <= 0:
				print("You don't have that item in your inventory.")
				continue
			sell_price = item_prices[sell_item] // 2 # items sell for half their purchase price
			while True:
				try:
					sell_quantity = int(input(f"How many {sell_item}s will you sell? Enter '0' to cancel and return to option select.\n(You have: {player['inventory'][sell_item]}): "))
					if sell_quantity <= 0:
						break
					elif sell_quantity > player["inventory"][sell_item]:
						print("You don't have that many of that item to sell. Try again.")
					else:
						new_stock = shop_stock[sell_item] + sell_quantity
						if new_stock > max_shop_stock[sell_item]:
							print(f"The shop cannot hold more than {max_shop_stock[sell_item]} {sell_item}s.\nPlease sell fewer {sell_item}s.")
							continue
						# complete the sale
						if sell_quantity == player["inventory"][sell_item]:
							del player["inventory"][sell_item] # remove item entirely if all are sold
						else:
							player["inventory"][sell_item] -= sell_quantity
						shop_stock[sell_item] += sell_quantity
						player["current_G"] += sell_price * sell_quantity
						print(f"You sold {sell_quantity} {sell_item}(s) for {sell_price * sell_quantity}G!")
						print(f"G left: {player['current_G']}")		
						break
				except ValueError:
					print("Invalid input. Please enter a number.")
			else:
				print("Invalid action. Try again.")
		elif shop_action == "3":
			print("You leave the shop and return to the town square.")
			world["loc"] = "town_square"
			break
		else:
			print("Invaild action. Try again.")

# area for player to spend 20G to fully heal their HP
# returns: nothing
def showTavern(world, player):
	print("You walk through the tavern door and enter a firelit room bustling with adventurers.")
	print("The owner of the tavern shouts out to you in a deep, booming voice and asks if you will be staying the night.")
	print("What will you do?")
	player_hp = player["HP"]
	options = ["stay", "leave"]
	decision = getValidInput(options)
	if decision == "stay":
		cost = 20
		if player["current_G"] >= cost:
			player["current_G"] -= cost
			player_hp = player["maxHP"] # fully heal player
			print(f"You pay {cost}G and stay the night.\nYour HP is fully restored!")
			print(f"G left: {player['current_G']}")
			print("You leave the tavern and return to the town square.")
			world["loc"] = "town_square"
		else:
			print("You don't have enough G to stay the night.\nYou leave the tavern and return to the town square.")
			world["loc"] = "town_square"
	elif decision == "leave":
		print("You leave the tavern and return to the town square.")
		world["loc"] = "town_square"
	player["HP"] = player_hp

# dict containing final boss info, accessible on the world level
fallen_titan = {
		"maxhp": 500,
		"hp": 500,
		"name": "Fallen Titan"
	}

# function for final boss fight
# just like the basic battle function, if player HP reaches 0, game ends
# game ends if boss HP reaches 0
def finalBoss(player):
	enemy_hp = fallen_titan["hp"]
	print("The Fallen Titan lunges into battle!")
	while player["HP"] > 0 and enemy_hp > 0:
		enemy_atkRoll = random.randint(1,3)
		print(f"{player['name']}'s HP: {player['HP']}/{player['maxHP']}")
		print(f"Fallen Titan's HP: {enemy_hp}/{fallen_titan['maxhp']}")
		weapon_dmg = 30
		atk_dmg = diceRoll("2d20")
		atk_dmg = sum(atk_dmg) + weapon_dmg + player["atk"]
		if "shield" in player["inventory"]:
			player["def"] = 10
		action = input("What will you do? (1: Attack; 2: Use item): ").strip().lower()
		if action == "1":
			print(f"You attack the {fallen_titan['name']}, dealing {atk_dmg} damage!")
			enemy_hp -= atk_dmg
		elif action == "2":
			if not player["inventory"]:
				print("You have no usable items! Returning to menu.")
				continue
			print("\nYour availble items:")
			for item, quantity in player["inventory"].items():
				print(f"   {item.capitalize()} (x{quantity})")
			use_item = input("will you use an item? (Y/N): ").strip().lower()
			if use_item == "y":
				player = useItem(player)
			elif use_item == "n":
				print("You decided to not use any items.")
				continue
		else:
			print("Invalid action. Try again.")
		if enemy_atkRoll == 1:
			enemy_atk = diceRoll("3d10")
			enemy_atk = sum(enemy_atk)
			print(f"The {fallen_titan['name']} attacks you for {enemy_atk} damage!")
			player["HP"] -= enemy_atk
		elif enemy_atkRoll == 2 or enemy_atkRoll == 3:
			print(f"The {fallen_titan['name']} flinches and cannot attack!")
		if player["HP"] <= 0:
			player["HP"] = 0
			return
				
	fallen_titan["hp"] = enemy_hp
	return player, fallen_titan	

# final area of the game
def showOminousDungeon(world, player):
	if "celestial blade" not in player["held_weapon"]:
		print("You arrive at the entrance of the ominous dungeon, but it is sealed shut by a magical barrier.\nYou hear a faint voice emanate from the barrier. It says:")
		print(f"'Fateful traveler, a terribly evil being slumbers in this dungeon. If you wish to destroy this barrier and wake the being from his eternal slumber, you must first slay 100 enemies in the cavern'. You must slay {100 - player['enemy_slain']} more enemies before you can destroy the barrier.")
		print("You are warped back to the town square.")
		world["loc"] = "town_square"
	elif "celestial blade" in player["held_weapon"]:
		print("You arrive at the entrance of the ominous dungeon.\nYou reach out and touch the barrier...")
		print("The barrier shatters and you hear countless screams of pain and terror as a terribly frigid wind rushes out of the dungeon entrance.")
		print("You then hear a distant, earth-shaking groan from deep within the dungeon.")
		print("What will you do?")
		options = ["enter", "go back"]
		decision = getValidInput(options)
		if decision == "enter":
			final_battle = finalBoss(player)
		if decision == "go back":
			print("You decide to go back to the town square.")
			world["loc"] = "town_square"
			return
