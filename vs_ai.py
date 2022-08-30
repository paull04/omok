from model import *
from game import *
from omok import BLACK, WHILE


class Agent:
    def __init__(self, n):
        self.model = Model(n)
        self.game = Game(n)
        self.n = n
        self.turn = 1

    def load(self, fa):
        self.model.load_weights(fa)

    def put_human(self, r, c):
        return self.game.put(r, c)

    def put_ai(self):
        arr = board_to_input(self.game, self.n)
        _, p = self.model(arr)
        r, c = max_rc(self.n, self.game.board, p[0])
        return self.game.put(r, c), r, c

    def put(self, r, c):
        for _ in range(2):
            if self.turn & 1:
                res = self.put_human(r, c)
                if res:
                    return res
            else:
                res = self.put_ai()
                if res:
                    return 2
            self.turn = BLACK if self.turn == WHILE else WHILE


if __name__ == "__main__":
    agent = Agent(19)
    agent.load('fa')
    while not agent.game.finish:
        print(agent.game.board)
        r, c = map(int, input().split())
        agent.put(r, c)