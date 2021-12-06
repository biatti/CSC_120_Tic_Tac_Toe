import numpy as np
import random


class Player(object):
    def __init__(self, user):
        self.user = user
        self._wins = 0
        self._loss = 0
        self._wallet = 1000
        self._wager = 0


    def __str__(self):
        return f'Player: {self.user} with {self._wins} wins, {self._loss} losses'

    def get_wins(self):
        return self._wins

    def get_loss(self):
        return self._loss

    def get_wager(self):
        return self._wager

    def reset_wager(self):
        self._wager = 0

    def get_balance(self):
        return self._wallet

    def wager(self, amount):
        if amount <= self._wallet:
            self._wallet = self._wallet - amount
            self._wager = amount
        else:
            print('Insufficient Balance!')


class TicTacToeGame():
    game_lock = False

    def __init__(self, player1, player2):

        self._p1 = player1
        self._p2 = player2
        self._winner = ''
        self._wager = self.check_wager()
        self._bonus = self.set_bonus()
        self._total_prize = self._wager + self._bonus
        self._turn = self._p1
        self._markers = {self._p1.user: 'X',
                         self._p2.user: 'O'}
        self._board = self.set_new_game()
        self._game_intro = self.game_intro()
        self._game_history = self._board

    def game_intro(self):
        return f'Welcome {self._p1.user} and {self._p2.user}!\n' \
               f'${self._wager} have been waged by the players\n' \
               f'${self._bonus} have been set aside as a bonus for the victor\n' \
               f'${self._total_prize} is the total prize money!\n\n' \
               f'Board Preview:\n' \
               f'{self._board}'

    def set_new_game(self):
        "sets a new board"
        if not self.game_lock:
            game = np.empty([3, 3], dtype=str)
            game.fill('-')
            return game

    def check_wager(self):
        """Checks to see if wagers match between players"""
        p1 = self._p1.get_wager()
        p2 = self._p2.get_wager()
        if p1 == p2:
            total = p1 + p2
            self._p1.reset_wager()
            self._p2.reset_wager()
            return total
        else:
            raise ValueError

    def move(self, row, col):
        if not self.get_lock_status():
            my_marker = self._markers[self._turn.user]
            move_ok = False

            if self._board.item(row,col) == '-':
                move_ok = True
                self._board[row,col] = my_marker
                self.check_victory()
                self.change_turn()
            else:
                print('Bad Move - Board Occupied in that position')

            self.check_victory(row, col)

        else:
            print('Game is locked')

    def change_turn(self):
        if self._turn == self._p1:
            self._turn = self._p2
        elif self._turn == self._p2:
            self._turn = self._p1

    def surrender(self, player):
        if player.user == self._p1.user:
            self.set_victor(self._p2)
        elif player.user == self._p2.user:
            self.set_victor(self._p1)

    def set_bonus(self):
        bonus = random.randint(100, 5000)
        return bonus

    def check_victory(self, move):

        win_conditions = {self._board[0:3].count('X') == 3: self._p1,
                          self._board[3:6].count('X') == 3: self._p1,
                          self._board[6:9].count('X') == 3: self._p1,
                          self._board[0:7,3].count('X') == 3: self._p1,
                          self._board[1:8,3].count('X') == 3: self._p1,
                          self._board[2:9,3].count('X') == 3: self._p1,
                          self._board[0:9,4].count('X') == 3: self._p1,
                          self._board[2:8,2].count('X') == 3: self._p1,
                          self._board[0:3].count('O') == 3: self._p1,
                          self._board[3:6].count('O') == 3: self._p1,
                          self._board[6:9].count('O') == 3: self._p1,
                          self._board[0:7,3].count('O') == 3: self._p1,
                          self._board[1:8,3].count('O') == 3: self._p1,
                          self._board[2:9,3].count('O') == 3: self._p1,
                          self._board[0:9,4].count('O') == 3: self._p1,
                          self._board[2:8,2].count('O') == 3: self._p1,
                          }
        winner = win_conditions.get(True, False)
        if not winner:
            self.set_victor(winner)

    def get_board(self):
        return self._board

    def set_victor(self, winner):
        self.game_lock = True
        self._winner = winner
    def get_lock_status(self):
        return self.game_lock



