import numpy as np
import tkinter as tk
import time

'''
grids' data:
_______________________________
   y  0  1  2  3
 x +--------------+
 0 |  1  1  1  1  | White Side
 1 |  0  0  0  0  |
 2 |  0  0  0  0  |
 3 | -1 -1 -1 -1  | Black Side
   +--------------+
'''

ACT_UP = [-1, 0]
ACT_DOWN = [1, 0]
ACT_RIGHT = [0, 1]
ACT_LEFT = [0, -1]

SIDE_WHITE = 0
SIDE_BLACK = 1

GRID_WIDTH = 100
FRAME_WIDTH = 200
ANI_DELAY = 0.8

ST_KILL = 1
ST_KILLED = -1
ST_WIN = 1
ST_LOSE = -1


# data of the pieces are stored in two places:
#   1. self.players keeps records of pieces's coordinates of each side
#   2. self.grids keeps records of the situation of the entire board
#   and everytime data is updated, they must be updated all together


class Ding():
    def __init__(self):
        self.cnt = 0
        self.reset()
        # print(self.players[0])

    def reset(self):
        self.whose_move = SIDE_WHITE

        self.grids = np.zeros((4, 4))
        self.grids[:][0] = np.ones((1, 4))
        self.grids[:][3] = -np.ones((1, 4))

        self.usable_actions = [{}, {}]
        self.usable_actions[0] = {
            'piece_0': [ACT_DOWN], 'piece_1': [ACT_DOWN],
            'piece_2': [ACT_DOWN], 'piece_3': [ACT_DOWN]}
        self.usable_actions[1] = {
            'piece_0': [ACT_UP], 'piece_1': [ACT_UP],
            'piece_2': [ACT_UP], 'piece_3': [ACT_UP]}

        self.players = [{}, {}]
        self.players[0] = {
            'piece_0': [0, 0], 'piece_1': [0, 1],
            'piece_2': [0, 2], 'piece_3': [0, 3]}
        self.players[1] = {
            'piece_0': [3, 0], 'piece_1': [3, 1],
            'piece_2': [3, 2], 'piece_3': [3, 3]}

        return self.grids

    def turn_side(self, side):
        if side == SIDE_WHITE:
            self.whose_move = SIDE_BLACK
        elif side == SIDE_BLACK:
            self.whose_move = SIDE_WHITE

    def player_delete_piece(self, side, x, y):
        for key, value in self.players[side].items():
            if value == [x, y]:
                piece_n = key
        del self.players[side][piece_n]
        return piece_n

    def piece_move(self, side, piece_n, action):
        is_valid = False
        [x, y] = self.players[side][piece_n]
        [x_next, y_next] = [x, y]

        if action == ACT_UP:
            if x != 0 and self.grids[x - 1][y] == 0:
                x_next -= 1
                is_valid = True
        elif action == ACT_DOWN:
            if x != 3 and self.grids[x + 1][y] == 0:
                x_next += 1
                is_valid = True
        elif action == ACT_LEFT:
            if y != 0 and self.grids[x][y - 1] == 0:
                y_next -= 1
                is_valid = True
        elif action == ACT_RIGHT:
            if y != 3 and self.grids[x][y + 1] == 0:
                y_next += 1
                is_valid = True

        return is_valid, x_next, y_next

    def board_move_piece(self, side, piece_n, action):
        is_valid = False
        # print('test 8\n', self.players[side], '\npiece: ', piece_n)
        # print('test 16 ', self.players[side])
        # print('test 16 ', piece_n)

        [x, y] = self.players[side][piece_n]

        if side == 0:
            if piece_n in self.players[0].keys():
                # print('test 14')
                is_valid, x_next, y_next = self.piece_move(
                    side, piece_n, action)
                if is_valid:
                    self.grids[x][y] = 0
                    self.grids[x_next][y_next] = 1
                    self.players[side][piece_n] = [x_next, y_next]
        elif side == 1:
            if piece_n in self.players[1].keys():
                is_valid, x_next, y_next = self.piece_move(
                    side, piece_n, action)
                if is_valid:
                    self.grids[x][y] = 0
                    self.grids[x_next][y_next] = -1
                    self.players[side][piece_n] = [x_next, y_next]

        if is_valid is False:
            print("wrong: board_move_piece")
            # print('test 13\n', side, piece_n, action)
            # print(self.players[0].keys())

        return is_valid

    def rule_enforce(self, side, piece_n):
        is_kill = False
        [x, y] = self.players[side][piece_n]
        side_value = self.grids[x][y]
        if side == 0:
            side_enemy = 1
        elif side == 1:
            side_enemy = 0
        piece_dead = 'none'

        # X, vertically
        if x == 0:
            # (o) o
            if self.grids[x + 1][y] == side_value:
                # (o) o x
                if self.grids[x + 2][y] == -side_value:
                    self.grids[x + 2][y] = 0
                    piece_dead = self.player_delete_piece(side_enemy, x + 2, y)
                    is_kill = True
        elif x == 1:
            # o (o)
            if self.grids[x - 1][y] == side_value:
                # o (o) x
                if self.grids[x + 1][y] == -side_value:
                    self.grids[x + 1][y] = 0
                    piece_dead = self.player_delete_piece(side_enemy, x + 1, y)
                    is_kill = True
            # (o) o
            if self.grids[x + 1][y] == side_value:
                # (o) o x
                if self.grids[x + 2][y] == -side_value:
                    self.grids[x + 2][y] = 0
                    piece_dead = self.player_delete_piece(side_enemy, x + 2, y)
                    is_kill = True
                # x (o) o
                if self.grids[x - 1][y] == -side_value:
                    self.grids[x - 1][y] = 0
                    piece_dead = self.player_delete_piece(side_enemy, x - 1, y)
                    is_kill = True
        elif x == 2:
            # (o) o
            if self.grids[x + 1][y] == side_value:
                # x (o) o
                if self.grids[x - 1][y] == -side_value:
                    self.grids[x - 1][y] = 0
                    piece_dead = self.player_delete_piece(side_enemy, x - 1, y)
                    is_kill = True
            # o (o)
            if self.grids[x - 1][y] == side_value:
                # x o (o)
                if self.grids[x - 2][y] == -side_value:
                    self.grids[x - 2][y] = 0
                    piece_dead = self.player_delete_piece(side_enemy, x - 2, y)
                    is_kill = True
                # o (o) x
                if self.grids[x + 1][y] == -side_value:
                    self.grids[x + 1][y] = 0
                    piece_dead = self.player_delete_piece(side_enemy, x + 1, y)
                    is_kill = True
        elif x == 3:
            # o (o)
            if self.grids[x - 1][y] == side_value:
                # x o (o)
                if self.grids[x - 2][y] == -side_value:
                    self.grids[x - 2][y] = 0
                    piece_dead = self.player_delete_piece(side_enemy, x - 2, y)
                    is_kill = True

        # Y, horizontally
        if y == 0:
            # (o) o
            if self.grids[x][y + 1] == side_value:
                # (o) o x
                if self.grids[x][y + 2] == -side_value:
                    self.grids[x][y + 2] = 0
                    piece_dead = self.player_delete_piece(side_enemy, x, y + 2)
                    is_kill = True
        elif y == 1:
            # o (o)
            if self.grids[x][y - 1] == side_value:
                # o (o) x
                if self.grids[x][y + 1] == -side_value:
                    self.grids[x][y + 1] = 0
                    piece_dead = self.player_delete_piece(side_enemy, x, y + 1)
                    is_kill = True
            # (o) o
            if self.grids[x][y + 1] == side_value:
                # (o) o x
                if self.grids[x][y + 2] == -side_value:
                    self.grids[x][y + 2] = 0
                    piece_dead = self.player_delete_piece(side_enemy, x, y + 2)
                    is_kill = True
                # x (o) o
                if self.grids[x][y - 1] == -side_value:
                    self.grids[x][y - 1] = 0
                    piece_dead = self.player_delete_piece(side_enemy, x, y - 1)
                    is_kill = True
        elif y == 2:
            # (o) o
            if self.grids[x][y + 1] == side_value:
                # x (o) o
                if self.grids[x][y - 1] == -side_value:
                    self.grids[x][y - 1] = 0
                    piece_dead = self.player_delete_piece(side_enemy, x, y - 1)
                    is_kill = True
            # o (o)
            if self.grids[x][y - 1] == side_value:
                # x o (o)
                if self.grids[x][y - 2] == -side_value:
                    self.grids[x][y - 2] = 0
                    piece_dead = self.player_delete_piece(side_enemy, x, y - 2)
                    is_kill = True
                # o (o) x
                if self.grids[x][y + 1] == -side_value:
                    self.grids[x][y + 1] = 0
                    piece_dead = self.player_delete_piece(side_enemy, x, y + 1)
                    is_kill = True
        elif y == 3:
            # o (o)
            if self.grids[x][y - 1] == side_value:
                # x o (o)
                if self.grids[x][y - 2] == -side_value:
                    self.grids[x][y - 2] = 0
                    piece_dead = self.player_delete_piece(side_enemy, x, y - 2)
                    is_kill = True

        return is_kill, side_enemy, piece_dead

    def move(self, side, piece_n, action):
        st_kill = st_win = 0
        if side != self.whose_move:
            print("wrong! it's not your turn. move()")
        else:
            is_valid = self.board_move_piece(side, piece_n, action)
            if is_valid:
                is_kill, side_enemy, piece_dead = self.rule_enforce(
                    side, piece_n)
                self.turn_side(side)
                if is_kill:
                    st_kill = ST_KILL
                if len(self.players[side_enemy]) < 2:
                    st_win = ST_WIN
            else:
                print("failed: board_move_piece()")

        # return is_kill, side_enemy, piece_dead
        return st_kill, st_win


