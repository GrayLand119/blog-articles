import os
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

import mnist_inference
import mnist_eval

BATCH_SIZE = 100

LEARNING_RATE_BASE = 0.8
LEARNING_RATE_DECAY = 0.99  # 指数衰减法

REGULARIZATION_RATE = 0.0001        # 正则化项的系数
TRAINING_STEPS = 5000               # 实际发现训练5000次的时候准确率已经稳定
MOVING_AVERAGE_DECAY = 0.99         # 滑动平均衰减率

MODEL_SAVE_PATH = "/SaveModels/"
MODEL_NAME = "mnist_model.ckpt"


def train(mnist):
    # 定义输入输出 placeholder
    x = tf.placeholder(tf.float32, [None, mnist_inference.INPUT_NODE], name='x-input')
    y_ = tf.placeholder(tf.float32, [None, mnist_inference.OUTPUT_NODE], name='y-input')

    regularizer = tf.contrib.layers.l2_regularizer(REGULARIZATION_RATE)
    y = mnist_inference.inference(x, regularizer)

    global_step = tf.Variable(0, trainable=False)

    # 设置滑动平均衰减率
    variable_averages = tf.train.ExponentialMovingAverage(MOVING_AVERAGE_DECAY, global_step)
    # 所有神经网络上的变量使用滑动平均
    variable_avg_op = variable_averages.apply(tf.trainable_variables())
    # 计算交叉熵
    cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=y, labels=tf.argmax(y_, 1), name='loss1')
    # 计算交叉熵平均值
    cross_entropy_mean = tf.reduce_mean(cross_entropy)

    loss = cross_entropy_mean + tf.add_n(tf.get_collection("losses"))
    # 设置指数衰减学习率
    learning_rate = tf.train.exponential_decay(LEARNING_RATE_BASE,
                                               global_step,
                                               mnist.train.num_examples / BATCH_SIZE,  # 需要迭代的次数
                                               LEARNING_RATE_DECAY)
    train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss, global_step=global_step)

    # 反向传播更新参数
    # tf.control_dependencies and tf.group 两种机制, 效果等同
    # Method1
    train_op = tf.group(train_step, variable_avg_op)
    # Method2
    # with tf.control_dependencies([train_step, variable_avg_op]):
    #     train_op = tf.no_op(name='train')

    # 初始化持久化对象
    saver = tf.train.Saver()
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())

        for i in range(TRAINING_STEPS):
            xs, ys = mnist.train.next_batch(BATCH_SIZE)
            _, loss_value, step = sess.run([train_op, loss, global_step], feed_dict={x: xs, y_: ys})

            if i % 1000 == 0:
                # 每1000次训练保存一次模型
                print("After %d trainning steps, loss on trainning batch is %g." % (i, loss_value))
                path = os.getcwd() + MODEL_SAVE_PATH + MODEL_NAME
                saver.save(sess, path, global_step=global_step)
                print("Save model to ", path)

        print("Trainning  finished.")

def runTrainning():
    # path = os.getcwd() + "/Resources/MINSTData"
    path = "./Resources/MINSTData"
    print("path = ", path)

    mnist = input_data.read_data_sets(path, one_hot=True)

    print("Training data size: ", mnist.train.num_examples)
    train(mnist)

def runTesting():
    path = "./Resources/MINSTData"
    print("path = ", path)
    mnist_test = input_data.read_data_sets(path, one_hot=True)
    mnist_eval.evaluate(mnist_test)
    pass


if __name__ == '__main__':
    while 1:
        num = input("Please input num: 1-Trainning , 2-Testing, q-quit\n")
        if num == 'q':
            break
        if num == '1':
            runTrainning()
            continue
        if num == '2':
            runTesting()
            continue
        break

