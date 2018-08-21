---

title: TensorFlow学习笔记(6) - CNN
subtitle: tfln6
date: 2018-08-21 18:07:33
tags: iOS
mathjax: true

---

<!--# TensorFlow学习笔记(6) - CNN-->

CNN(Convolutional Neural Network) 即卷积神经网络的简称.

CNN 的应用非常广泛, 在自然语言处理/医药发现/灾难气候发现/围棋人工智能等领域都有应用.

本次学习主要针对图像识别领域上的应用.

ImageNet 是一个基于 WordNet 的大型图像数据库, ImageNet 中的图片都是从互联网上爬取下来的, 并且通过亚马逊人工标注服务奖图片分类到WordNet 的同义词集上.

ImageNet 每年都举办图像识别相关的竞赛(ImageNet Large Scale Visual Recognition Challenge, ILSVRC). 本次学习主要使用 ILSVRC2012 的图像分类数据集.

ILSVRC2012 图像分类数据集中包含了来自1000个类别的120万张图片, 其中每张图片只属于一个类别.

[历届 ILSVRC 竞赛题目和数据集](http://www.image-net.org/challenges/LSVRC)

## CNN 简介

之前学习的神经网络两层之间每个节点都是相连的, 称为`全连接层网络结构`. 为了与` CNN`和`循环神经网络`区分开来, 在这将其称之为`全连接神经网络`.

CNN 与全连接神经网络结构类似, 但 CNN相连两层之间只有部分节点相连.

CNN 的输入输出以及训练流程与全连接神经网络也基本一致.

一个 CNN 主要由以下5种结构组成:

1. 输入层.在处理图像问题中, 输入层一般为一张图片的像素矩阵.
2. 卷积层.卷积层中每个节点的输入是上一层的一小块,而不是全部.这个小块常用的大小有`3X3`,`5X5`.卷积层试图将神经网络中的一小块进行更加深入地分析,从而得到抽象度更高的特征.一般来说, 通过卷积层处理的节点矩阵的深度会增加.
3. 池化层(Pooling).池化层不会改变参数矩阵的深度,但改变大小.可以认为是把一张高分辨率的图片转化成低分辨率的过程.通过池化层可以减少节点的个数,从而减少神经网络中的参数.
4. 全连接层.在经过多轮卷积和池化之后, 在 CNN 中一般是使用1~2个全连接层来进行分类. 可认为卷积和池化是抽象提取更高特征的过程.分类任务还是靠全连接层.
5. Softmax 层. 结果转概率分布.

## 卷积层

卷积层中主要部分称之为`过滤器 filter` 或`内核 kernel`, TensorFlow 中称之为`过滤器`.

过滤器可以将上一层的一个子`节点矩阵`转化成下一层的`单位节点矩阵`.`单位节点矩阵`就是长和宽都为1,但深度不限的节点矩阵.

在卷积层中`节点矩阵`的大小一般由人工指定, 一般为 3X3, 5X5. 这个尺寸也称为过滤器尺寸.另一个需要人工指定的是过滤器的深度.

向前传播过程和全连接的类似, 假设入参为 2x2x3 的一个矩阵, 经过 2x2x5 的过滤器后, 得到一个 1x1x5 的单位节点矩阵. 总共需要 2x2x3x5+5=65 个参数. 其中 +5 是5个偏置项参数.

向前传播过程和全连接类似, 假设 $w_{x,y,z}^i$表示输出单位矩阵中的第 i 个节点, $a_{x,y,z}$为过滤器节点`(x,y,z)`的取值, `f` 为激活函数, $b^i$表示第 i 个输出节点对应的偏置项参数. 那么第 i 个节点 g(i) 的取值:

$$g(i)=f(\sum\limits_{x=1}^{2} \sum\limits_{y=1}^{2} \sum\limits_{z=1}^{3} a_{x,y,z} \times w_{x,y,z}^{i} + b^{i})$$

卷积过程参考: [技术向：一文读懂卷积神经网络CNN | 数盟](http://dataunion.org/11692.html)

这个过程就是: 卷积核矩阵在输入矩阵上, 依次从左到右,从上到下按指定步长移动然后相乘的得到的结果输入激活函数, 得到的输出结果就是输出矩阵上对应位置的取值.

当过滤器(卷积核)大小不为1x1时, 向前传播的矩阵要小于当前矩阵.

为了避免传播结果的尺寸变化, 可以对当前矩阵的边界加入全0填充(zero-padding),或调整合适的步长.

另外, CNN 还有一个重要的性质, 就是 `每个卷积层使用的过滤器参数都是一样的`. 直观上理解就是, 共享过滤器参数可以使得图像上的内容不受位置的影响, 例如手写识别1, 1出现在图像中的任意地方都是一个效果. 共享参数还能巨幅减少神经网络上的参数.

## 池化层

池化层可以有效缩小矩阵的尺寸,从而减少全连接层中的参数,起到加速和防止过拟合的作用.

池化过程和卷积过程类似,故参数也和卷积层一样,包含尺寸/步长/填充方式等,但使用的不是加权和, 而是其他操作. 一般使用取最大值或平均值.分别称为最大池化层和平均池化层.

以下代码为向前传播(卷积->池化)的过程:

```python
import tensorflow as tf


if __name__ == '__main__':
    # shape 的第1,2参数是过滤器尺寸, 3为当前层深度, 4位过滤器深度
    filter_weight = tf.get_variable('weights', [5, 5, 3, 16], initializer=tf.truncated_normal_initializer(stddev=0.1))

    # 偏置项
    biases = tf.get_variable('biases', [16], initializer=tf.constant_initializer(0.1))

    # 随机产生一个输入数据
    input_data = tf.get_variable('inputdata', [1, 32, 32, 3], initializer=tf.truncated_normal_initializer(stddev=5))

    # tf 提供的的向前传播方法 tf.nn.conv2d padding="SAME"表示用0填充, "VALID"表示不填充, strides表示不同维度上的步长
    """
    1. Flattens the filter to a 2-D matrix with shape
     `[filter_height * filter_width * in_channels, output_channels]`.
    2. Extracts image patches from the input tensor to form a *virtual*
    tensor of shape `[batch, out_height, out_width,
    filter_height * filter_width * in_channels]`.
    3. For each patch, right-multiplies the filter matrix and the image patch
    vector.
     """
    conv = tf.nn.conv2d(input_data, filter_weight, strides=[1, 1, 1, 1], padding='SAME')

    # tf.nn.bias_add 提供一个方便函数给每个节点添加偏置项.
    conv_biased = tf.nn.bias_add(conv, biases)

    conv_actived = tf.nn.relu(conv_biased)
    # NHWC - [输入样例个数, 高, 宽, 深度/Channel]
    # ksize 第一和最后一个参数始终为1, 意味着着池化层不能改变输入样例个数和深度的
    # strides 同理.
    conv_pool = tf.nn.max_pool(conv_actived, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1], padding="SAME")

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        print(sess.run(conv_pool))

```

