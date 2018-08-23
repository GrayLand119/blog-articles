---

title: TensorFlow学习笔记(8) - 迁移学习
subtitle: tfln8
date: 2018-08-23 18:12:00
tags: TensorFlow
mathjax: true

---

<!--# TensorFlow学习笔记(8) - 迁移学习-->

所谓迁移学习, 就是将一个问题上训练好的模型通过简单的调整使其适用于一个新的问题.

为什么需要迁移学习?

随着模型复杂度的增加可以提高识别的准确率, 但是同时需要大量的标记数据和时间来进行训练, 在真实应用中很难收集到如此多的标记数据. 即便可以收集到也会消耗大量的人力物力, 即便收集到了, 还需要大量时间训练. 迁移学习可以很好解决这些问题.

这里有个新名词叫做`瓶颈层( bottleneck)`, 即最后一层全连接层之前的网络称之为`瓶颈层`.

迁移学习, 就是保留模型中的参数, 只替换最后一层全连接层.

可以认为瓶颈层输出节点向量表示的是对图像的特征提取的抽象表达, 于是, 在新的数据集上, 可以直接利用这个训练好的神经网络对图像进行特征提取, 再通过一个新的单层全连接, 处理新的分类问题.

一般来说, 在数据量足够的情况下, 迁移学习的效果不如完全重新训练. 但是迁移学习需要的时间和样本数远远小于训练完整的模型.

## TensorFlow 实现迁移学习

下载数据集:

```
# 图片资源 没有翻墙工具的, 使用迅雷下载有惊喜
https://download.tensorflow.org/example_images/flower_photos.tgz
# 训练好的模型 需要翻墙
https://storage.googleapis.com/download.tensorflow.org/models/inception_dec_2015.zip
```

以下是训练代码:

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


