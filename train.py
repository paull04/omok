import numpy as np
from random import choice
import tensorflow as tf
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import MeanSquaredError
from model import Model
from game import Game


class Train:
    def __init__(self, n):
        game = Game(n)
        self.env = game
        self.n = game.n
        self.epsilon = 1
        self.gamma = 0.9
        self.opt = Adam()
        self.loss = MeanSquaredError()
        self.model = Model(self.env.n)
        self.r = [list(), list()]
        self.s = [list(), list()]
        self.action = [(x, y) for x in range(self.env.n) for y in range(self.env.n)]
        self.arr = np.zeros([self.n, self.n, 3], dtype=np.float)
        self.cnt = 0

    def apply(self, s, r):
        params = self.model.trainable_variables

        with tf.GradientTape() as t:
            t.watch(params)
            v1, p = self.model(s)
            loss1 = self.loss(r, v1)
            loss2 = -tf.reduce_mean(tf.math.log(p)) * (r - v1)
            loss = (loss1 + loss2)
        grad = t.gradient(loss, params)
        self.opt.apply_gradients(zip(grad, params))

    def step1(self, s):
        self.s[self.env.turn - 1].append(np.array(s, dtype=np.float))
        v, p = self.model(np.array([s, ]))
        action = (0, 0)
        actions = [(x, y) for x in range(self.env.n) for y in range(self.env.n) if self.env.board[x, y] == 0]
        if np.random.rand() < self.epsilon:
            action = choice(actions)
        else:
            v = -1
            for x in range(self.n):
                for y in range(self.n):
                    if p[0, x, y] > v and self.env.board[x, y] == 0:
                        v = p[0, x, y]
                        action = (x, y)
        return action

    def step2(self, action):
        t = self.env.turn - 1
        res = self.env.put(action[0], action[1])
        if res == 1:
            if t == 0:
                self.r[1][-1] = -1
            else:
                self.r[0][-1] = -1

        self.r[t].append(res)

    def step(self):
        for x in range(self.n):
            for y in range(self.n):
                if self.env.board[x, y] == self.env.turn:
                    self.arr[x, y, 0] = 1
                elif self.env.board[x, y] == 0:
                    self.arr[x, y, 2] = 1
                else:
                    self.arr[x, y, 1] = 1
        a = self.step1(self.arr)
        self.step2(a)

    def episode(self):
        while not self.env.finish:
            self.step()
        for r in self.r:
            for x in range(len(r)-1, 0, -1):
                r[x-1] = r[x] * self.gamma
        self.apply(tf.Variable(self.s[0], dtype=tf.float32), tf.Variable(self.r[0], dtype=tf.float32))
        self.apply(tf.Variable(self.s[1], dtype=tf.float32), tf.Variable(self.r[1], dtype=tf.float32))
        self.epsilon *= 0.9
        self.env.init()

    def run(self, e):
        for x in range(e):
            self.episode()
            print(x)

    def save(self, file_name):
        self.model.save_weights(file_name)

    def load(self, file_name):
        self.model.load_weights(file_name)


if __name__ == "__main__":
    agent = Train(19)
    agent.run(100)
    agent.save('fa')

