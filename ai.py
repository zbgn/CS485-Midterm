# -*- coding: utf-8 -*-
"""
This module is the AI of the Gomoku game.
"""

from referee import Referee


def ai_play(board, color):
    """
    Return the move done by the AI.
    """
    copied_board = list()
    for j in board:
        to_append = list()
        for i in j:
            to_append.append(i)
        copied_board.append(to_append)
    return ai_alpha_beta(copied_board, color, 0, float('-Inf'), float('Inf'))


def ai_check_win(board, coord, color, depth):
    """
    Check if the move made the AI win.
    """
    coord_x = coord[0]
    coord_y = coord[1]
    ref = Referee()
    if ref.check5(board, coord, color):
        board[coord_y][coord_x] = None
        if not depth:
            return True
        return False
    return False


def ai_check_pos(board, coord):
    """
    Check if the position is nearby another stone.
    """
    for coord_y in range(coord[0] - 1, coord[0] + 2):
        for coord_x in range(coord[1] - 1, coord[1] + 2):
            if not ((coord_x > 18 or coord_x < 0) or
                    (coord_y > 18 or coord_y < 0)):
                if board[coord_y][coord_x] is not None:
                    return True
    return False


def ai_alpha_beta(board, color, depth, alpha, beta):
    """
    Algo min-max with calibration alpha-beta
    """
    if depth == 3:
        return ai_estimate(board) if color == 'b' else -ai_estimate(board)
    best = float('-Inf')
    estim = 0
    play = None
    enemy = 'b' if color == 'w' else 'w'
    for coord_y in range(0, 19):
        for coord_x in range(0, 19):
            if board[coord_y][coord_x] is not None:
                continue
            if not ai_check_pos(board, [coord_y, coord_x]):
                continue
            if not play:
                play = [coord_y, coord_x]
            board[coord_y][coord_x] = color
            if ai_check_win(board, [coord_y, coord_x], color, depth):
                board[coord_y][coord_x] = None
                return [coord_y, coord_x] if not depth else float('Inf')
            estim = -ai_alpha_beta(board, enemy, depth + 1, -beta, -alpha)
            if estim > best:
                best = estim
                if best > alpha:
                    alpha = best
                    play = [coord_y, coord_x]
                    if alpha >= beta:
                        board[coord_y][coord_x] = None
                        return play if not depth else best
            board[coord_y][coord_x] = None
    if not depth:
        return play
    elif play:
        return best
    return 0


def ai_estimate(board):
    """
    Return an estimation of the position.
    """
    estimation = 0
    for coord_y in range(0, 19):
        for coord_x in range(0, 19):
            if board[coord_y][coord_x] is None:
                continue
            if board[coord_y][coord_x] == 'b':
                estimation += ai_analyse(board, coord_x, coord_y)
            elif board[coord_y][coord_x] == 'w':
                estimation -= ai_analyse(board, coord_x, coord_y)
    return estimation


def ai_diagonal2_analyse(board, coord_x, coord_y, color):
    """
    Analyse the board (diagonal ymax->ymin;xmin->xmax)
    Called by ai_analyse
    """
    cpt = 0
    bonus = 0
    i = coord_x
    j = coord_y
    while i > 0 and j < 18:
        i -= 1
        j += 1
        if board[j][i] is None:
            cpt += 1
        elif board[j][i] == color:
            cpt += 1
            bonus += 1
        else:
            i = 0
    center = cpt
    cpt += 1
    i = coord_x
    j = coord_y
    while i < 18 and j > 0:
        i += 1
        j -= 1
        if board[j][i] is None:
            cpt += 1
        elif board[j][i] == color:
            cpt += 1
            bonus += 1
        else:
            i = 19
    if cpt >= 5:
        return cpt + bonus + (1 - abs(center / (cpt - 1) - 0.5)) * cpt * 2
    return 0


def ai_diagonal1_analyse(board, coord_x, coord_y, color):
    """
    Analyse the board (diagonal ymin->ymax;xmin->xmax)
    Called by ai_analyse
    """
    cpt = 0
    bonus = 0
    i = coord_x
    j = coord_y
    while i > 0 and j > 0:
        i -= 1
        j -= 1
        if board[j][i] is None:
            cpt += 1
        elif board[j][i] == color:
            cpt += 1
            bonus += 1
        else:
            i = 0
    center = cpt
    cpt += 1
    i = coord_x
    j = coord_y
    while i < 18 and j < 18:
        i += 1
        j += 1
        if board[j][i] is None:
            cpt += 1
        elif board[j][i] == color:
            cpt += 1
            bonus += 1
        else:
            i = 19
    if cpt >= 5:
        return cpt + bonus + (1 - abs(center / (cpt - 1) - 0.5)) * cpt * 2
    return 0


