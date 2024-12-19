from final_project_gameTools import *
# get player name
# set character limit to between 3 and 12
# if inputted # of characters < 3 or > 12, tell the player
# that their chosen name is too long or short
# parameters: none
# returns: dictionary containing player data
def createPlayer():# dictionary that contains all player information
	# get name input from user
	while True:
		playerName = input("Enter the name of your character (between 3 and 12 characters): ")
		playerName = playerName.upper().strip()
		if len(playerName) >= 3 and len(playerName) <= 12:
			correct_playerName = playerName
			break
		if len(playerName) < 3:
			print("Your character's name is too short!")
		if len(playerName) > 12:
			print("Your character's name is too long!")
	player = {
		"name": correct_playerName, 
		"maxHP": 50,
		"HP": 50,
		"held_weapon": ["basic stick"],
		"current_G": 0, 
		"atk": 0,
		"def": 0,
		"enemy_slain": 0, 
		"inventory": {
			
		}
	}
			
	return player
	
# function to save player data to txt file upon death
def playerDeath(world, player):
	with open("current_data.txt", "a") as file:
		save_player = file.write(f"\nFinal player data: player name: {player['name']}\nplayer inventory: {player['inventory']}\nG: {player['current_G']}\natk: {player['atk']}\ndef: {player['def']}\nheld weapon: {player['held_weapon']}\nenemies slain: {player['enemy_slain']}\n")

def gameWinSave(world, player):
	with open("current_data.txt", "a") as file:
		save_player = file.write(f"\nFinal player data: player name: {player['name']}\nplayer inventory: {player['inventory']}\nG: {player['current_G']}\natk: {player['atk']}\ndef: {player['def']}\nheld weapon: {player['held_weapon']}\nenemies slain: {player['enemy_slain']}\n")
