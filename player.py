import numpy as np
import pandas as pd
import os
import time
# import board

ACT_UP = [-1, 0]
ACT_DOWN = [1, 0]
ACT_RIGHT = [0, 1]
ACT_LEFT = [0, -1]

SIDE_WHITE = 0
SIDE_BLACK = 1

ST_KILL = 1
ST_KILLED = -1
ST_WIN = 1
ST_LOSE = -1

action_space = []
for i in range(0, 4):
    action_space.append(str(i) + 'u')
    action_space.append(str(i) + 'd')
    action_space.append(str(i) + 'l')
    action_space.append(str(i) + 'r')

SAVE_INTER = 512

# action_space = []
# action_space_str = []
# for i in range(0, 4):
#     action_space.append([i] + ACT_UP)
#     action_space.append([i] + ACT_DOWN)
#     action_space.append([i] + ACT_RIGHT)
#     action_space.append([i] + ACT_LEFT)
#
#     action_space_str.append(str([i] + ACT_UP))
#     action_space_str.append(str([i] + ACT_DOWN))
#     action_space_str.append(str([i] + ACT_RIGHT))
#     action_space_str.append(str([i] + ACT_LEFT))


class Brain():
    def __init__(self, learning_rate=0.1, reward_decay=0.9, e_greedy=0.9,
                 rwd_kill=10, rwd_killed=-10, rwd_win=50, rwd_lose=-50,
                 filename='q_table'):
        self.alpha = learning_rate
        self.gamma = reward_decay
        self.epsilon = e_greedy
        # self.action_space = []

        self.rwd_kill = rwd_kill
        self.rwd_win = rwd_win
        self.rwd_killed = rwd_killed
        self.rwd_lose = rwd_lose
        self.cnt_win = 0
        self.cnt_lose = 0

        self.filename = filename
        if os.path.exists(filename):
            self.q_table = pd.read_csv(filename, index_col=0)
            # print('Q table read')
            # time.sleep(0.5)
        else:
            self.q_table = pd.DataFrame(columns=action_space)

        # print('test 3\n', self.q_table)

    def check_usable_action(self, player_data, grids):
        # print('test 1\n', player_data)
        usable_actions = []
        sorted_pieces = []
        coors = sorted(player_data.values())
        for i in range(0, len(coors)):
            [x, y] = coors[i]

            for key, value in player_data.items():
                if value == [x, y]:
                    sorted_pieces.append(value)

            if x != 0:
                if grids[x - 1][y] == 0:
                    usable_actions.append([i] + ACT_UP)
            if x != 3:
                if grids[x + 1][y] == 0:
                    usable_actions.append([i] + ACT_DOWN)
            if y != 0:
                if grids[x][y - 1] == 0:
                    usable_actions.append([i] + ACT_LEFT)
            if y != 3:
                if grids[x][y + 1] == 0:
                    usable_actions.append([i] + ACT_RIGHT)
        return usable_actions, sorted_pieces

    def flip_action(self, flip_status, action):
        fliped_action = [piece_n, dx, dy] = action
        if 'v' in flip_status:
            dy = -dy
        if 'h' in flip_status:
            dx = -dx
        if 'T' in flip_status:
            temp = dx
            dx = dy
            dy = temp
        return fliped_action

    def flip_gird(self, flip_status, grid):
        fliped_grid = grid
        if 'T' in flip_status:
            fliped_grid = fliped_grid.T
        if 'v' in flip_status:
            fliped_grid = np.flip(fliped_grid, 0)
        if 'h' in flip_status:
            fliped_grid = np.flip(fliped_grid, 1)
        return fliped_grid

    def check_state(self, side, player_data, grid_frame):
        if side == SIDE_BLACK:
            grid_frame = -grid_frame

        usable_actions, sorted_pieces = self.check_usable_action(
            player_data, grid_frame)

        flip_status = 'none'
        is_found = False
        grid_dic = {}
        grid_dic['none'] = grid_frame
        grid_dic['v'] = np.flip(grid_frame, 0)
        grid_dic['h'] = np.flip(grid_frame, 1)
        grid_dic['vh'] = np.flip(np.flip(grid_frame, 0), 1)
        grid_dic['T'] = grid_frame.T
        grid_dic['Tv'] = np.flip(grid_frame.T, 0)
        grid_dic['Th'] = np.flip(grid_frame.T, 1)
        grid_dic['Tvh'] = np.flip(np.flip(grid_frame.T, 0), 1)

        for key, value in grid_dic.items():
            if str(value) in self.q_table.index:
                flip_status = key
                # temp_grid = grid_dic[key]
                is_found = True
                break

        # print('test 2\n', self.q_table.columns)

        if is_found is True:
            fliped_usable_actions = []
            for action in usable_actions:
                fliped_usable_actions.append(
                    self.flip_action(flip_status, action))
            return grid_dic[flip_status], flip_status, \
                fliped_usable_actions, sorted_pieces

        else:
            self.q_table = self.q_table.append(
                pd.Series([0] * 16,
                          index=self.q_table.columns,
                          name=str(grid_frame)))
            return grid_dic['none'], flip_status, \
                usable_actions, sorted_pieces

    def choose_action(self, side, player_data, grid_frame):
        state, flip_status, usable_actions, sorted_pieces = self.check_state(
            side, player_data, grid_frame)
        state_str = str(state)

        is_deadend = False
        if not usable_actions:
            is_deadend = True
            return 'none', 'none', 'none', 'none', is_deadend
        else:
            usable_actions_str = []
            for a in usable_actions:
                if a[-2:] == [-1, 0]:       # up
                    act = 'u'
                elif a[-2:] == [1, 0]:      # down
                    act = 'd'
                elif a[-2:] == [0, 1]:      # right
                    act = 'r'
                elif a[-2:] == [0, -1]:     # left
                    act = 'l'
                usable_actions_str.append(str(a[0]) + act)

            if np.random.rand() < self.epsilon:
                state_action = self.q_table.loc[state_str, usable_actions_str]
                state_action = state_action.reindex(
                    np.random.permutation(state_action.index))
                # ======================================================= #
                action_str = state_action.argmax()
                # ======================================================= #
            else:
                action_str = np.random.choice(usable_actions_str)

            if action_str[1] == 'u':
                act = [-1, 0]
            elif action_str[1] == 'd':
                act = [1, 0]
            elif action_str[1] == 'r':
                act = [0, 1]
            elif action_str[1] == 'l':
                act = [0, -1]
            action = [int(list(action_str)[0])] + act
            # print('test 6\n', action)

            if flip_status:
                action = self.flip_action(flip_status, action)

            piece_coor = sorted_pieces[action[0]]
            for key, value in player_data.items():
                if value == piece_coor:
                    piece_n = key

        # print('test 17 ', player_data)
        # print('test 17 ', piece_n)
        return piece_n, action[-2:], action_str, state_str, is_deadend

    def learn(self, *args):
        pass


