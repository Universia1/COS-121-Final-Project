from player_data import *
from final_project_gameTools import *
		
def battle(player, enemy):
	print(f"\nA {enemy['name']} appears!")
	enemy_hp = int(enemy["maxhp"])  # make sure maxhp is an int
	player_hp = player["HP"]
	
	while enemy_hp > 0 and player_hp > 0:
		print(f"\n{player['name']}'s HP: {player_hp}/{player['maxHP']}")
		print(f"{enemy['name']}'s HP: {enemy_hp}/{enemy['maxhp']}")
		action = input("What will you do? (1: Attack; 2: Use item): ").strip().lower()
		weapon_dmg = 0
		if "basic stick" in player["held_weapon"]:
			weapon_dmg = 3 
		if "blade of cinders" in player["held_weapon"]:
			weapon_dmg = 15
		if action == "1":
			atk_dmg = diceRoll("2d6")
			atk_dmg = sum(atk_dmg) + weapon_dmg + player["base_atk"] # take the sum of the values inside rolls_list, convert to int and then add the base weapon dmg and player's base dmg (0 if no atk ups have been used) to calculate total atk dmg
			print(atk_dmg)
			enemy_hp -= atk_dmg
			print(f"You attack and deal {atk_dmg} damage to the {enemy['name']}!")
		elif action == "2":
			if not player["inventory"]:
				print("You have no usable items! Returning to menu.")
				continue
			print(f"Your available items: {','.join(player['inventory'])}")
			use_item = input("will you use an item? (Y/N): ").strip().lower()
			if use_item == "y":
				break
			elif use_item == "n":
				print("You decided not to use an item.")
				continue
			else:
				print("Invalid action. Try again.")
			item_choice = input("Which item will you use? (Enter item name): ")
			if item_choice == "atk up" and "atk up" in player["inventory"]:
				use_atk_up = input("Will you use an atk up? (Y/N): ").strip().lower()
			if use_atk_up == "y": 
				print("You used an atk up and your attack damage went up!")
				player["base_atk"] += 5
				player["inventory"]["atk up"] -= 1
				break
			elif use_atk_up == "n":
				print("You decided not to use an atk up.")
				break
			else:
				print("Invalid action. Try again.") 
			if item_choice == "health potion" and "health potion" in player["inventory"]:
				use_potion = input("Will you use a health potion (Y/N)?: ").strip().lower()
				if use_potion == "y":
					player["inventory"].remove("health potion")
					heal_amount = sum(diceRoll("2d9"))
					player_hp = min(player_hp + heal_amount, player["maxHP"]) # this makes it so that the heal doesn't exceed player's max HP
					print(f"You used a health potion and healed for {heal_amount} HP! Your current HP: {player_hp}/{player['maxHP']}")
					break # exits item menu after using the item
				elif use_potion == "n":
					print("You decided not to use a health potion.")
					break # exit item menu 
				else:
					print("Invalid action. Try again.")
							
		else:
			print("Invalid input. Try again.") # the enemy will have the chance to attack player as punishment even if input is invalid
		if enemy_hp <= 0:
			print(f"You defeated the {enemy['name']}!")
			print(f"You gained {enemy['reward']} G!")
			player["current_G"] += enemy["reward"]
			break
		# enemy's turn
		enemy_atk_roll = random.randint(1,3)
		if enemy_atk_roll == 1:
			enemy_atk_dmg = diceRoll("2d10")
			enemy_atk_dmg = sum(enemy_atk_dmg)
			player_hp -= enemy_atk_dmg
			print(f"The {enemy['name']} attacks and deals {enemy_atk_dmg} damage!")
		else:
			print(f"The {enemy['name']} tries to attack but misses!")
		if player_hp <= 0:
			print(f"The {enemy['name']} defeated you.")
			player["HP"] = 0
			return
	player["HP"] = player_hp # update player's HP after battle
	return player

# enter player into the town square
# from here, player can choose to go to the tavern, shop, cave, ominous dungeon, sky fortress,
# or the final dungeon (once the key to open the dungeon is in the player's inventory).
# parameters: world
# returns the whole function
def showTown(world, player):
	print("\nYou are in the main town square, this is your home base.")
	print("\nAround you, there is a tavern and a shop to buy/sell items.")
	print("\nTo the East there is a cave said to hold the fabled 'Blade of Cinders'.")
	print("\nTo the West, there is an ominous dungeon.")

	while True:
		movement_input = input("Where will you go? (Tavern, Shop, East, or West): ")
		movement_input = movement_input.strip().lower()
		if movement_input == "tavern":
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
				player["inventory"]["health potion"] = player["inventory"].get("health potion", 0) + 1
				print(f"You now have {player['inventory']['health potion']} health potion(s) in your inventory.")
				while True:
					next_step = input("What will you do? (1: Go deeper, 2: Return to town): ").strip()
					if next_step == "1":
						current_room += 1
						break
					elif next_step == "2":
						if current_room == 1:
							print("You return to the town square.")
							world["loc"] = "town_square"
							return
						else:
							current_room -= 1
							break
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
							if current_room == 1:
								print("You return to the town square.")
								world["loc"] = "town_square"
								return
							else:
								current_room -= 1
								break
						else:
							print("Invalid action. Try again.")
							
