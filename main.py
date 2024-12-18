# COS 121 Final Project
# Author: Yuuna Pogrebitskiy
# Date: 12/18/2024
from player_data import *
from zones import *
from final_project_gameTools import *

def main():
	player = createPlayer()
	world = {}
	print(f"Welcome to Celestia, {player['name']}!")
	world["loc"] = "town_square"
	
	while True:
		if player["enemy_slain"] == 100:
			print(f"The skies open up and you hear a deep, entrancing voice slowly say:\n'Good job slaying 100 enemies, {player['name']}!' I, the Great Celestial Titan, bestow upon thee the Celestial Blade, the sword that created this realm during the great war of the titans.")
			print("'Now, go on and defeat the fallen titan who slumbers in the ominous dungeon!'")
			player["held_weapon"] = ["celestial blade"]
		if player["HP"] <= 0:
			print(f"{player['name']} has been defeated.")
			playerDeath(world, player)
			print("Game Over.")
			print("Thanks for playing!")
			break
			
		if world["loc"] == "town_square":
			showTown(world, player)
		elif world["loc"] == "mysterious_cavern":
			showCavern(world, player)
		elif world["loc"] == "shop":
			showShop(world, player)
		elif world["loc"] == "tavern":
			showTavern(world, player)
		elif world["loc"] == "ominous_dungeon":
			showOminousDungeon(world, player)

main()