class QL(Brain):
    def __init__(self, learning_rate=0.1, reward_decay=0.9, e_greedy=0.9,
                 rwd_kill=10, rwd_killed=-10, rwd_win=50, rwd_lose=-50):
        super().__init__(learning_rate, reward_decay, e_greedy,
                         rwd_kill, rwd_killed, rwd_win, rwd_lose)

    def learn(self, is_over, state_old, action_old, reward, state_next):
        q_old = self.q_table.loc[state_old, action_old]

        if is_over:
            q_correct = reward
        else:
            q_correct = reward + self.gamma * \
                self.q_table.loc[state_next, :].max()

        self.q_table.loc[state_old,
                         action_old] += self.alpha * (q_correct - q_old)


class Sarsa(Brain):
    def __init__(self, learning_rate=0.1, reward_decay=0.9, e_greedy=0.9,
                 rwd_kill=10, rwd_killed=-10, rwd_win=50, rwd_lose=-50):
        super().__init__(learning_rate, reward_decay, e_greedy,
                         rwd_kill, rwd_killed, rwd_win, rwd_lose)

    def learn(self, is_over, state_old, action_old, reward,
              state_next, action_next):
        q_old = self.q_table.loc[state_old, action_old]

        if is_over:
            q_correct = reward
        else:
            q_correct = reward + self.gamma * \
                self.q_table.loc[state_next, action_next]

        self.q_table.loc[state_old,
                         action_old] += self.alpha * (q_correct - q_old)


class Manual(QL, Sarsa):
    def __init__(self):
        pass


class SuperGamer(Brain):
    def __init__(self, learning_rate=0.1, reward_decay=0.9, e_greedy=0.9,
                 rwd_kill=10, rwd_killed=-10, rwd_win=50, rwd_lose=-50,
                 filename='q_table'):
        super().__init__(learning_rate, reward_decay, e_greedy,
                         rwd_kill, rwd_killed, rwd_win, rwd_lose,
                         filename)

    def save_q(self):
        self.q_table.to_csv(self.filename)

    def learn_experience(self, state_old, action_old, state_new):
        q_old = self.q_table.loc[state_old][action_old]
        # =============================================================== #
        q_correct = self.gamma * self.q_table.loc[state_new, :].max()
        # =============================================================== #
        self.q_table.loc[state_old][action_old] += self.alpha * \
            (q_correct - q_old)

    def learn_reward(self, st_kill, st_win, state, action):
        q_old = self.q_table.loc[state][action]
        q_correct = 0

        if st_win:
            if st_win == ST_WIN:
                q_correct += self.rwd_win
                self.cnt_win += 1
            elif st_win == ST_LOSE:
                q_correct += self.rwd_lose
                self.cnt_lose += 1

            if not (self.cnt_win + self.cnt_lose) % SAVE_INTER:
                self.save_q()
                # print('\nQ table saving...')
                # time.sleep(0.5)

        if st_kill:
            if st_kill == ST_KILL:
                q_correct += self.rwd_kill
            elif st_kill == ST_KILLED:
                q_correct += self.rwd_killed

        self.q_table.loc[state, action] += self.alpha * (q_correct - q_old)

    def learn_deadend(self, state_old, action_old):
        q_old = self.q_table.loc[state_old][action_old]
        q_correct = self.rwd_lose
        self.q_table.loc[state_old][action_old] += self.alpha * \
            (q_correct - q_old)
        self.cnt_lose += 1
        if not (self.cnt_win + self.cnt_lose) % SAVE_INTER:
            self.save_q()
            # print('Q table saving...')
            # time.sleep(0.5)


if __name__ == "__main__":
    p = Brain()
