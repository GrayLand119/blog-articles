
---

title: TensorFlow 学习笔记(1)
subtitle: tfln1
date: 2018-08-14 16:07:22
tags: TensorFlow

---

<!--# TensorFlow 学习笔记(1)-->

## 张量 - Tensor

0阶张量 - Scalar(标量) - 一个数字
1阶 - 向量 - 一维数组 
N阶 - N维

张量的实现不是直接采用数组的形式.
它只是对 TensorFlow 中运算结果的引用.

张量主要属性: 
* name(名字)
* shape(维度)
* type(类型)

张量和计算图上的阶段是对应的.

名字不仅是唯一标识符,也给出该张量是如何计算出来的.
命名:"node: src_output"
e.g.: "add: 0" -> result = a + b
Mean: 计算节点 'add'输出的第一个结果.



## 会话 - Session

TensorFlow中使用会话( session)来执行定义好的运算.
会话拥有并管理 TensorFlow 程序运行时的所有资源.
使用完成后需要手动释放.
流程: 
* sess = tf.Session()
* sess.run(...), e.g.: sess.run(result)
* sess.close

上面的方法, 崩溃不释放.

使用 `Python 上下文管理机制` 解决崩溃释放.

```python
with tf.Session() as sess:
  sess.run(...)
```

与图不同的是系统不会默认指定, 需要手动指定:
```python
sess = tf.Session()
with sess.as_default():# 手动指定
  print(result.eval())
  
# 一下代码效果等同
print(sess.run(result))
print(sessresult.eval(session=sess))
```

`InteractiveSession()`函数:
直接构建默认会话.省去设为默认的过程.

`ConfigProto`配置会话:
ConfigProto 可以配置线程数, GPU 分配策略, 运算超时时间等参数.
```python
config = tf.ConfigProto(allow_soft_placement=True, 
                        log_device_placement=True)
sess1 = tf.InteractiveSession(config=config)
sess2 = tf.Session(config=config)
```

`allow_soft_placement`:
默认为 False, =True时, 满足以下任一条件, GPU 运算可以放到 CPU 上运行:
* 运算无法在 GPU 上运行
* 没有 GPU资源
* 运算输入包含 CPU 计算结果的引用

`log_device_placement`:
=True时, 日志会记录每个节点被安排在哪个设备上, 以方便调试.
生产环境= False, 减少日志量.

`feature vector`:
描述实体的特征数字组合, 称为`特征向量`

## TensorFlow Playground

playground.TensorFlow.org

## 向前传播算法

参数=权重=W, W1,W2,.. 表示第1层参数, 第2层参数...
优化过程=调参
`全连接神经网络`:
相邻两层之间,任意节点都有连接.

向前传播算法可以表示为矩阵乘法.
矩阵表示 = rows x cols
cols - 参数个数
rows - 某参数对应不同输入所取的不同值

`tf.matmul` 实现矩阵乘法:
a = tf.matmul(x, w1)

`神经网络参数与 TensorFlow 变量`:
一般使用随机数给 TensorFlow 中的变量初始化:
```python
# 声明 2 x 3 矩阵 ,均值=0,标准差=2
# mean 参数设置平均数. default = 0
weights = tf.Variable(tf.random_normal([2,3], stddev=2))
```

### 随机数生成器

`tf.<function>`
* `random_normal`, 正态分布
* `truncated_normal`, 正态分布,随机出来的值偏离平均值超过2个标准差, 那么这个数会被重新随机
* `random_uniform`, 平均分布
* `random_gamma`, Gamma 分布

常数生成函数:
`tf.<function>`:
* `zeros`, all 0
* `ones`, all 1
* `fill`, 全部指定数, tf.fill([2,3], 9) - > [[9,9,9],[9,9,9]]
* `constant`, tf.constan([1,2,3]) -> [1,2,3]

`biases`偏置项通常使用常数来设置初始值.

### 初始化变量

```python
biases = tf.Variable(tf.zeros([3]))
weights = tf.Variable(tf.random_normal([2, 3], stddev=2))
w2 = tf.Variable(weights.initialized_value())
w3 = tf.Variable(weights.initialized_value() * 2.0)
```

每个参数设置后并不能马上使用, 需要先进行初始化操作.
> sess.run(w1.initializer)
> 

参数多的时候,为了方便初始化,使用:
`tf.initialize_all_veriables()`:
自动处理变量之间的依赖关系.

```python
init_op = tf.initialize_all_variables()
sess.run(init_op)
```

### Collection - 集合

