import tkinter as tk
from time import time
import time
import numpy as np
import pandas as pd
import sys


class A():
    def __init__(self, xa=1):
        # print('A')
        # print(xa)
        self.va = 10

    def shit(self):
        print('shit A')

    def p_va(self):
        print(self.va)


class B():
    def __init__(self, xb=3):
        # print('B')
        print(xb)
        self.shit()

    def shit(self):
        print('shit B')


class C(A, B):
    def __init__(self, xc=5):
        super(C, self).__init__()
        print("C")
        print(xc)

    def shit(self):
        super().shit()
        print('shit C')

    def p_v(self):
        print(self.va)


def update():
    print("test 1")
    while True:
        print("test 2")
        c.move(o1, 50, 30)
        w.update()
        time.sleep(0.5)


if __name__ == "__main__":
    # a = A(1)
    # a.p_va()
    # b = B(3)
    # c = C(5)
    # c.p_va()
    # c.p_v()

    # w = tk.Tk()
    # w.title('test')
    # w.geometry('800x600')
    # c = tk.Canvas(w, bg='orange', height=400, width=600)
    # o1 = c.create_oval(0, 0, 20, 20, fill='red')
    # o2 = c.create_oval(200, 200, 250, 250, fill='red')
    # l = [o1, o2]
    # c.pack()
    # w.after(500, update)
    # w.mainloop()

    # a = np.random.rand(1636180, 4, 4)
    # a = np.random.rand(409045, 4, 4)
    # x = a[9999]
    # start = time()
    # if x in a:
    #     print('yes')
    # stop = time()
    # print(stop - start)

    # col = [(1, 2), (3, 4)]
    # df1 = df = pd.DataFrame(columns=col)
    # df.to_csv('t0.csv')
    # df.to_csv('t1.csv')
    # print(df)
    #
    # s0 = pd.Series([3] * 2, index=col, name=0)
    # s1 = pd.Series([2] * 2, index=col, name=0)
    # df = df.append(s0)
    # df = df.append(s1)
    # df.to_csv('t0.csv')
    # df.to_csv('t2.csv')
    #
    # df1 = df1.append(s1)
    # df1.to_csv('t2.csv')
    #
    # print(df)

    # for i in range(0, 10):
    #     fn = 'file {0}'.format(i)
    #     with open(fn, 'w') as fo:
    #         fo.write('file {0}'.format(i))

    # df = pd.read_csv('wq.csv')
    # print(df)
    # df.to_csv('test.csv')

    # print(42)
    # df = pd.read_csv('qw.csv')
    # print(df)

    # insa = A()
    # print(insa.__class__.__name__)
