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
    ng_counter = 0
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
        """
        Moves player marker, checks for valid positions
        and winning criteria.

        :param row: row index 0-2
        :param col: col index 0-2
        """
        row = int(row)
        col = int(col)
        if not self.get_lock_status():
            my_marker = self._markers[self._turn.user]
            move_ok = False

            if self._board.item(int(row), int(col)) == '-':
                move_ok = True
                self._board[row, col] = my_marker
                self.check_victory()
                self.check_draw()
                self.change_turn()
            else:
                print('Bad Move - Board Occupied in that position')




        else:
            print('Game is locked')

    def change_turn(self):
        """changes current turn to the opponent"""
        if self._turn == self._p1:
            self._turn = self._p2
        elif self._turn == self._p2:
            self._turn = self._p1

    def surrender(self, player):
        """Forfeit the game and surrender prize money and waged to opponent"""
        if player.user == self._p1.user:
            print(f'{player.user} surrenders')
            self.set_victor(self._p2)
        elif player.user == self._p2.user:
            print(f'{player.user} surrenders')
            self.set_victor(self._p1)

    def set_bonus(self):
        """A random bonus is allocated at the start of each match"""
        bonus = random.randint(100, 5000)
        return bonus

    def check_victory(self):
        """
        Checks for victory conditions and sets victor if applicable

        """
        x = np.char.count(self._board, 'X')
        o = np.char.count(self._board, 'O')

        win_conditions_x = {sum((x.item(0), x.item(1), x.item(2))) == 3: self._p1,
                            sum((x.item(3), x.item(4), x.item(5))) == 3: self._p1,
                            sum((x.item(6), x.item(7), x.item(8))) == 3: self._p1,
                            sum((x.item(0), x.item(3), x.item(6))) == 3: self._p1,
                            sum((x.item(1), x.item(4), x.item(7))) == 3: self._p1,
                            sum((x.item(2), x.item(5), x.item(8))) == 3: self._p1,
                            sum((x.item(0), x.item(4), x.item(8))) == 3: self._p1,
                            sum((x.item(2), x.item(4), x.item(6))) == 3: self._p1,
                            }

        win_conditions_o = {sum((o.item(0), o.item(1), o.item(2))) == 3: self._p2,
                            sum((o.item(3), o.item(4), o.item(5))) == 3: self._p2,
                            sum((o.item(6), o.item(7), o.item(8))) == 3: self._p2,
                            sum((o.item(0), o.item(3), o.item(6))) == 3: self._p2,
                            sum((o.item(1), o.item(4), o.item(7))) == 3: self._p2,
                            sum((o.item(2), o.item(5), o.item(8))) == 3: self._p2,
                            sum((o.item(0), o.item(4), o.item(8))) == 3: self._p2,
                            sum((o.item(2), o.item(4), o.item(6))) == 3: self._p2,

                            }

        winner_x = win_conditions_x.get(True,False)
        winner_o = win_conditions_o.get(True,False)

        if winner_x and winner_o != False:
            raise ValueError(f'Cannot have two winners')
        elif winner_x != False:
            self.set_victor(winner_x)
        elif winner_o !=False:
            self.set_victor(winner_o)


    def check_draw(self):
        count = (self._board == '-').sum()
        if count == 0:
            self.game_lock = True
            self._winner = 'DRAW'
            self._p1._wallet = self._p1._wallet + (self._total_prize / 2)
            self._p2._wallet = self._p2._wallet + (self._total_prize / 2)

    def get_board(self):
        return self._board

    def set_victor(self, winner):
        self.game_lock = True
        self._winner = winner
        winner._wallet = winner._wallet + self._total_prize
        print(f'Congratulations {winner.user}!!\n'
              f'${self._total_prize} prize money has been added to your wallet')
        self.stats_cleanup()

    def get_lock_status(self):
        """returns game lock status.
            Locked games are games that ended and should not be modified further
        """
        return self.game_lock

    def menu_option(self):
        """
        presents user menu options
        """
        option = 0
        while not self.game_lock:
            print(self.menu_info())
            option = input()
            if option == '1':
                try:
                    row = input('Input Row: ')
                    col = input('Input Col: ')
                    self.move(row, col)
                except (IndexError,ValueError) as err:
                    print(f'Please use integers between 0-2 --->{err.args}')
            elif option == '2':
                print(self.get_board())
            elif option == '3':
                self.surrender(self._turn)

    def menu_info(self):
        if self.ng_counter == 0:
            print(self.game_intro())
            self.ng_counter = self.ng_counter + 1
        return f'Player Turn: {self._turn.user} \n' \
               f'Please make a selection:\n\n' \
               f'[1] - Move\n' \
               f'[2] - Show Board\n' \
               f'[3] - Surrender\n'
    def stats_cleanup(self):
        if self.get_lock_status() and not isinstance(self._winner,str):
            self._winner._wins = self._winner._wins + 1
            if self._winner.user == self._p1.user:
                    self._p2._loss = self._p2._loss + 1
            elif self._winner.user == self._p2.user:
                    self._p1._loss = self._p1._loss + 1