所有的变量会被自动的加入 GraphKeys.VARIABLES 这个集合.
通过 `tf.all_variables`函数可以拿到当前计算图上所有变量, 有助于持久化整个计算图的运行状态.

`trainable`参数, 声明/区分 需要优化的参数.
trainable=True, 则变量自动加入 GraphKeys.TRAINABLE_VARIABLES 集合.
tf.trainable_variables 函数得到所有需要优化的参数.

`validate_shape`, =False 则 shape 能被改变. 实践中比较少见.

## 训练神经网络模型

1. 通过` placeholder` 实现向前传播算法.
2. 执行`sess.run()`得到向前传播结果.
3. 定义损失函数来刻画预测值与真实值的差距. `cross_entropy`
4. 定义学习率 `learning_rate`
5. 定义反向传播算法来优化神经网络中的参数.

`placeholder` 定存放输入数据的维度.(维度不一定要定义, 但如果确定, 定义后降低出错概率)
`feed_dict`, sess.run()中的参数, 定义向前传播中1个 batch的数据. 输入数据 x
`优化算法`, TensorFlow 支持7种不同的优化器.常用的有3种:

* tf.train.GradientDescentOptimizer
* tf.train.AdamOptimizer
* tf.train.MomentumOptimizer

# 深层神经网络
## 线性模型的局限性

假设一个模型的输出 y 和输入 x,满足以下关系, 那么这个模型就是一个线性模型:
$$y = \sum\limits_{i} w_ix_i + b$$

线性模型叠加后还是线性的.

常见激活函数有:

* ReLU->tf.nn.relu()->$\displaystyle f(x)=max(x,0)$
* sigmoid->tf.sigmoid()->$\displaystyle f(x)=\frac {1}{1+e^{-x}}$
* tanh->tf.tanh->$\displaystyle f(x)=\frac {1-e^{-2x}}{1+e^{-2x}}$

## 多层网络解决异或运算

感知机不能处理异或问题.
深层神经网络实际上有`组合特征提取`的功能.

## 损失函数定义
### 经典损失函数

分类和回归问题是监督学习的两大种类.

#### 分类问题

分类问题希望解决的是,将不同样本分到事先定义好的类别中.

##### 交叉熵(Cross-Entropy)

交叉熵刻画两个概率分布之间的距离. 是分类问题中使用得比较广的函数.

交叉熵原本是信息论中的一个概念, 用来估算平均编码长度的.

给定两个概率分布p 和 q, 通过 q 来表示 p 的交叉熵为:
$$ H(p,q) = - \sum\limits_x p(x)log^{q(x)}$$

如何将神经网络向前传播得到的结果也满足概率分布?
Softmax 回归就是一个非常常用的方法.

Softmax 回归本身可以作为一个学习算法来优化分类结果, 但在 TensorFlow 中, Softmax 回归的参数被去掉了, 它只是一层额外的处理层, 将神经网络输出变成一个概率分布.

假设神经网络的输出为 $y_1,y_2,y_n...$

$$softmax(y)_i = y_i^, = \frac {e^{yi}}{\sum_{j=1}^{n} e^{yj}}$$

从交叉熵的公式中可以看出, 交叉熵函数不是对称的
$\displaystyle  H(p,q) \neq  H(q,p)$

它刻画的是通过概率分布 p 来表达概率分布 q 的困难程度.

当交叉熵作为神经网络的损失函数时, p 带表正确答案, q 带表预测值.

交叉熵越小, 两个概率分布越接近.

例如一个三分类问题:
某个正确答案是(1,0,0)
某模型经过 Softmax 回归后的预测答案A为(0.5,0.4,0.1), B为(0.8,0.1,0.1)

则:

$H(A)=H((1,0,0),(0.5,0.4,0.1))=-(1*log(0.5) + 0*log(0.4) + 0*log(0.1)) \approx 0.3$

$H(B)=H((1,0,0),(0.8,0.1,0.1))=-(1*log(0.8) + 0*log(0.1) + 0*log(0.1)) \approx 0.1$

可以看出 B是优于 A的.

Python实现:
```python
cross_entropy = -tf.reduce.mean(y_ * tf.log(tf.clip_by_value(y, 1e-10, 1.0)))
```
`clip_by_value` 将张量中的数值限制在一个范围内, 以避免一些运算错误(log(0)是无效的), 其实就是取上下限.

因为交叉熵一般会与 Softmax 回归一起使用, TensorFlow 对两个功能进行了统一封装:

```python
cross_entropy = tf.nn.softmax_cross_entropy_with_logits(y, y_)
```

