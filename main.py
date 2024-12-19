# COS 121 Final Project
# Author: Yuuna Pogrebitskiy
# Date: 12/18/2024
from player_data import *
from zones import *
from final_project_gameTools import *

# this is the main function of the game
# the entire world is stored inside this function
# all major events throughout the game are printed via this function

def main():
	player = createPlayer()
	world = {}
	print(f"Welcome to Celestia, {player['name']}!")
	world["loc"] = "town_square"
	
	while True:
		if world["loc"] == "town_square":
			if player["enemy_slain"] >= 100 and "celestial blade" not in player["held_weapon"]:
				print(f"\nThe skies open up and you hear a deep, entrancing voice slowly say:\n'Good job slaying 100 enemies, {player['name']}!' I, the Great Celestial Titan, bestow upon thee the Celestial Blade, the sword that was thrust into the heart of the Great Destroyer, spilling the blood that created this realm during the great war of the titans.")
				print("'Now, go on and defeat the Fallen Titan who slumbers in the ominous dungeon!'")
				player["held_weapon"] = ["celestial blade"]
			elif "basic stick" in player["held_weapon"] or "blade of cinders" in player["held_weapon"] and player["enemy_slain"] < 100:
				world["loc"] = "town_square"
			showTown(world, player)
		if world["loc"] == "mysterious_cavern":
			showCavern(world, player)
		if world["loc"] == "shop":
			showShop(world, player)
		if world["loc"] == "tavern":
			showTavern(world, player)
		if world["loc"] == "ominous_dungeon":
			showOminousDungeon(world, player)
		if player["HP"] <= 0:
			print(f"{player['name']} has been defeated.")
			playerDeath(world, player)
			print("Game Over.")
			print("Thanks for playing!")
			break
		elif fallen_titan["hp"] <= 0:
			print("You defeated the Fallen Titan!")
			print(f"You gained 1000G for defeating the Fallen Titan!")
			player["current_G"] += 1000
			gameWinSave(world, player)
			print("You Win!\nThanks for playing!")
			break

main()
