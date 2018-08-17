---

title: TensorFlow 学习笔记(2)-手写体识别
subtitle: tfln2
date: 2018-08-15 17:41:38
tags: TensorFlow
mathjax: true

---

<!-- # TensorFlow 学习笔记(2) -->

# 实践-手写体识别

本次内容主要是基于 `TensorFlow 学习笔记(1)` 中的知识, 进行一次实战操作.

[相关代码](./MINSTPractice1.py.py)

## MNIST 数字识别问题

### MNIST 数据处理

`MNIST` 是一个非常有名的手写体数字识别数据集. 它是` NIST` 数据集的一个子集.

### 实践

依赖 `MNIST` 的数据建立了一个手写体识别的训练模型.
用到了全部 TensorFLow 学习笔记(1) 的内容.

```python
from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf
import os


# MNIST 数据集相关的常数
INPUT_NODE = 784            # 图片的像素
OUTPUT_NODE = 10            # 识别10个数字

# 配置神经网络的参数
LAYER1_NODE = 500
BATCH_SIZE = 100

LEARNING_RATE_BASE = 0.8
LEARNING_RATE_DECAY = 0.99  # 指数衰减法

REGULARIZATION_RATE = 0.0001        # 正则化项的系数
TRAINING_STEPS = 5000               # 实际发现训练5000次的时候准确率已经稳定
MOVING_AVERAGE_DECAY = 0.99         # 滑动平均衰减率


# 辅助函数, 计算向前传播的结果
def inference(input_tensor, avg_class, weights1, biases1, weights2, biases2):
    # 没有滑动平均类 直接使用参数当前的取值
    if avg_class == None:
        # 计算向前传播的结果, 使用 ReLU 激活函数 + 去线性化
        layer1 = tf.nn.relu(tf.matmul(input_tensor, weights1) + biases1)
        layer2 = tf.matmul(layer1, weights2) + biases2
        return layer2
    else:
        # 使用 avg_class.average 函数来计算滑动平均值
        # 然后计算相应的向前传播结果
        layer1 = tf.nn.relu(tf.matmul(input_tensor,
                                      avg_class.average(weights1)) + avg_class.average(biases1))
        layer2 = tf.matmul(layer1, avg_class.average(weights2)) + avg_class.average(biases2)
        return layer2

# 训练模型
def train(mnist):
    x = tf.placeholder(tf.float32, [None, INPUT_NODE], name='x-input')
    y_ = tf.placeholder(tf.float32, [None, OUTPUT_NODE], name='y-input')

    # Hidden Layer
    weights1 = tf.Variable(tf.truncated_normal([INPUT_NODE, LAYER1_NODE], stddev=0.1))
    biases1 = tf.Variable(tf.constant(0.1, shape=[LAYER1_NODE]))

    # Output Layer
    weights2 = tf.Variable(tf.truncated_normal([LAYER1_NODE, OUTPUT_NODE], stddev=0.1))
    biases2 = tf.Variable(tf.constant(0.1, shape=[OUTPUT_NODE]))

    # 计算向前传播结果
    y = inference(x, None, weights1, biases1, weights2, biases2)

    # 定义循环次数变量, 并标记不参与训练
    global_step = tf.Variable(0, trainable=False)

    # 设置滑动平均衰减率
    variable_averages = tf.train.ExponentialMovingAverage(MOVING_AVERAGE_DECAY, global_step)

    # 所有神经网络上的变量使用滑动平均
    variable_avg_op = variable_averages.apply(tf.trainable_variables())

    # 计算使用滑动平均后向前传播的结果
    avg_y = inference(x, variable_averages, weights1, biases1, weights2, biases2)

    # 计算交叉熵
    cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=y,  labels=tf.argmax(y_, 1), name='loss1')
    # 计算交叉熵平均值
    cross_entropy_mean = tf.reduce_mean(cross_entropy)

    # 计算 L2 正则化损失函数
    regularizer = tf.contrib.layers.l2_regularizer(REGULARIZATION_RATE)
    # 计算模型正则化损失
    regularization = regularizer(weights1) + regularizer(weights2)
    # 总损失
    loss = cross_entropy_mean + regularization

    # 设置指数衰减学习率
    learning_rate = tf.train.exponential_decay(
        LEARNING_RATE_BASE,
        global_step,
        mnist.train.num_examples / BATCH_SIZE, # 需要迭代的次数
        LEARNING_RATE_DECAY)

    # 优化损失函数
    train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss, global_step=global_step)

    # 反向传播更新参数
    # tf.control_dependencies and tf.group 两种机制, 效果等同
    # Method1
    train_op = tf.group(train_step, variable_avg_op)
    # Methos2
    # with tf.control_dependencies([train_step, variable_avg_op]):
    #     train_op = tf.no_op(name='train')

    # 检验滑动平均模型向前传播结果是否正确
    correct_prediction = tf.equal(tf.argmax(avg_y, 1), tf.argmax(y_, 1))
    # 一组数据上的正确率
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    # 初始化会话并开始训练
    with tf.Session() as sess:
        tf.global_variables_initializer().run()

        # 准备验证数据
        validate_feed = {x: mnist.validation.images,
                         y_: mnist.validation.labels}

        # 准备测试数据
        test_feed = {x: mnist.test.images,
                     y_: mnist.test.labels}

        # 迭代训练
        for i in range(TRAINING_STEPS):
            if i % 1000 == 0:
                validate_acc = sess.run(accuracy, feed_dict=validate_feed)
                print("After %d training steps, test accuracy using average model is %g" % (i, validate_acc))

            # 产生 batch size 训练数据
            xs, ys = mnist.train.next_batch(BATCH_SIZE)
            sess.run(train_op, feed_dict={x: xs, y_: ys})

        test_acc = sess.run(accuracy, feed_dict=test_feed)
        print("[Finish] After %d training steps, test accuracy using average model is %g" % (TRAINING_STEPS, test_acc))


if __name__ == '__main__':

    path = os.getcwd() + "/Resources/MINSTData"
    print("path = ", path)

    mnist = input_data.read_data_sets(path, one_hot=True)
    
    print("Training data size: ", mnist.train.num_examples)
    train(mnist)


"""
Result:
raining data size:  55000
2018-08-15 14:20:22.909926: I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
After 0 training steps, test accuracy using average model is 0.1186
After 1000 training steps, test accuracy using average model is 0.9762
After 2000 training steps, test accuracy using average model is 0.983
After 3000 training steps, test accuracy using average model is 0.9838
After 4000 training steps, test accuracy using average model is 0.9836
After 5000 training steps, test accuracy using average model is 0.985
After 6000 training steps, test accuracy using average model is 0.9846
After 7000 training steps, test accuracy using average model is 0.985
After 8000 training steps, test accuracy using average model is 0.9846
After 9000 training steps, test accuracy using average model is 0.9844
After 10000 training steps, test accuracy using average model is 0.9848
After 11000 training steps, test accuracy using average model is 0.9856
After 12000 training steps, test accuracy using average model is 0.9842
...
"""
```