在只有一个正确答案的分类问题中, 使用`softmax_cross_entropy_with_logits`函数来加速计算过程.

#### 回归问题

回归问题解决的是对具体数值的预测.

##### 均方误差(MSE, mean squared error)

$$MSE(y, y^,) = \frac {\sum _{i=1}^{n} (y_i - y_i^,)^2}{n}$$

其中 $y_i$为一个 batch中,第 i 个数据的正确答案
$y_i^,$为预测值.

```python
mse = tf.reduce_mean(tf.square(y_ - y))
```

#### 自定义损失函数

当实际问题预测多和预测少造成的结果或影响不同时, MSE不能得到贴近实际的预估效果, 就需要用到自定义损失函数.

其实就是对不同区间进行不同的加权操作.

## 神经网络优化算法

神经网络模型中的参数优化过程直接决定了模型的质量, 是使用神经网络时非常重要的一步.

梯度下降法是最常用的神经网络优化方法.

`梯度下降法`不断沿着梯度的反方向让参数朝着总损失更小的方向更新.(因此学习率设置过大,会造成结果不断的跳跃)

> 梯度 = 求偏导方式计算
> 参数更新 = 上次参数 - 梯度 x 学习率
> 

梯度下降法不能保证被优化的函数达到全局最优解.
只有当损失函数为凸函数时才能保证达到全局最优解.

由于梯度下降法每一轮迭代中, 如果选取的是全部训练数据, 计算量将会非常的大, 通过概率学的一些原理可以知道, 采用随机的方式选取局部的样本也能得到近似解.
所以, 为了加速训练过程, 可以选择随机梯度下降法结合小部分 batch 的数据进行每次的迭代.

## 神经网络进一步优化
### 学习率的设置

通过之前的学习自导, 学习率不能过大,也不能过小, 且学习率对训练速度的影响很大, 为了解决学习率的问题 TensorFlow 提供了一种更加灵活的学习率设置方法--`指数衰减法`

`指数衰减法`: `tf.train.exponential_decay`实现了指数衰减学习率. 具体就是,先使用比较大的学习率来快速得到比较优的解, 然后随着迭代继续逐步减小学习率.

衰减公式:

> decayed_learning_rate = 
> learning_rate * decay_rate ^ (global_step / decay_steps)

参数 `staircase` , = True 时, `global_step / decay_steps`取整.

### 过拟合问题

简单理解, 过拟合就是训练过度, 训练过程中过度关注噪声, 把噪声都刻画到训练模型中去了.

为了避免过拟合, 常用方法是正则化( regularization)

基本思想是`通过限制权重大小, 使得模型不能任意拟合训练数据中的随机噪音`

假设用于刻画模型在训练数据上表现的损失函数为 J(θ) , 那么在优化时不直接优化 J(θ), 而是优化 `J(θ) + λR(w)`
R(w)刻画的是模型复杂程度.
λ 表示模型复杂损失在总损失中的比例

#### L1 正则化

L1 正则化会让更多的参数变为0, 这样可以达到类似特征选取的功能.

$$ L_1  = R(w) = \sum\limits_i \Big|w_i\Big| $$

> tf.contrib.layers.l1_regularizer(lambda)(w)
> lambda -> λ
> 

L1 不可导.

#### L2 正则化

$$ L_2  = R(w) = \sum\limits_i \Big|w_i^2\Big| $$

L2 可导.

实践中, L1,L2可以同时使用

实践:
```python
weights = tf.constant([[1.0, -2.0], [-3.0, 4.0]])
    with tf.Session() as sess:
        print("L1 = ", sess.run(tf.contrib.layers.l1_regularizer(.5)(weights)))
        print("L2 = ", sess.run(tf.contrib.layers.l2_regularizer(.5)(weights)))
"""
L1 =  5.0
L2 =  7.5
"""
```

当参数增多之后, 这样的方式会使得损失函数 loss 定义很长, 可读性差且易错.

这个时候可以使用之前的 `Collection` 和 `tf.Graph` 相关知识.

## 滑动平均模型

在采用随机梯度下降算法训练神经网络时, 使用滑动平均模型在很多应用中都可以在一定程度提高最终模型在测试数据上的表现.

> tf.train.ExponentialMovingAverage 来实现
> 参数- decay 衰减率, 一般设为接近1的数 (0.9999)
> 参数- num_updates, $decay=min(decay, \frac {1+num_updates}{10 + num_updates})$
> shadow_variable 影子变量
> variable 待更新变量
> shadow_variable 初始值是相应变量的初始值


$$shadow\_variable=decay * shadow\_variable + (1-decay) * variable$$

