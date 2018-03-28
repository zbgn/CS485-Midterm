# -*- coding: utf-8 -*-
 
"""
This module is the Referee of the Gomoku game.
"""
import os


class Referee:
    """
    The class Referee contain all functions necessary
    to arbitrate the game.
    """
    played = 0

    def __init__(self):
        self.score_white = 0
        self.score_black = 0
        self.case = [[0, 1], [1, 1], [1, 0], [1, -1]]

    def copy_board(self, board):
        """
        Make a copy of the board.
        """
        _ = self
        cop_board = list()
        for j in board:
            to_append = list()
            for i in j:
                to_append.append(i)
            cop_board.append(to_append)
        return cop_board

    def remove_dir(self, direction):
        """
        Remove the direction we have already checked.
        """
        simplified_case = list()
        for case in self.case:
            if not (case[0] == direction[0] and case[1] == direction[1]):
                simplified_case.append(case)
        return simplified_case

    def display_win(self, win, msg=None):
        """
        Inputs:
        -   win     =>  char [w/b/None]

        Outputs:
        -   bool
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        if msg:
            print(msg)
        print('score Black:', self.score_black)
        print('score White:', self.score_white)
        if self.score_white == 10 or win == 'w':
            print('White won.')
            return False
        elif self.score_black == 10 or win == 'b':
            print('Black won.')
            return False
        return True

    def display_score(self, score, player, win, msg=None):
        """
        Inputs:
        -   score   =>  int [0/2]
        -   player  =>  char [w/b]
        -   enemy   =>  char [w/b]
        -   win     =>  char [w/b/None]

        Outputs:
        -   char [w/b]
        -   char [w/b]
        -   bool
        """
        if player == 'w':
            self.score_white += score
        else:
            self.score_black += score
        run = self.display_win(win, msg)
        return run

    def set_stone(self, board, player_color, coord):
        """
        Inputs:
        -   board
        -   player_color  =>  char [w/b]
        -   coord         =>  x,y

        Outputs:
        - board modified or None
        """
        chck, msg = self.is_double3(board, coord, player_color)
        score = 0
        if board[coord[0]][coord[1]] is None and not chck:
            board[coord[0]][coord[1]] = player_color
            score, board, msg = self.capture(board, coord, player_color)
            return board, score, msg
        return None, score, msg

    def capture(self, board, coord, player_color):
        """
        Check if the move make a capture.
        Return the new board and the score.
        """
        _ = self
        score = 0
        enemy = 'b' if player_color == 'w' else 'w'
        case = [[-1, -1], [0, -1], [1, -1], [-1, 0], [0, 0], [1, 0], [-1, 1],
                [0, 1], [1, 1]]
        msg = None
        for i in case:
            if ((coord[0] + 3 * i[0] < 19 and coord[1] + 3 * i[1] < 19) and
                (coord[0] + 3 * i[0] >= 0 and coord[1] + 3 * i[1] >= 0)):
                if (board[coord[0] + 1 * i[0]][coord[1] + 1 * i[1]] == enemy
                        and board[coord[0] + 2 * i[0]][coord[1]
                                                       + 2 * i[1]] == enemy
                        and board[coord[0] + 3 * i[0]][coord[1] + 3 * i[1]] ==
                        player_color):
                    board[coord[0] + 1 * i[0]][coord[1] + 1 * i[1]] = None
                    board[coord[0] + 2 * i[0]][coord[1] + 2 * i[1]] = None
                    score += 2
                    msg = ("White" if player_color == 'w' else
                           "Black") + " has made a capture!"
        return score, board, msg

    def check_double3(self, board, coord, direction, color):
        """
        Check in the precedent alignment of 3, if there any other 3 stones aligned.
        """
        simplified_case = self.remove_dir(direction)
        for coord_yx in coord:
            for case in simplified_case:
                dir_yx = [coord_yx[0] - 4 * case[0], coord_yx[1] - 4 * case[1]]
                cpt = 0
                for j in range(0, 9):
                    new_pos = [
                        dir_yx[0] + j * case[0], dir_yx[1] + j * case[1]
                    ]
                    if ((new_pos[1] > 18 or new_pos[1] < 0)
                            or (new_pos[0] > 18 or new_pos[0] < 0)):
                        continue
                    if board[new_pos[0]][new_pos[1]] == color:
                        cpt = 7 if (cpt == j and cpt > 1) else cpt + 6
                    elif board[new_pos[0]][new_pos[1]] is None:
                        cpt = 0 if (cpt % -100 == 0 and cpt != 0) else cpt + 1
                    else:
                        cpt = -100
                    if cpt >= 20:
                        return (True,
                                "The placement of this stone is not possible."
                                + " (Double three).")
                    elif cpt < 0 and j >= 5:
                        break
        return False, None

    def is_double3(self, board, coord, color):
        """
        Check the double three rule.
        Return True if this rule is NOT respected.
        """
        cop_board = self.copy_board(board)
        cop_board[coord[0]][coord[1]] = color
        for case in self.case:
            dir_yx = [coord[0] - 4 * case[0], coord[1] - 4 * case[1]]
            cpt = 0
            coord_stone = list()
            for i in range(0, 9):
                new_pos = [dir_yx[0] + i * case[0], dir_yx[1] + i * case[1]]
                if not ((new_pos[1] > 18 or new_pos[1] < 0) or
                        (new_pos[0] > 18 or new_pos[0] < 0)):
                    if cop_board[new_pos[0]][new_pos[1]] == color:
                        cpt = 7 if (cpt == i and cpt > 1) else cpt + 6
                        coord_stone.append(new_pos)
                    elif cop_board[new_pos[0]][new_pos[1]] is None:
                        cpt = 0 if (cpt % -100 == 0 and cpt != 0) else cpt + 1
                    else:
                        cpt = -100
                    if cpt == 20:
                        return self.check_double3(cop_board, coord_stone, case,
                                                  color)
                    elif i >= 5 and cpt >= 27:
                        break
        return False, None

    def is_breakable(self, direction, coord, player, board):
        """
        Check if the 5 stones are breakable.
        Return True if so.
        """
        enemy = 'w' if player == 'b' else 'b'
        if (coord[0] == 0 or coord[0] == 18) and (direction[0] == 0
                                                  and direction[1] == -1):
            return False
        elif (coord[1] == 0 or coord[1] == 18) and (direction[0] == -1
                                                    and direction[1] == 0):
            return False
        for i in range(0, 5):
            new_yx = [coord[0] + direction[0] * i, coord[1] + direction[1] * i]
            for case in self.remove_dir([-direction[0], -direction[1]]):
                dir_yx = [new_yx[0] - 2 * case[0], new_yx[1] - 2 * case[1]]
                cpt = 0
                for j in range(0, 5):
                    new_pos = [
                        dir_yx[0] + j * case[0], dir_yx[1] + j * case[1]
                    ]
                    if not ((new_pos[1] > 18 or new_pos[1] < 0) or
                            (new_pos[0] > 18 or new_pos[0] < 0)):
                        if board[new_pos[0]][new_pos[1]] == enemy and (
                                cpt == 0 or cpt == 2):
                            cpt += 3
                        elif ((board[new_pos[0]][new_pos[1]] == enemy
                               and cpt != 1)
                              or (board[new_pos[0]][new_pos[1]] == player
                                  and cpt == 2)
                              or (board[new_pos[0]][new_pos[1]] is None)):
                            cpt = 0
                        elif board[new_pos[0]][new_pos[1]] == player and (
                                cpt <= 1 or cpt >= 3):
                            cpt += 1
                    if cpt == 5:
                        return True
        return False

    def check5(self, board, coord, color):
        """
        Check if 5 stones are aligned.
        Return color of winner, else 0.
        """
        for case in self.case:
            dir_yx = [coord[0] - 4 * case[0], coord[1] - 4 * case[1]]
            cpt = 0
            for i in range(0, 9):
                calculated_x = dir_yx[1] + i * case[1]
                calculated_y = dir_yx[0] + i * case[0]
                if not ((calculated_x > 18 or calculated_x < 0) or
                        (calculated_y > 18 or calculated_y < 0)):
                    if board[calculated_y][calculated_x] == color:
                        cpt += 1
                        if cpt == 5:
                            tup_coord = [calculated_y, calculated_x]
                            opp_dir = [-case[0], -case[1]]
                            if self.is_breakable(opp_dir, tup_coord, color,
                                                 board) is False:
                                return color
                    else:
                        cpt = 0
        return 0
