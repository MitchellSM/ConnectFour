"""
@author:    Mitchell Sulz-Martin
@date:      02/24/18

This script will run the neccesary scripts for starting a game of 
    Connect4.
"""

import connect_four as c4


print("\n"*100)
print("------------------------------------------------------")
print("                Welcome to Connect4!")
print("------------------------------------------------------", end='')
game = c4.Connectfour()
game.new_game()