from tic_tac_toe import *
import numpy as np
import random


def main():
    a = Player('Biatti')
    b = Player('Mary')

    Game1 = TicTacToeGame(a,b)
    print(Game1.game_intro())



if __name__ == '__main__':
    main()