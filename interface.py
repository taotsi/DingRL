from board import Ding_TK
from player import SuperGamer
import pandas as pd
from time import time
import sys

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


def game_on():

    t0 = time()
    while True:
        # print('--------------------------------------------------------------')
        board0.cnt += 1
        dt = time() - t0
        print('| round', board0.cnt, '| time: ',
              round(dt, 1), 's | speed:', round((board0.cnt / dt), 1),
              'r/s | w:b -> ', gamer_w.cnt_win, ':', gamer_w.cnt_lose,
              '|        ',
              end='\r')

        board0.tk_reset()

        piece_w, aw0, aw0_q, s0, is_deadend_w = gamer_w.choose_action(
            SIDE_WHITE, board0.players[SIDE_WHITE], board0.grids)
        st_kill_w, st_over_w = board0.tk_move(SIDE_WHITE, piece_w, aw0)

        piece_b, ab0, ab0_q, s1, is_deadend_b = gamer_b.choose_action(
            SIDE_BLACK, board0.players[SIDE_BLACK], board0.grids)
        st_kill_b, st_over_b = board0.tk_move(SIDE_BLACK, piece_b, ab0)

        while True:
            st_kill_w = st_win_w = 0
            st_kill_b = st_win_b = 0

            # state 2 at the moment
            piece_w, aw1, aw1_q, s2, is_deadend_w = gamer_w.choose_action(
                SIDE_WHITE, board0.players[SIDE_WHITE], board0.grids)

            if not is_deadend_w:
                # now move to state 3
                st_kill_w, st_win_w = board0.tk_move(SIDE_WHITE, piece_w, aw1)

                gamer_w.learn_reward(st_kill_w, st_win_w, s2, aw1_q)
                gamer_w.learn_experience(s0, aw0_q, s2)

            else:
                st_win_w = ST_LOSE
                gamer_w.learn_deadend(s0, aw0_q)

            gamer_b.learn_reward(-st_kill_w, -st_win_w, s1, ab0_q)

            if st_win_w or is_deadend_w:
                break

            # state 3 at the moment
            piece_b, ab1, ab1_q, s3, is_deadend_b = gamer_b.choose_action(
                SIDE_BLACK, board0.players[SIDE_BLACK], board0.grids)

            if not is_deadend_b:
                # now move to state 4, which will be state 2 next turn
                st_kill_b, st_win_b = board0.tk_move(SIDE_BLACK, piece_b, ab1)

                gamer_b.learn_reward(st_kill_b, st_win_b, s3, ab1_q)
                gamer_b.learn_experience(s1, ab0_q, s3)

            else:
                st_win_b = ST_LOSE
                gamer_b.learn_deadend(s1, ab0_q)

            gamer_w.learn_reward(-st_kill_b, -st_win_b, s2, aw1_q)

            if st_win_b or is_deadend_b:
                break

            s0 = s2
            s1 = s3
            aw0_q = aw1_q
            ab0_q = ab1_q


if __name__ == "__main__":

    gamer_w = SuperGamer(rwd_kill=20, rwd_win=100, rwd_killed=-5, rwd_lose=-25,
                         e_greedy=0.9, filename='qw.csv')
    gamer_b = SuperGamer(rwd_kill=5, rwd_win=25, rwd_killed=-20, rwd_lose=-100,
                         e_greedy=0.9, filename='qb.csv')

    board0 = Ding_TK()
    board0.after(100, game_on)
    board0.mainloop()

    # gamer_w.save_q()
    # gamer_b.save_q()

    # print(gamer_w.q_table)
    # print(gamer_b.q_table)

    # with open('wq', 'w') as fwq:
    #     fwq.write(str(gamer_w.q_table))

    # gamer_w.q_table.to_csv('wq.csv')
