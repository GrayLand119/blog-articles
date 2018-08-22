---

title: TensorFlow学习笔记(7) - 经典CNN模型
subtitle: tfln7
date: 2018-08-22 16:30:07
tags: TensorFlow
mathjax: true

---

<!--# TensorFlow学习笔记(7) - 经典CNN模型-->

上一节学习了 CNN 的结构 - 卷积层和池化层. 然而通过这些网络结构任意组合得到的神经网络有无限多种, 那么怎样的神经网络更能解决图像问题呢. 大神们已经总结出了几种经典的模型, 通过学习这些模型可以总结出一些 CNN 结构设计的一些模式.

## LeNet-5 模型

LeNet-5 模型时 Yann LeCun 教授于1998年在论文 Gradient-based learning applied to document recognition 中提出的. 它是第一个成功应用于数字识问题的 CNN. 在 MNIST 数据集上, LeNet-5 模型可以达到99.2%的正确率.

LeNet-5模型总共有7层:

##### 1.卷积层

* 输入层大小 32X32X1.
* 过滤器尺寸为 5X5, 深度为 6.
* 不使用全0填充
* 步长为1.

由上面数据可以看出, 输出层=32-5+1=28, 深度=6.参数数量=5X5X1X6+6=156.
输出的节点=28X28X6=4704, 与5X5=25个过滤器(卷积核)上的点连接, 连接数=4704*(25+1)=122304个连接.1是偏置项.

##### 2.池化层

* 输入 28X28X6.
* 过滤器尺寸=2X2, 步长=2

输出矩阵大小=14X14X6.

##### 3.卷积层

* 输入 14X14X6.
* 过滤器大小 5X5, 深度 16.
* 不使用全0填充
* 步长为1.

输出矩阵大小=10X10X16, 参数数量=5X5X6X16+16=2416, 连接数=10X10X16X(5X5+1)=41600个连接

##### 4. 池化层

* 输入 10X10X16
* 过滤器大小 2X2
* 步长 2

输出 5X5X16.

##### 5.全连接层/池化层

原论文中是5X5的池化层, 等同于全连接.

* 输入&输出 5X5X16
* 输出节点 120

参数数量=5X5X16X120+120=48120

##### 6.全连接层

* 输入节点 120
* 输出节点 84

参数数量=120X84+84=10164

##### 7.全连接层

* 输入84
* 输出 10

参数数量=84X10+10=850

到这里实际编码的时候发现对 Padding 的方式有疑惑, 后来又回去看了下总结出padding的公式:

* 输入尺寸 W, 输出尺寸 NW, 过滤器尺寸 F, 步长 S
* 如果不填充, NW = (W - F + 1) / S , 向上取整
* 如果全0填充, NW = W / S, 向上取整
* 需要 Padding 的尺寸PW = (NW - 1) X S + F - W

简单说就是如果移动步长后, 在卷积的时候如果剩下的输入数据不够过滤器的Size, 则差多少Size就填充多少.

除了 LeNet-5模型, 2012年的 ImageNet ILSVRC 图像分类大赛第一名 AlexNet 模型, 2013年 第一名 ZF Net 模型, 2014年第二名 VGGNet 模型都满足上面7层结构.

从这些模型中看出, 过滤器尺寸通常在2~3,一般不超过5,少有的一些会使用到7甚至11.
深度上, 大多都采用逐层递增或乘以2.
卷积层步长一般为1, 有的为2~3.
池化层尺寸和步长一般都为2~3.

TensorFlow 编码时, 卷积层和池化层实现和上一节学习的一样的, 需要注意的是在第二个池化结束后, 输出的是一个 `Height x Width x Deep` 的矩阵, 第一个全连接层输入需要的是一个向量, 所以这里需要将矩阵拉直成一个向量.

* `pool2.get_shape` 可以得到矩阵的维度.
* 每层输入输出都为1个 batch 的矩阵, 故获得的维度也包含了1个 batch 中数据的个数.
* `tf.reshape` 可以将输出编程一个 batch 的向量.

```python
# ... 略
pool2 = 第二个池化层输出
# 得到维度信息 如 Batch x Heiht x Width x Deep/Channel
# as_list() 转 list
pool_shape = pool2.get_shape().as_list()
nodes = pool_shape[1] * pool_shape[2] * pool_shape[3]
# 将四维的输出编程一维向量
reshaped = tf.reshape(pool2, [pool_shape[0], nodes])
# 之后就是全连接一样的传播方法
# ... 略
```

## Inception-v3模型

Inception 结构和 LeNet-5结构完成不同.
在 LeNet-5 中, 不同卷积层通过串联连接在一起, 而 Inception-v3模型中的 Inception 结构是并联的方式结合在一起.

简单说就是 输入矩阵->多个尺寸的过滤器->输出的结果组合成一个更深的矩阵.多个过滤器使用1步长和0填充,就保证了输出的矩阵大小不变.

合并使用函数`tf.concat`.

Inception-v3 模型总共46层, 由11个 Inception 模块组成, Inception-v3一共有96个卷积层. 如果按照之前卷积层的实现代码, 一个 Inception 结构就需要至少5行代码. 总共需要480行代码实现.

为了简化代码, TensorFlow 提供了` TensorF-Slim` 工具来更加简洁的实现一个卷积层.

以下为普通实现和 Slim 实现一个卷积层的代码:

```python
# Normal
with tf.variable_scopr(SCOPE_NAME):
  weight =  tf.get_variable(...)
  biases = tf.get_variable(...)
  conv = tf.nn.conv2d(...)
relu = tf.nn.relu(tf.nn.bias_add(conv, biases))

# Slim
# param1 数据节点矩阵, param2 深度, param3 过滤器尺寸
# 其他可选字段 步长/填充/命名空间/激活函数选择
net = slim.conv2d(input, 32, [3, 3])
```

Slim 还提供 `slim.arg_scope`方法 设置指定默认参数, 如步长和填充, 使用此方法, 在其上下文环境中的 `conv2d` 参数默认值会与之相同, 进一步简化代码.

```python
with slim.arg_scope([slim.conv2d, slim.max_pool2d, slim.avg_pool2d], stride=1, padding='SAME'):
  #...
  net = 上层输出
  # Inception 结构
  with ...scope...:
    # 路径1
    with ...branch_0...:
      branch_0 = slim.conv2d(net, 320, [1, 1], scope='Conv2d_0a_1x1')
    # 路径2
    with ...branch_1...:
      branch_1 = slim.conv2d(net, 384, [1, 1], scope='Conv2d_0a_1x1')
      # Inception 结构
      branch_1_1 = slim.conv2d(branch_1, 384, [1, 3], scope='Conv2d_0ba_1x3')
      branch_1_2 = slim.conv2d(branch_2, 384, [3, 1], scope='Conv2d_0bb_3x1')
      branch_1 = tf.concat(3, [branch_1_1, branch_1_2])
    # 路径3 路径4
    # ...
    # 当前 Inception 最后输出
    net = tf.concat(3, [branch_0, branch_1, branch_2, branch_3])
```





