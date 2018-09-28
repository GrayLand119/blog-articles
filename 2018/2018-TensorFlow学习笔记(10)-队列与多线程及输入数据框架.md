
---

title: TensorFlow学习笔记(10) - 队列与多线程及输入数据框架
subtitle: tfln10
date: 2018-09-12 17:17:42
tags: TensorFlow
mathjax: true

---

<!--# TensorFlow学习笔记(10) - 队列与多线程及输入数据框架-->

## 队列

在 Tensorflow 中,队列和变量类似,都是计算图上的节点.
对于变量节点, 其操作为赋值操作, 修改其取值.
对于队列节点, 其操作为修改操作, 修改其状态. 主要方法有:

* Enqueue
* EnqueueMany
* Dequeue

TensorFlow 提供的队列有两种, `FIFOQueue` 和 `RandomShuffleQueue`.
`FIFOQueue`创建普通FIFO队列, `RandomShuffleQueue`创建一个随机队列, 每次出队都是随机的选择.

以下是一个出队/入队的程序:

```python
# 创建容量为2的队列, 类型为 int32
q = tf.FIFOQueue(2, 'int32')
# 入队多个 > 1, 100
init = q.enqueue_many(([1, 100],))

# 出队 > 1
x = q.dequeue()
# y = 1 + 1 = 2
y = x + 1
# 重新入队 > 100, 1
q_inc = q.enqueue([y])

with tf.Session() as sess:
    init.run()
    for _ in range(5):
        print(sess.run([x, q_inc]))
"""
输出:
[1, None]
[100, None]
[2, None]
[101, None]
[3, None]
"""
```

## 多线程

TensorFlow 提供`tf.Coordinator` 和 `tf.QueueRunner` 两个类来完成多线程协同的功能.

`tf.Coordinator` 提供以下三个函数:

* `should_stop`:启动线程需要一直查询此函数, 返回为 True 时, 当前线程需要退出
* `request_stop`: 每个线程都可以通过此函数来通知其他线程退出
* `join`: 线程数组加入到协调器中,并等待其全部结束

```python
def threadFunc(coord, work_id):
    while not coord.should_stop():
        # 随机停止
        if np.random.rand() < 0.1:
            print("Stopping from id:{0}\n".format(work_id))
            coord.request_stop()
        else:
            print("Working from id:{0}\n".format(work_id))
        time.sleep(1)


if __name__ == '__main__':
    coord = tf.train.Coordinator()
    threads = [threading.Thread(target=threadFunc, args=(coord, i)) for i in range(5)]

    for t_thread in threads:
        t_thread.start()
    
    coord.join(threads)
```

`tf.QueueRunner` 主要用于启动多个线程来操作同一个队列.

```python
# 创建队列
queue = tf.FIFOQueue(100, "float")
"""
enqueue params
vals: A tensor, a list or tuple of tensors, or a dictionary containing
    the values to enqueue.
tf.random_norma params
shape: A 1-D integer Tensor or Python array. The shape of the output tensor.
"""
# 创建队列操作
enqueue_op = queue.enqueue([tf.random_normal([1])])
# 创建线程来操作队列, 5个线程 都是 入队操作
qr = tf.train.QueueRunner(queue, [enqueue_op] * 5)
# qr 加入计算图上的指定集合, 没有指定则加入默认 tf.GraphKeys.QUEUE_RUNNERS
tf.train.add_queue_runner(qr)
# 定义出队操作
dequeue_op = queue.dequeue()

with tf.Session() as sess:
    # 创建协调器, 来协同启动的线程
    coord = tf.train.Coordinator()
    """
    使用 tf.train.QueueRunner 时, 需要明确调用 tf.train.start_queue_runners 来启用所有线程
    否则, 程序没有运行入队操作, 直接调用出队操作会一直等待入队
    
    tf.train.start_queue_runners 默认启动默认集合中的所有 QueueRunner , 即tf.GraphKeys.QUEUE_RUNNERS集合
    """
    threads = tf.train.start_queue_runners(sess=sess, coord=coord)
    # 获取队列中的取值
    for _ in range(3):
        print(sess.run(dequeue_op)[0])

    coord.request_stop()
    coord.join(threads)
```

## 输入文件队列

