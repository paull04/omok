import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential, Model as kModel
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Softmax
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.optimizers import Adam


class Model(kModel):
    def __init__(self, n):
        super(Model, self).__init__()
        self.n1 = Conv2D(32, (3, 3), padding="same")
        self.n2 = Conv2D(64, (3, 3), padding="same")
        self.n3 = Conv2D(32, (3, 3), padding="same")
        self.v = Dense(1)
        self.p = Conv2D(1, (3, 3), padding="same")
        self.gamma = 0.9
        self.build([None, n, n, 3])

    def call(self, x, training=None, mask=None):
        x = self.n1(x)
        x = self.n2(x)
        x = self.n3(x)
        p = self.p(x)
        p = Softmax()(tf.reshape(p, [-1, 361]))
        p = tf.reshape(p, [-1, 19, 19])

        return self.v(Flatten()(x)), p


def board_to_input(env, n):
    arr = np.zeros([1, n, n, 3])
    for x in range(n):
        for y in range(n):
            if env.board[x, y] == env.turn:
                arr[0, x, y, 0] = 1
            elif env.board[x, y] == 0:
                arr[0, x, y, 2] = 1
            else:
                arr[0, x, y, 1] = 1
    return arr


def max_rc(n, board, p):
    v = 0
    action = (0, 0)
    for x in range(n):
        for y in range(n):
            if p[x, y] > v and board[x, y] == 0:
                v = p[x, y]
                action = (x, y)
    print(p)
    return action


if __name__=='__main__':
    m = Model(19)
    print(m.summary())
    a, b = m.predict(np.zeros([1, 19, 19, 3]))
    print(a.shape, b.shape)