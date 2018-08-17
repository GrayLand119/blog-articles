from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf
from tensorflow.python.framework import graph_util
import os
import sys

SAVE_MODEL_PATH = "./SaveModels/model1.ckpt"

def save1():
    # with tf.variable_scope('field1'):
    v1 = tf.Variable(tf.constant(1.0, shape=[1]), name='v1')
    v2 = tf.Variable(tf.constant(2.0, shape=[1]), name='v2')
    result = v1 + v2

    init_op = tf.global_variables_initializer()

    saver1 = tf.train.Saver()

    with tf.Session() as sess:
        sess.run(init_op)
        print("All variables:", tf.global_variables())
        saver1.save(sess, "./SaveModels/model1.ckpt")

    pass

def read1():
    # 运行 save1 后直接 运行 read1 出错, v1,v2的名字冲突.
    v1 = tf.get_variable('v1', shape=[1], dtype=tf.float32, initializer=tf.constant_initializer(0.0, tf.float32))
    v2 = tf.get_variable('v2', shape=[1], dtype=tf.float32, initializer=tf.constant_initializer(0.0, tf.float32))
    # v1 = tf.Variable(tf.constant(0.0, shape=[1]), name='v1')
    # v2 = tf.Variable(tf.constant(0.0, shape=[1]), name='v2')

    result = v1 + v2

    saver2 = tf.train.Saver()

    with tf.Session() as sess:
        saver2.restore(sess, './SaveModels/model1.ckpt')
        print(sess.run(result))

    pass

def read12():
    # 直接加载图, 包含运算
    saver = tf.train.import_meta_graph('./SaveModels/model1.ckpt.meta')

    with tf.Session() as sess:
        saver.restore(sess, './SaveModels/model1.ckpt')
        print(sess.run(tf.get_default_graph().get_tensor_by_name("add:0")))

def read13():
    V1 = tf.Variable(tf.constant(0.0, shape=[1]), name='other-v1')
    V2 = tf.Variable(tf.constant(0.0, shape=[1]), name='other-v2')
    result = V1 + V2

    saver = tf.train.Saver({"v1": V1, "v2": V2})

    with tf.Session() as sess:
        saver.restore(sess, './SaveModels/model1.ckpt')
        print(V1)
        print(V2)
        print("Result=", sess.run(result))

def save2():
    # 存
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

def read2():
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

def save3():
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

def read3():
    # 加载
    from tensorflow.python.platform import gfile
    # Read pb file
    with tf.Session() as sess:
        filePath = './SaveModels/model3.pb'
        with gfile.FastGFile(filePath, 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())

        result = tf.import_graph_def(graph_def, return_elements=["add:0"])
        print(sess.run(result))
        # [array([ 7.], dtype=float32)]
    pass

if __name__ == '__main__':
    isLoop = False
    while 1:
        # print("Input Run Num:...")
        # inputStr: str = input("Input Run Num:")
        inputStr = '31'
        if inputStr == 'q' or inputStr == 'Q':
            break
        try:
            i = int(inputStr)
        except Exception as e:
            print(e)
            continue

        if i == 1:
            save1()
        elif i == 11:
            read1()
        elif i == 12:
            read12()
        elif i == 13:
            read13()
        elif i == 2:
            save2()
        elif i == 21:
            read2()
        elif i == 3:
            save3()
        elif i == 31:
            read3()

        if not isLoop:
            break



