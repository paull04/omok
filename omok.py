import numpy as np

dx = [0, 0, 1, -1, 1, -1, 1, -1]
dy = [1, -1, 0, 0, 1, -1, -1, 1]
BLACK, WHILE = 1, 2


class Omok:
    def __init__(self, n):
        self.n = n
        self.board = np.zeros([n, n], dtype=np.int)

    def check(self, x, y):
        return 0 <= x < self.n and 0 <= y < self.n

    def init(self):
        self.board = np.zeros_like(self.board, dtype=np.int)

    def _put(self, r, c, turn):
        if not self.check(r, c):
            return 0

        if self.board[r, c]:
            return 0
        self.board[r, c] = turn
        for i in range(0, 8, 2):
            cnt = 1
            for j in range(i, i + 2):
                for k in range(1, 10):
                    nr = k*dx[j] + r
                    nc = k*dy[j] + c
                    if not self.check(nr, nc) or self.board[nr, nc] != turn:
                        break
                    cnt += 1
            if cnt == 5:
                return 2
        return 1

    def put1(self, r, c, turn):
        return self._put(r, c, turn)

    def __str__(self):
        s = ''
        for x in self.board:
            for y in x:
                s += str(y) + ' '
            s += '\n'
        return s


if __name__ == '__main__':
    omok = Omok(19)
    pos = [
        [1, 1],
        [2, 2],
        [3, 3],
        [4, 4],
        [5, 5]
    ]

    for x in pos:
        print(omok.put1(*x, 2))
        print(omok)