class Ding_TK(tk.Tk, Ding):
    def __init__(self):
        # super(Ding_TK, self).__init__()
        tk.Tk.__init__(self)
        Ding.__init__(self)
        self.tittle = 'Ding'
        self.players_tk = [{}, {}]
        # self.grids_tk = self.grids.T
        self.geometry('{0}x{1}'.format(GRID_WIDTH * 4, GRID_WIDTH * 4))
        self.tk_init_board()
        self.update()

    def tk_init_pieces(self):
        # side 0, white
        for key, value in self.players[0].items():
            [x, y] = value
            oval = self.canvas.create_oval(GRID_WIDTH * (x + 0.2),
                                           GRID_WIDTH * (y + 0.2),
                                           GRID_WIDTH * (x + 0.8),
                                           GRID_WIDTH * (y + 0.8),
                                           fill='white')
            self.players_tk[0][key] = oval
        # side 1, black
        for key, value in self.players[1].items():
            [x, y] = value
            oval = self.canvas.create_oval(GRID_WIDTH * (x + 0.2),
                                           GRID_WIDTH * (y + 0.2),
                                           GRID_WIDTH * (x + 0.8),
                                           GRID_WIDTH * (y + 0.8),
                                           fill='black')
            self.players_tk[1][key] = oval

    def tk_init_board(self):
        self.canvas = tk.Canvas(
            self, bg='orange', height=GRID_WIDTH * 4, width=GRID_WIDTH * 4)

        # draw grid lines
        for col in range(0, 4):
            x0, y0 = col * GRID_WIDTH + GRID_WIDTH * 0.5, GRID_WIDTH * 0.5
            x1, y1 = col * GRID_WIDTH + GRID_WIDTH * 0.5, GRID_WIDTH * 3.5
            self.canvas.create_line(x0, y0, x1, y1, width=4, fill='grey')
        for row in range(0, 4):
            x0, y0 = GRID_WIDTH * 0.5, row * GRID_WIDTH + GRID_WIDTH * 0.5
            x1, y1 = GRID_WIDTH * 3.5, row * GRID_WIDTH + GRID_WIDTH * 0.5
            self.canvas.create_line(x0, y0, x1, y1, width=4, fill='grey')

        self.tk_init_pieces()
        self.canvas.pack()

    def tk_reset(self):
        self.reset()
        for side in range(0, 2):
            for piece_n in self.players_tk[side].keys():
                self.canvas.delete(self.players_tk[side][piece_n])
        self.players_tk = [{}, {}]
        self.tk_init_pieces()
        self.update()

        return self.grids

    def tk_update(self):
        # if self.cnt > 9999:
        #     time.sleep(0.6)
        self.update()
        time.sleep(ANI_DELAY)

    def tk_move_piece(self, side, piece_n, action):
        is_valid = self.board_move_piece(side, piece_n, action)
        dx = action[0]
        dy = action[1]
        if is_valid:
            dx_tk = dx * GRID_WIDTH
            dy_tk = dy * GRID_WIDTH
            self.canvas.move(self.players_tk[side][piece_n], dx_tk, dy_tk)
            self.tk_update()

        return is_valid

    def tk_rule_enforce(self, side, piece_n):
        is_kill, side_enemy, piece_dead = self.rule_enforce(side, piece_n)
        st_kill = st_win = 0
        if is_kill:
            self.canvas.delete(self.players_tk[side_enemy][piece_dead])
            del(self.players_tk[side_enemy][piece_dead])
            self.tk_update()
            st_kill = ST_KILL

        if len(self.players[side_enemy]) < 2:
            st_win = ST_WIN

        return st_kill, st_win

    def tk_move(self, side, piece_n, action):
        # print('test 7\n', action)
        if side != self.whose_move:
            print("wrong! it's not your turn. tk_move()")
        else:
            # print('test 11\n', piece_n, action)
            is_valid = self.tk_move_piece(side, piece_n, action)
            # print('test 12\n', is_valid)
            if is_valid:
                # print('test 12')
                st_kill, st_win = self.tk_rule_enforce(side, piece_n)
                # print('test 13\n', is_kill, is_over)
                self.turn_side(side)
            else:
                print("failed: tk_move()")

        return st_kill, st_win


def test(board):
    board.tk_move_piece(SIDE_WHITE, 'piece_1', ACT_DOWN)
    board.tk_move_piece(SIDE_BLACK, 'piece_1', ACT_UP)
    board.tk_move_piece(SIDE_WHITE, 'piece_2', ACT_LEFT)
    board.tk_rule_enforce(SIDE_WHITE, 'piece_2')


if __name__ == "__main__":

    board = Ding_TK()
    board.after(500, test(board))
    board.mainloop()

    print(board.grids)
    print("side white: ", board.players[0])
    print("side black: ", board.players[1])
