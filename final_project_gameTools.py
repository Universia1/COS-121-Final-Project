from player_data import *
import random

# create a d&d dice roll function that will be used for:
# player HP/max HP
# which enemy spawns in what room
# how much damage is dealt to player/enemy
# parameters: roll_str
# returns: a list containing result of rolls
def diceRoll(roll_str):
	# try to split the string based on 'd'
	try:
		# split the string into num of dice (x) and num of sides (y)
		x, y = roll_str.split('d')
		# list to store results of each roll
		# convert x and y into int
		x = int(x)
		y = int(y)
		rolls_list = []
		for i in range(x):
			rolls = random.randint(1, y)
			rolls_list.append(rolls)
		return rolls_list
	# if input is invaild (causes a ValueError) returns empty list
	except ValueError:
		return []
	return roll_str