### 使用验证数据集判断模型效果

经过实践来看, 在验证模型上的表现可以体现测试模型上的表现.

### 不同模型效果比较

激活函数、隐藏层可以给模型效果带来质的飞越

相比滑动平均模型和指数衰减学习率, 使用加入正则化的损失函数给模型效果带来的提升要相对显著.

对于`训练数据`:
只优化交叉熵的表现 > 优化总损失的表现.

对于`测试数据`:
优化总损失的表现 > 只优化交叉熵的表现.

其原因就是`过拟合`造成的.

可见损失函数很重要.

## 变量管理

在上面的实践中, 只有3层网络就有了, weights1, weights2, biases1, biases2...等参数, 随着模型的复杂, 就面临一个参数管理的问题.

`TensorFlow`提供 `tf.Variable` 函数来`创建`或`获取变量`.

```python
# 以下两方法等价
v = tf.get_variable("v", shape=[1], initializer=tf.constant_initializer(1.0))
v = tf.Variable(tf.constant(1.0, shape=[1]), name="v")
```

总的来说, 类似字典方法, 不同的多了几种初始化函数:

|初始化函数|功能|主要参数|
|:-:|:-:|:-:|
|tf.constant_initializer|将变量初始化为给定常量|常量的取值|
|tf.random_normal_initializer|将变量初始化为满足正态分布的随机值|正态分布的均值和标准差|
|tf.truncated_normal_initializer|同上,但随即出来的偏离平均值超过2个标准差,那么这个数将会被重新随机|同上|
|tf.random_uniform_initializer|初始化为满足平均分布的随机值|最大,最小值|
|tf.uniform_unit_scaling_initializer|初始化为满足平均分布,但不影响影响输出数量级的随机值|factor|
|tf.zeros_initializer|初始化为全0|变量维度|
|tf.ones_initializer|初始化为全1|变量维度|

