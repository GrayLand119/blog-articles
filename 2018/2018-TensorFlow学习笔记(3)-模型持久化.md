---

title: TensorFlow学习笔记(3) - 模型持久化
subtitle: tfln3
date: 2018-08-17 17:59:04
tags: iOS
mathjax: true

---

<!-- # TensorFlow学习笔记(3) - 模型持久化 -->


## TensorFlow 模型持久化

[代码](./3-DataPersistence.py)

主要类 `tf.train.Saver`. 方法`<Saver>saver.save`.

保存后会生成3个文件.

* `ckpt.meta` , 保存计算图的结构
* `ckpt`, 保存每个变量的取值
* `checkpoint`, 保存一个目录下所有模型文件列表

保存图

### 保存计算图

```python
v1 = tf.Variable(tf.constant(1.0, shape=[1]), name='v1')
v2 = tf.Variable(tf.constant(2.0, shape=[1]), name='v2')
result = v1 + v2

init_op = tf.global_variables_initializer()

saver1 = tf.train.Saver()

with tf.Session() as sess:
    sess.run(init_op)
    print("All variables:", tf.global_variables())
    saver1.save(sess, "./SaveModels/model1.ckpt")
```

### 读取计算图中的变量

`<Saver>saver.restore` 函数

```python
v1 = tf.Variable(tf.constant(0.0, shape=[1]), name='v1')
v2 = tf.Variable(tf.constant(0.0, shape=[1]), name='v2')

result = v1 + v2

saver2 = tf.train.Saver()

with tf.Session() as sess:
    saver2.restore(sess, './SaveModels/model1.ckpt')
    print(sess.run(result))

pass

```

### 加载持久化的图(包含运算)

```python
# 直接加载图, 包含运算
saver = tf.train.import_meta_graph('./SaveModels/model1.ckpt.meta')

with tf.Session() as sess:
    saver.restore(sess, './SaveModels/model1.ckpt')
    print(sess.run(tf.get_default_graph().get_tensor_by_name("add:0")))
```

### 只加载部分指定变量

加载变量方法:

`tf.train.Saver(paramNeedLoad: list)`, paramNeedLoad 是要加载变量的 list.

同时也支持加载变量后重命名, 其目的之一是为了方便使用变量的滑动平均值. 因为, 滑动平均值是通过影子变量维护的, 如果加载模型时直接将影子变量映射到自身, 那么使用训练好的模型时, 就不需要再调用函数来获取变量的滑动平均值了.

```python
V1 = tf.Variable(tf.constant(0.0, shape=[1]), name='other-v1')
V2 = tf.Variable(tf.constant(0.0, shape=[1]), name='other-v2')
result = V1 + V2

saver = tf.train.Saver({"v1": V1, "v2": V2})

with tf.Session() as sess:
    saver.restore(sess, './SaveModels/model1.ckpt')
    print(V1)
    print(V2)
    print("Result=", sess.run(result))
    
"""
<tf.Variable 'other-v1:0' shape=(1,) dtype=float32_ref>
<tf.Variable 'other-v2:0' shape=(1,) dtype=float32_ref>
Result= [ 3.]
"""

```


存取滑动平均例子:

```python
# 存滑动平均
v1 = tf.Variable(0, dtype=tf.float32, name='v1')
v2 = tf.Variable(0, dtype=tf.float32, name='v2')
# 这时打印全部变量 只有 "v:0"
print("Before: ")
for tempV in tf.global_variables():
    print(tempV.name)

ema = tf.train.ExponentialMovingAverage(0.99)
maintain_avg_op = ema.apply(tf.global_variables())
# 这时打印
print("After: ")
for tempV in tf.global_variables():
    print(tempV.name)

saver = tf.train.Saver()

with tf.Session() as sess:
    init_op = tf.global_variables_initializer()
    sess.run(init_op)

    sess.run(tf.assign(v1, 10))
    sess.run(tf.assign(v2, 5))
    sess.run(maintain_avg_op)

    saver.save(sess, "./SaveModels/model1.ckpt")

    print(sess.run([v1, v2, ema.average(v1), ema.average(v2)]))

"""
Before: 
v1:0
v2:0
After: 
v1:0
v2:0
v1/ExponentialMovingAverage:0
v2/ExponentialMovingAverage:0
2018-08-17 11:03:37.258476: I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
[10.0, 5.0, 0.099999905, 0.049999952]
"""
```

```python
# 取滑动平均
avgV1 = tf.Variable(0, dtype=tf.float32, name='avg-v1')
avgV2 = tf.Variable(0, dtype=tf.float32, name='avg-v2')
# 通过命名的方式读取滑动平均值
saver = tf.train.Saver({"v1/ExponentialMovingAverage": avgV1,
                        "v2/ExponentialMovingAverage": avgV2})
with tf.Session() as sess:
    saver.restore(sess, SAVE_MODEL_PATH)
    print("avg v1", sess.run(avgV1))
    print("avg v2", sess.run(avgV2))
    
"""
avg v1 0.0999999
avg v2 0.05
"""
```


从上面的代码可以发现, 如果` Saver`中的字典很多的时候使用就不太方便. `tf.train.ExponentialMovingAverage` 类提供了自动生成类所需要的变量重命名字典.

修改之前的代码为:

