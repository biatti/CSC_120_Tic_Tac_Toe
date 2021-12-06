from tic_tac_toe import *
import numpy as np
import random


def main():
    a = Player('Biatti')
    b = Player('Mary')
    Game1 = TicTacToeGame(a,b)

    Game1.menu_option()




if __name__ == '__main__':
    main()