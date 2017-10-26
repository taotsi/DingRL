from board import Ding
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

N_ROUND = 20000


def game_on():

    t0 = time()
    # while True:
    for i in range(0, N_ROUND):

        board1.cnt += 1
        dt = time() - t0
        print('| round', board1.cnt, '| time: ',
              round(dt / 60, 1), 'min | speed:', round((board1.cnt / dt), 1),
              'r/s | w:b -> ', gamer_w.cnt_win, ':', gamer_w.cnt_lose,
              '|        ',
              end='\r')

        board1.reset()

        piece_w, aw0, aw0_q, s0, is_deadend_w = gamer_w.choose_action(
            SIDE_WHITE, board1.players[SIDE_WHITE], board1.grids)
        st_kill_w, st_over_w = board1.move(SIDE_WHITE, piece_w, aw0)

        piece_b, ab0, ab0_q, s1, is_deadend_b = gamer_b.choose_action(
            SIDE_BLACK, board1.players[SIDE_BLACK], board1.grids)
        st_kill_b, st_over_b = board1.move(SIDE_BLACK, piece_b, ab0)

        while True:
            st_kill_w = st_win_w = 0
            st_kill_b = st_win_b = 0

            piece_w, aw1, aw1_q, s2, is_deadend_w = gamer_w.choose_action(
                SIDE_WHITE, board1.players[SIDE_WHITE], board1.grids)

            if not is_deadend_w:
                st_kill_w, st_win_w = board1.move(SIDE_WHITE, piece_w, aw1)

                gamer_w.learn_reward(st_kill_w, st_win_w, s2, aw1_q)
                gamer_w.learn_experience(s0, aw0_q, s2)

            else:
                st_win_w = ST_LOSE
                gamer_w.learn_deadend(s0, aw0_q)

            gamer_b.learn_reward(-st_kill_w, -st_win_w, s1, ab0_q)

            if st_win_w or is_deadend_w:
                break

            piece_b, ab1, ab1_q, s3, is_deadend_b = gamer_b.choose_action(
                SIDE_BLACK, board1.players[SIDE_BLACK], board1.grids)

            if not is_deadend_b:
                # now move to state 4, which will be state 2 next turn
                st_kill_b, st_win_b = board1.move(SIDE_BLACK, piece_b, ab1)

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
    print('loading...')

    gamer_w = SuperGamer(rwd_kill=20, rwd_win=100, rwd_killed=-5, rwd_lose=-25,
                         e_greedy=0.8, filename='qw.csv')
    gamer_b = SuperGamer(rwd_kill=5, rwd_win=25, rwd_killed=-20, rwd_lose=-100,
                         e_greedy=0.8, filename='qb.csv')

    board1 = Ding()

    print('game on, for {0} rounds'.format(N_ROUND))
    game_on()

    print('\nsaving and quiting...')
    gamer_w.save_q()
    gamer_b.save_q()
