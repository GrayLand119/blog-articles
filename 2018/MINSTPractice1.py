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