* `tf.train.match_filenames_once`: 获取符合正则表达式的所有文件
* `tf.train.string_input_producer`: 可管理上个函数生成文件. 是用初始化时提供的文件列表创建一个输入队列, 通过设置`shuffle`参数来打乱顺序, 打乱顺序会运行在一个单独的线程上, 不影响读取文件的速度.

`string_input_producer` 读取流程: 调用文件读取函数->判断是否有打开的文件可读->有则读,没有或已读完则出队一个文件并读取.
当队列所有数据都读完后会重新初始化, 即全部文件重新加入队列, `num_epochs` 限制了重复使用次数

`string_input_producer` 中的输入队列可以被多个线程读取, 且其中文件会被均匀分给不同的线程.

#### 模拟生成数据文件

```python
def convert_to_feature(values: list):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=values))

def genTFRecord():
    num_shards = 2
    instane_per_shard = 10
    cur_path = os.getcwd() + "/"

    for i in range(num_shards):
        filename = cur_path + "data.tfrecord-%.5d-of-%.5d" % (i, num_shards)
        print("To File:", filename)
        writer = tf.python_io.TFRecordWriter(filename)
        for j in range(instane_per_shard):
            name = "Rand data-%d" % (j)
            features = tf.train.Features(feature={
                'name': tf.train.Feature(bytes_list=tf.train.BytesList(value=[name.encode()])),
                'values': convert_to_feature(list(np.random.randint(50, 100, 1) for x in range(10)))
            })
            example: tf.train.Example = tf.train.Example(features=features)
            writer.write(example.SerializeToString())
        writer.close()
```

#### 使用文件生成器来加载文件

```python
def inputProducerDemo():
    cur_path = os.getcwd() + "/"
    # 正则匹配文件名
    ss = cur_path + "data.tfrecord-*"
    print("ss=", ss)

    files = tf.train.match_filenames_once(ss)
    # 创建输入队列
    filename_queue = tf.train.string_input_producer(files, shuffle=True)

    reader = tf.TFRecordReader()
    """
    Returns:
      A tuple of Tensors (key, value).
      key: A string scalar Tensor.
      value: A string scalar Tensor.
    """
    _, serialized_example = reader.read(filename_queue)
    features = tf.parse_single_example(serialized_example,
                                       features={
                                           'name': tf.FixedLenFeature([], tf.string),
                                           'values': tf.FixedLenFeature([10], tf.int64)
                                       })

    p1 = features['name']
    p2 = features['values']
    with tf.Session() as sess:
        tf.local_variables_initializer().run()
        print(sess.run(files))

        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(sess=sess, coord=coord)
        for i in range(6):
            print(sess.run([p1, p2]))

        coord.request_stop()
        coord.join(threads)

    """
    [b'Rand data-0', array([94, 91, 85, 73, 73, 62, 93, 68, 92, 53])]
    [b'Rand data-1', array([81, 70, 83, 61, 61, 85, 84, 56, 88, 71])]
    [b'Rand data-2', array([81, 55, 56, 88, 84, 95, 73, 81, 66, 71])]
    [b'Rand data-3', array([63, 96, 73, 52, 54, 92, 54, 67, 87, 61])]
    [b'Rand data-4', array([71, 84, 78, 62, 92, 70, 86, 54, 79, 82])]
    [b'Rand data-5', array([70, 86, 80, 93, 94, 56, 55, 57, 88, 67])]
    """
    pass
```

## 组合训练数据

上个 Demo 一次读取一个样例数据, 使用 `tf.train.batch` 和 `tf.train.shuffle_batch` 一次读取一个 batch 的数据, 后者随机读取.

设置`num_threads`参数,可以指定多个线程同时执行入队操作. >1 时,多线程会同时读取一个文件中的不同样例并行进行处理.

`tf.train.shuffle_batch_join`, 会从输入文件队列中获取不同文件分配给不同线程. 其中, 如果线程过多会导致过多硬盘寻址,从而降低效率.

主要体现逻辑的伪代码如下:

```python
example, label = features['values'], features['label']
batch_size = 3
capacity = 1000 + batch_size * 3
example_batch, label_batch = tf.train.batch([example, label], batch_size=batch_size, capacity=capacity)

with tf.Session() as sess:
    ...
    for _ in range(2):
      cur_example_batch, cur_label_batch = sess.run([example_batch, label_batch])
    ...
```

另外,自己目前使用的 `pandas`和`numpy` 也可以作为输入数据框架.