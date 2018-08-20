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