```python
# 取滑动平均
# avgV1 = tf.Variable(0, dtype=tf.float32, name='avg-v1')
# avgV2 = tf.Variable(0, dtype=tf.float32, name='avg-v2')
# 通过命名的方式读取滑动平均值
# saver = tf.train.Saver({"v1/ExponentialMovingAverage": avgV1,
#                         "v2/ExponentialMovingAverage": avgV2})

# 自动生成重命名字典, 自动生成的是根据 name 字段的名字来生成
avgV1 = tf.Variable(0, dtype=tf.float32, name='v1')
avgV2 = tf.Variable(0, dtype=tf.float32, name='v2')
ema = tf.train.ExponentialMovingAverage(0.99)
renameDict = ema.variables_to_restore()
print("renameDict=", renameDict)
saver = tf.train.Saver(renameDict)

with tf.Session() as sess:
        saver.restore(sess, SAVE_MODEL_PATH)
        print("avg v1", sess.run(avgV1))
        print("avg v2", sess.run(avgV2))

"""
renameDict= {'v2/ExponentialMovingAverage': <tf.Variable 'v2:0' shape=() dtype=float32_ref>, 'v1/ExponentialMovingAverage': <tf.Variable 'v1:0' shape=() dtype=float32_ref>}
avg v1 0.0999999
avg v2 0.05
"""
```

### convert_variables_to_constants 转成常量保存

之前的方法会保存运行 TensorFlow 程序所需要的全部信息,然而有时并不需要某些信息.
比如在测试或者离线预测时,只需要知道如何从神经网络的输入层经过向前传播得到输出层即可,而不需要变量的初始化等辅助节点信息.


利用 `convert_variables_to_constants` 函数将变量及其取值通过常量的方式保存.

```python
v3 = tf.Variable(tf.constant(3.0, shape=[1]), name='v3')
    v4 = tf.Variable(tf.constant(4.0, shape=[1]), name='v4')
    result = v3 + v4

    init_op = tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init_op)
        # 导出当前计算图的 GraphDef 部分, 完成输入层到输出层的计算过程
        graph_def = tf.get_default_graph().as_graph_def()

        # 下面输出 Result: Tensor("add:0", shape=(1,), dtype=float32)
        print("Result: ", result)

        # 将图中的变量及其取值转化为常量, 同时去掉不必要节点.
        # add 是节点名称, 表示相加操作.
        output_graph_def = graph_util.convert_variables_to_constants(sess, graph_def, ['add'])
        print('output_graph_def: ', output_graph_def)
        """ 输出
        output_graph_def:  node {
          name: "v3"
          op: "Const"
          attr {
            key: "dtype"
            value {
              type: DT_FLOAT
            }
          }
          attr {
            key: "value"
            value {
              tensor {
                dtype: DT_FLOAT
                tensor_shape {
                  dim {
                    size: 1
                  }
                }
                float_val: 3.0
              }
            }
          }
        }
        node {
          name: "v3/read"
          op: "Identity"
          input: "v3"
          attr {
            key: "T"
            value {
              type: DT_FLOAT
            }
          }
          attr {
            key: "_class"
            value {
              list {
                s: "loc:@v3"
              }
            }
          }
        }
        node {
          name: "v4"
          op: "Const"
          attr {
            key: "dtype"
            value {
              type: DT_FLOAT
            }
          }
          attr {
            key: "value"
            value {
              tensor {
                dtype: DT_FLOAT
                tensor_shape {
                  dim {
                    size: 1
                  }
                }
                float_val: 4.0
              }
            }
          }
        }
        node {
          name: "v4/read"
          op: "Identity"
          input: "v4"
          attr {
            key: "T"
            value {
              type: DT_FLOAT
            }
          }
          attr {
            key: "_class"
            value {
              list {
                s: "loc:@v4"
              }
            }
          }
        }
        node {
          name: "add"
          op: "Add"
          input: "v3/read"
          input: "v4/read"
          attr {
            key: "T"
            value {
              type: DT_FLOAT
            }
          }
        }
        library {
        }
        """
        # 导出模型, 存入文件
        with tf.gfile.GFile("./SaveModels/model3.pb", 'wb') as f:
            outputData = output_graph_def.SerializeToString()
            # 以下输出
            # b'\n3\n\x02v3\x12\x05Const*\x19\n\x05value\x12\x10B\x0e\x08\x01\x12\x04\x12\x02\x08\x01*\x04\x00\x00
            # @@*\x0b\n\x05dtype\x12\x020\x01\n7\n\x07v3/read\x12\x08Identity\x1a\x02v3*\x07\n\x01T\x12\x020\x01*
            # \x15\n\x06_class\x12\x0b\n\t\x12\x07loc:@v3\n3\n\x02v4\x12\x05Const*\x19\n\x05value\x12\x10B\x0e
            # \x08\x01\x12\x04\x12\x02\x08\x01*\x04\x00\x00\x80@*\x0b\n\x05dtype\x12\x020\x01\n7\n\x07v4/read\x12
            # \x08Identity\x1a\x02v4*\x07\n\x01T\x12\x020\x01*\x15\n\x06_class\x12\x0b\n\t\x12\x07loc:@v4\n%\n\x03
            # add\x12\x03Add\x1a\x07v3/read\x1a\x07v4/read*\x07\n\x01T\x12\x020\x01\x12\x00'
            print('Serialize Data: ', outputData)
            f.write(outputData)
```

以上是保存节点代码, 以下是加载节点并执行结果的代码:

```python
# 省略之前都有的 import
from tensorflow.python.platform import gfile

# Read pb file
with tf.Session() as sess:
    filePath = './SaveModels/model3.pb'
    with gfile.FastGFile(filePath, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())

    result = tf.import_graph_def(graph_def, return_elements=["add:0"])
    print(sess.run(result))
    # 输出结果
    # [array([ 7.], dtype=float32)]
    
```


