---

title: TensorFlow学习笔记(5) - 完善手写体识别
subtitle: tfln5
date: 2018-08-20 16:49:04
tags: TensorFlow
mathjax: true

---

<!-- # TensorFlow学习笔记(5) - 完善手写体识别 -->

相关代码:

[mnist_eval.py](./mnist_eval.py)[mnist_inference.py](./mnist_inference.py)[mnist_train.py](./mnist_train.py)

之前写的手写体程序没有持久化训练好的模型. 经过上一节持久化的学习后, 现在来优化一下之前的程序. 顺便把各个功能的实现进行模块化拆分.

持久化主要解决问题:

* 程序退出后, 模型无法使用, 即模型无法重用.
* 训练过程中程序挂了, 那么没有保存的中间结果会丢失, 浪费大量时间和资源.

解决办法:

* 训练过程中, 每隔一段时间保存一次模型训练的中间结果.
 

模块: 

* `mnist_inference.py`: 定义向前传播过程, 以及神经网络中的参数.
* `mnist_train.py`: 定义神经网络训练过程
* `mnist_eval.py`: 定义测试过程

为了方便 `函数主程序入口写在`mnist_train.py`中

mnist_inference.py:

```python
import tensorflow as tf


# MNIST 数据集相关的常数
INPUT_NODE = 784            # 图片的像素
LAYER1_NODE = 500           # 第一层参数数量
OUTPUT_NODE = 10            # 识别10个数字


def get_weight_variable(shape, regularizer):
    # 使用 get_variable 函数, 在训练时创建, 测试时加载
    # 因为变量加载重名功能, 在训练时使用变量自身, 在测试时使用变量的滑动平均值
    weights = tf.get_variable('weights', shape, initializer=tf.truncated_normal_initializer(stddev=0.1))

    # 当使用正则化函数时, 将当前变量的正则化损失加入 losses 集合
    if regularizer != None:
        tf.add_to_collection('losses', regularizer(weights))

    return weights


def inference(input_sensor, regularizer):
    """
    定义向前传播过程
    :param input_sensor:入参
    :param regularizer: 正则化表达式
    :return: 向前传播结果
    """
    with tf.variable_scope("layer1"):
        weights = get_weight_variable([INPUT_NODE, LAYER1_NODE], regularizer)
        biases = tf.get_variable('biases', [LAYER1_NODE], initializer=tf.constant_initializer(0.0))
        layer1 = tf.nn.relu(tf.matmul(input_sensor, weights) + biases)

    with tf.variable_scope("layer2"):
        weights = get_weight_variable([LAYER1_NODE, OUTPUT_NODE], regularizer)
        biases = tf.get_variable('biases', [OUTPUT_NODE], initializer=tf.constant_initializer(0.0))
        layer2 = tf.matmul(layer1, weights) + biases

    return layer2


```

`mnist_train.py`:

```python
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
        num = input("Please input num: 1-Trainning , 2-Testing, q-quit:\n")
        if num == 'q':
            break
        if num == '1':
            runTrainning()
            continue
        if num == '2':
            runTesting()
            continue
        break
```

`mnist_eval.py`:

```python
import time
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import os
import mnist_inference
import mnist_train

# Every 10 seconds load leatest model once, then testing
EVAL_INTERVAL_SECS = 10


def evaluate(mnist):
    with tf.Graph().as_default() as g:
        x = tf.placeholder(tf.float32, [None, mnist_inference.INPUT_NODE], name='x-input')
        y_ = tf.placeholder(tf.float32, [None, mnist_inference.OUTPUT_NODE], name='y-input')

        validate_feed = {x: mnist.validation.images,
                         y_: mnist.validation.labels}

        # 向前传播, 计算结果. 测试不关注损失
        y = mnist_inference.inference(x, None)

        # 计算正确率
        correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

        # 加载模型, 并获取滑动平均值
        variable_averages = tf.train.ExponentialMovingAverage(mnist_train.MOVING_AVERAGE_DECAY)
        variable_to_restore = variable_averages.variables_to_restore()
        saver = tf.train.Saver(variable_to_restore)

        with tf.Session() as sess:
            path = os.getcwd() + mnist_train.MODEL_SAVE_PATH
            ckpt = tf.train.get_checkpoint_state(path)
            if ckpt and ckpt.model_checkpoint_path:
                saver.restore(sess, ckpt.model_checkpoint_path)
                global_step = ckpt.model_checkpoint_path.split('/')[-1].split('-')[-1]
                accuracy_score = sess.run(accuracy, feed_dict=validate_feed)
                print("After %s training steps, validation accuracy = %g" % (global_step, accuracy_score))
            else:
                print("No checkpoint file found.")
                return
            pass
```

