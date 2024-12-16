from player_data import *
from zones import *
from final_project_gameTools import *

def main():
	player = createPlayer()
	world = {}
	print(f"Welcome to Aurelis, {player['name']}!")
	print(f"HP: {player['HP']}/{player['maxHP']}")
	world["loc"] = "town_square"
	
	# for testing purposes
	f = open("current_data.txt", "r")
	contents = f.read()
	print(contents)
	
	while True:
		if player["HP"] <= 0:
			print(f"{player['name']} has been defeated.")
			with open("current_data.txt", "a") as file
			file.write(f"Final player data: {player['']}")
			print("Game Over.")
			print("Thanks for playing!")
			break
			
		if world["loc"] == "town_square":
			showTown(world)
		elif world["loc"] == "mysterious_cavern":
			showCavern(world, player)
		elif world["loc"] == "shop":
			showShop(world, player)

main()