以及为了防无意识重用参数, 在调用时,如果参数存在则返回错误.

需要在 `tf.variable_scrop`函数中指定 `reuse=True` 才能重用

`resue=True` 时, 若变量不存在, 不会自动创建, 返回错误.

`tf.variable_scrop` 可以嵌套使用.

可以通过`tf.get_variable_scope().reuse` 获取当前上下文中 reuse 的值.

`变量名称` = `命名空间名/变量名:索引`, 可见变量名跟命名空间是关联的, 于是有, 定义一个名字为空的命名空间, 然后变量名为 `scopeA/v` , 这个变量等同于命名空间` scopeA`中的变量`v`.


以下是使用命名空间修改过后的代码:

```python
from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf
import os


# MNIST 数据集相关的常数
INPUT_NODE = 784            # 图片的像素
OUTPUT_NODE = 10            # 识别10个数字

# 配置神经网络的参数
LAYER1_NODE = 500
BATCH_SIZE = 100

LEARNING_RATE_BASE = 0.8
LEARNING_RATE_DECAY = 0.99  # 指数衰减法

REGULARIZATION_RATE = 0.0001        # 正则化项的系数
TRAINING_STEPS = 4000               # 实际发现训练5000次的时候准确率已经稳定
MOVING_AVERAGE_DECAY = 0.99         # 滑动平均衰减率


# 辅助函数, 计算向前传播的结果
def inference(input_tensor, avg_class, reuse=False):
    # 没有滑动平均类 直接使用参数当前的取值
    if avg_class == None:
        with tf.variable_scope('layer1', reuse=reuse):
            weights = tf.get_variable('weights',
                                      [INPUT_NODE, LAYER1_NODE],
                                      initializer=tf.truncated_normal_initializer(stddev=0.1))
            biases = tf.get_variable('biases',
                                     [LAYER1_NODE],
                                     initializer=tf.constant_initializer(0.0))
            # 计算向前传播的结果, 使用 ReLU 激活函数 + 去线性化
            layer1 = tf.nn.relu(tf.matmul(input_tensor, weights) + biases)

        with tf.variable_scope('layer2', reuse=reuse):
            weights = tf.get_variable('weights', [LAYER1_NODE, OUTPUT_NODE],
                                      initializer=tf.truncated_normal_initializer(stddev=0.1))
            biases = tf.get_variable('biases', [OUTPUT_NODE], initializer=tf.constant_initializer(0.0))

            layer2 = tf.matmul(layer1, weights) + biases
        return layer2
    else:
        with tf.variable_scope('layer1', reuse=reuse):
            weights = tf.get_variable('weights',
                                      [INPUT_NODE, LAYER1_NODE],
                                      initializer=tf.truncated_normal_initializer(stddev=0.1))
            biases = tf.get_variable('biases',
                                     [LAYER1_NODE],
                                     initializer=tf.constant_initializer(0.0))
            # 使用 avg_class.average 函数来计算滑动平均值
            # 然后计算相应的向前传播结果
            layer1 = tf.nn.relu(tf.matmul(input_tensor,
                                          avg_class.average(weights)) + avg_class.average(biases))

        with tf.variable_scope('layer2', reuse=reuse):
            weights = tf.get_variable('weights', [LAYER1_NODE, OUTPUT_NODE],
                                      initializer=tf.truncated_normal_initializer(stddev=0.1))
            biases = tf.get_variable('biases', [OUTPUT_NODE], initializer=tf.constant_initializer(0.0))

            layer2 = tf.matmul(layer1, avg_class.average(weights)) + avg_class.average(biases)
        return layer2

# 训练模型
def train(mnist):
    x = tf.placeholder(tf.float32, [None, INPUT_NODE], name='x-input')
    y_ = tf.placeholder(tf.float32, [None, OUTPUT_NODE], name='y-input')

    # # Hidden Layer
    # weights1 = tf.Variable(tf.truncated_normal([INPUT_NODE, LAYER1_NODE], stddev=0.1))
    # biases1 = tf.Variable(tf.constant(0.1, shape=[LAYER1_NODE]))
    #
    # # Output Layer
    # weights2 = tf.Variable(tf.truncated_normal([LAYER1_NODE, OUTPUT_NODE], stddev=0.1))
    # biases2 = tf.Variable(tf.constant(0.1, shape=[OUTPUT_NODE]))

    # 计算向前传播结果
    y = inference(x, None, reuse=False)

    # 定义循环次数变量, 并标记不参与训练
    global_step = tf.Variable(0, trainable=False)

    # 设置滑动平均衰减率
    variable_averages = tf.train.ExponentialMovingAverage(MOVING_AVERAGE_DECAY, global_step)

    # 所有神经网络上的变量使用滑动平均
    variable_avg_op = variable_averages.apply(tf.trainable_variables())

    # 计算使用滑动平均后向前传播的结果
    avg_y = inference(x, variable_averages, reuse=True)

    # 计算交叉熵
    cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=y,  labels=tf.argmax(y_, 1), name='loss1')
    # 计算交叉熵平均值
    cross_entropy_mean = tf.reduce_mean(cross_entropy)

    # 计算 L2 正则化损失函数
    regularizer = tf.contrib.layers.l2_regularizer(REGULARIZATION_RATE)
    # 计算模型正则化损失
    with tf.variable_scope('layer1', reuse=True):
        weights1 = tf.get_variable('weights')
    with tf.variable_scope('layer2', reuse=True):
        weights2 = tf.get_variable('weights')

    regularization = regularizer(weights1) + regularizer(weights2)
    # 总损失
    loss = cross_entropy_mean + regularization

    # 设置指数衰减学习率
    learning_rate = tf.train.exponential_decay(
        LEARNING_RATE_BASE,
        global_step,
        mnist.train.num_examples / BATCH_SIZE, # 需要迭代的次数
        LEARNING_RATE_DECAY)

    # 优化损失函数
    train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss, global_step=global_step)

    # 反向传播更新参数
    # tf.control_dependencies and tf.group 两种机制, 效果等同
    # Method1
    train_op = tf.group(train_step, variable_avg_op)
    # Methos2
    # with tf.control_dependencies([train_step, variable_avg_op]):
    #     train_op = tf.no_op(name='train')

    # 检验滑动平均模型向前传播结果是否正确
    correct_prediction = tf.equal(tf.argmax(avg_y, 1), tf.argmax(y_, 1))
    # 一组数据上的正确率
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    # 初始化会话并开始训练
    with tf.Session() as sess:
        tf.global_variables_initializer().run()

        # 准备验证数据
        validate_feed = {x: mnist.validation.images,
                         y_: mnist.validation.labels}

        # 准备测试数据
        test_feed = {x: mnist.test.images,
                     y_: mnist.test.labels}

        # 迭代训练
        for i in range(TRAINING_STEPS):
            if i % 1000 == 0:
                validate_acc = sess.run(accuracy, feed_dict=validate_feed)
                test_acc = sess.run(accuracy, feed_dict=test_feed)
                print("After %d training steps\n" % (i),
                      "test accuracy using average model is %g" % (test_acc),
                      "validation accuracy using average model is %g" % (validate_acc))

            # 产生 batch size 训练数据
            xs, ys = mnist.train.next_batch(BATCH_SIZE)
            sess.run(train_op, feed_dict={x: xs, y_: ys})


        test_acc = sess.run(accuracy, feed_dict=test_feed)
        print("[Finish] After %d training steps, test accuracy using average model is %g" % (TRAINING_STEPS, test_acc))



def onTrain():
    path = os.getcwd() + "/Resources/MINSTData"
    print("path = ", path)

    mnist = input_data.read_data_sets(path, one_hot=True)

    print("Training data size: ", mnist.train.num_examples)
    train(mnist)


if __name__ == '__main__':
    onTrain()
    
"""
Training data size:  55000
2018-08-15 17:36:39.368090: I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
After 0 training steps
 test accuracy using average model is 0.047 validation accuracy using average model is 0.0518
After 1000 training steps
 test accuracy using average model is 0.9764 validation accuracy using average model is 0.9772
After 2000 training steps
 test accuracy using average model is 0.9813 validation accuracy using average model is 0.982
After 3000 training steps
 test accuracy using average model is 0.9829 validation accuracy using average model is 0.9828
[Finish] After 4000 training steps, test accuracy using average model is 0.9831
"""
```

