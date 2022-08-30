from omok import *


class Game(Omok):
    def __init__(self, n):
        super(Game, self).__init__(n)
        self.turn = 1
        self.finish = 0

    def init(self):
        super(Game, self).init()
        self.finish = 0

    def put(self, r, c):
        res = self._put(r, c, self.turn)
        if res == 0:
            return -1
        self.turn = BLACK if self.turn == WHILE else WHILE
        if res == 1:
            return 0
        else:
            self.finish = 1
            return 1

