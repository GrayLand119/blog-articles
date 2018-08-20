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
