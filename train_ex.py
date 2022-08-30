import numpy as np
import tensorflow as tf
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import MeanSquaredError
from model import Model

res = []


def run(env: Env):
    episode = 3000
    gamma = 0.9
    epsilon = 1
    n = env.n
    model = Model(n)
    opt = Adam()
    loss_f = MeanSquaredError()

    def train(a1, s1, s2, r):
        params = model.trainable_variables
        with tf.GradientTape() as t:
            t.watch(params)
            q = tf.reduce_sum(model(s1) * a1, axis=1)
            Qt = r + gamma * tf.reduce_min(model(s2), axis=1)
            loss = loss_f(q, Qt)
        grad = t.gradient(loss, params)
        opt.apply_gradients(zip(grad, params))
        #print(grad)

    for e in range(1, episode+1):
        score = 0
        cnt = 0
        a1s = []
        s1s = []
        s2s = []
        rs = []
        while not env.finished:
            s1 = env.state()
            tmp = np.array([x*inf for x in s1[:n]])
            if epsilon >= 1:
                a1 = np.argmin(np.random.rand(n)+tmp)

            else:
                p = model(np.array([s1, ]))
                a1 = np.argmin(p[0] + tmp)

            r = env.sel(a1)
            s2 = env.state()
            a1s.append(tf.one_hot(a1, n))
            s1s.append(s1)
            s2s.append(s2)
            rs.append(r)
            score += r
            cnt += 1
        res.append(score)
        s1 = np.array(s1s)
        s2 = np.array(s2s)
        r = np.array(rs)
        a1 = np.array(a1s)
        train(a1, s1, s2, r)
        #print(score)
        epsilon *= 0.991
        env.reset()
        print(score)


if __name__ == '__main__':
    run(create_env(4))
    import matplotlib.pyplot as plt
    plt.plot(list(range(0, len(res))), res)
    plt.show()