def getValidInput(choices):
	while True:
		print("Available options:")
		for option in choices:
			print(f"   {option}")
		decision = input(": ").strip().lower()
		if decision in choices:
			return decision
		else: 
			print("Invalid option. Try again.")
							
def showShop(world, player):
	print("You enter the shop and see shelves lined with all sorts of items and potions.")
	print("The shopkeeper greets you warmly and then asks if you will buy or sell.")
	avail_items = {
		"health potion": {"price": 5, "quantity": 30},
		"atk up": {"price": 20, "quantity": 10},
		"shield": {"price": 60, "quantity": 1},
	}
	
	while True:
		shop_action = input("What will you do? (1: Buy; 2: Sell; 3: Leave): ") 
		if shop_action == "1": # if player chooses to buy
			print(f"Your G: {player['current_G']}")
			print("\nAvailable items:")
			for item, details in avail_items.items():
				print(f"{item.capitalize()} - {details['price']}G (x{details['quantity']})")
				
			buy_item = input("Which item will you buy? (Enter name or 'cancel' to leave): ").strip().lower()
			if buy_item in avail_items and avail_items[buy_item]["quantity"] > 0:
				item = avail_items[buy_item]
				while True: # so player atk doesn't scale infinitely, limit atk ups but make potions unlimited
					try:
						quantity = int(input(f"How many {buy_item}s would you like to buy? (Available: {item['quantity']})"))
						total_cost = item["price"] * quantity
						if quantity <= 0:
							print("That's an invalid quantity. Enter quantity again.")
						elif quantity > item["quantity"]:
							print("There is not enough of that item in stock. Try again.")
						elif player["current_G"] < item["price"] * quantity:
							print("You don't have enough G. Returning to the main shop menu.")
							break
						else:
							# complete the transaction
							item["quantity"] -= quantity
							player["current_G"] -= total_cost
							if buy_item in player["inventory"]:
								player["inventory"][buy_item] += quantity
							else:
								player["inventory"][buy_item] = quantity
							print(f"You purchased {quantity} {buy_item}(s) for {item['price'] * quantity}G!")
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
			if decision != "cancel":
				sell_item = decision
				sell_price = avail_items[sell_item]["price"] // 2 # items sell for half their purchase price
				while True:
					try:
						sell_quantity = int(input(f"How many {sell_item}s will you sell? (You have: {player['inventory'][sell_item]}): "))
						if sell_quantity <= 0:
							print("Invalid quantity. Enter number of items you want to sell again.")
						elif sell_quantity > player["inventory"][sell_item]:
							print("You don't have that many of that item to sell. Try again.")
						else:
							# complete the sale
							for i in range(sell_quantity):
								player["inventory"][sell_item] -= sell_quantity
								if player["inventory"][sell_item] == 0:
									del player["inventory"][sell_item] # remove item from inventory if quantity is 0
								player["current_G"] += sell_price * sell_quantity
								if sell_item in avail_items:
									avail_items[sell_item]["quantity"] += sell_quantity
								else:
									avail_items[sell_item] = {"price": 0, "quantity": sell_quantity} # add item to shop inventory
								print(f"You sold {sell_quantity} {sell_item}(s) for {sell_price * sell_quantity}G!")
								print(f"G left: {player['current_G']}")
							
							break
					except ValueError:
						print("Invalid input. Please enter a number.")
			elif decision == "cancel":
				print("You decide not to sell anything.")
			else:
				print("Invalid action. Try again.")
		elif shop_action == "3":
			print("You leave the shop and return to the town square.")
			world["loc"] = "town_square"
			break
		else:
			print("Invaild action. Try again.")

def showTavern(world, player):
	print("You walk through the tavern door and enter a firelit room bustling with adventurers.")
	print("The owner of the tavern shouts out to you in a deep, booming voice and asks if you will be staying the night.")
	stay_leave = input("What will you do? (Stay the night (10G); Leave): ")
	option = stay_leave
	getValidInput(option)
	
	# test to see if the new commit worked