def ai_horizontal_analyse(board, coord_x, coord_y, color):
    """
    Analyse the board (horizontal)
    Called by ai_analyse
    """
    cpt = 0
    bonus = 0
    chck = False
    center = 0
    for i in range(0, 19):
        if i == coord_x:
            center = cpt
            cpt += 1
            chck = True
            continue
        if board[coord_y][i] is None:
            cpt += 1
        elif board[coord_y][i] == color:
            cpt += 1
            bonus += 1
        else:
            if chck:
                i = 19
            else:
                cpt = 0
                bonus = 0
    if cpt >= 5:
        return cpt + bonus + (1 - abs(center / (cpt - 1) - 0.5)) * cpt * 2
    return 0


def ai_vertical_analyse(board, coord_x, coord_y, color):
    """
    Analyse the board (vertical)
    Called by ai_analyse
    """
    cpt = 0
    bonus = 0
    chck = False
    center = 0
    for j in range(0, 19):
        if j == coord_y:
            center = cpt
            cpt += 1
            chck = True
            continue
        if board[j][coord_x] is None:
            cpt += 1
        elif board[j][coord_x] == color:
            cpt += 1
            bonus += 1
        else:
            if chck:
                j = 19
            else:
                cpt = 0
                bonus = 0
    if cpt >= 5:
        return cpt + bonus + (1 - abs(center / (cpt - 1) - 0.5)) * cpt * 2
    return 0


def ai_check4_analyse(board, coord, color):
    """
    Check if 4 allies stones are aligned.
    """
    estimation = 0
    ref = Referee()
    for case in ref.case:
        dir_yx = [coord[0] - 4 * case[0], coord[1] - 4 * case[1]]
        cpt = 0
        for i in range(0, 9):
            calculated_x = dir_yx[1] + i * case[1]
            calculated_y = dir_yx[0] + i * case[0]
            if not ((calculated_x > 18 or calculated_x < 0) or
                    (calculated_y > 18 or calculated_y < 0)):
                if board[calculated_y][calculated_x] == color:
                    cpt += 1
                    if cpt == 4:
                        estimation += 500 * Referee.played
                else:
                    cpt = 0
    return estimation


def ai_check3_analyse(board, coord, color):
    """
    Check if 3 enemy stones are aligned.
    """
    enemy = 'b' if color == 'w' else 'w'
    estimation = 0
    ref = Referee()
    for case in ref.case:
        dir_yx = [coord[0] - 3 * case[0], coord[1] - 3 * case[1]]
        cpt = 0
        for i in range(0, 7):
            calculated_x = dir_yx[1] + i * case[1]
            calculated_y = dir_yx[0] + i * case[0]
            if not ((calculated_x > 18 or calculated_x < 0) or
                    (calculated_y > 18 or calculated_y < 0)):
                if board[calculated_y][calculated_x] == enemy:
                    cpt += 1
                    if cpt == 3:
                        estimation += 1000 * Referee.played
                else:
                    cpt = 0
    return estimation


def ai_capture_analyse(board, coord, color):
    """
    Estimate the capture move
    """
    estimation = 0
    enemy = 'b' if color == 'w' else 'w'
    case = [[-1, -1], [0, -1], [1, -1], [-1, 0], [0, 0], [1, 0], [-1, 1],
            [0, 1], [1, 1]]
    for i in case:
        if ((coord[0] + 3 * i[0] < 19 and coord[1] + 3 * i[1] < 19)
                and (coord[0] + 3 * i[0] >= 0 and coord[1] + 3 * i[1] >= 0)):
            if (board[coord[0] + 1 * i[0]][coord[1] + 1 * i[1]] == enemy and
                    board[coord[0] + 2 * i[0]][coord[1] + 2 * i[1]] == enemy
                    and
                    board[coord[0] + 3 * i[0]][coord[1] + 3 * i[1]] == color):
                estimation += 800 * Referee.played
    return estimation


def ai_analyse(board, coord_x, coord_y):
    """
    Calcul the possibility
    """
    color = board[coord_y][coord_x]
    estimation = 0
    estimation += ai_vertical_analyse(board, coord_x, coord_y, color)
    estimation += ai_horizontal_analyse(board, coord_x, coord_y, color)
    estimation += ai_diagonal1_analyse(board, coord_x, coord_y, color)
    estimation += ai_diagonal2_analyse(board, coord_x, coord_y, color)
    estimation += ai_check3_analyse(board, [coord_y, coord_x], color)
    estimation += ai_check4_analyse(board, [coord_y, coord_x], color)
    ref = Referee()
    estimation += ai_capture_analyse(board, [coord_y, coord_x], color)
    chck, text = ref.is_double3(board, [coord_y, coord_x], color)
    _ = text
    if chck:
        estimation = 0
    return estimation
