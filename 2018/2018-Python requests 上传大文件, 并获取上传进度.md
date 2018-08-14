---

title: Python requests 上传文件, 并获取上传进度
subtitle: prufagp
date: 2018-04-19 10:40:00
tags: Python

---


<!--# Python requests 上传大文件, 并获取上传进度-->

最新在使用PyQt5开发时有个上传大文件的需求, 在查阅`Requests` 官网进阶手册 [Advanced Usage — Requests 2.18.4 documentation](http://docs.python-requests.org/en/master/user/advanced/#streaming-uploads) 中只有上传文件的几种方法介绍, 并没有提到上传进度获取.

后来发现有个基于`Requests`的扩展库`requests_toolbelt`可以实现上传进度的获取 :

[Uploading Data — requests_toolbelt 0.8.0 documentation](http://toolbelt.readthedocs.io/en/latest/uploading-data.html#monitoring-your-streaming-multipart-upload)

详细参见原文手册, 以下是我的使用总结:

## 上传数据
### Streaming Multipart Data Encoder

Requests 本身是支持 `multipart uploads`的, 但是从API上看想要构造一个灵活的 `multipart upload`是非常困难或不可能的. 另外, 当使用`Requests`的`multipart upload`功能时会加载所有的数据到内存中, 这导致在极端情况下有可能只发送了一部分文件到服务器.

`toolbelt` 包含了一个可以建立完全自定义的`multipart`请求体, 并且避免了读取文件到内存当中, 如:

```python
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

m = MultipartEncoder(
    fields={'field0': 'value', 'field1': 'value',
            'field2': ('filename', open('file.py', 'rb'), 'text/plain')}
    )

r = requests.post('http://httpbin.org/post', data=m,
                  headers={'Content-Type': m.content_type})
```

`MultipartEncoder`的方法`.to_string()`非常便捷, 它将`multipar body`转换成为`string`. 这个方法在开发的时候还是非常有用的, 它可以让你确切的看到你将要发送的数据格式.

`MultipartEncoder` 是最常用的接口, 它会为你创建一个 `multipart/form-data`请求体.

基础用法如下:

```python
import requests
from requests_toolbelt import MultipartEncoder

encoder = MultipartEncoder({'field': 'value',
                            'other_field', 'other_value'})
r = requests.post('https://httpbin.org/post', data=encoder,
                  headers={'Content-Type': encoder.content_type})
```

**注意!:** 此对象在`httplib`中结束. 而当前的`httplib`是使用硬编码来读取`8192bytes`. 这意味着这个操作将会一直循环读取, 上传将会消耗一部分时间.

## 监听你的分段流式上传

如果你是在使用一个分段的上传, 那说明你的任务将会需要执行一会, 这个时候我们需要监听上传的进度.
接下来讲一下监听上传进度. 

`toolbelt`提供两个模块`MultipartEncoder`, `MultipartEncoderMonitor`, 有以下一些相关信息:

* Monitor接收一个回调参数`callback`, 回调参数在`requests`每次调用`read`的时候调用, 并且传递当前`monitor`作为参数.
* Monitor追踪上传过程中已经加载了多少bytes.

所以, 可以使用Monitor来实现上传进度的监听.

实例代码如下:

```python
import requests
from requests_toolbelt.multipart import encoder

def my_callback(monitor):
    # Your callback function
    pass

e = encoder.MultipartEncoder(
    fields={'key1': 'value1', 'key2': 'value2',
            'fieldKey': ('filename', open('file.py', 'rb'), 'text/plain')}
    )
m = encoder.MultipartEncoderMonitor(e, my_callback)

r = requests.post('http://httpbin.org/post', data=m,
                  headers={'Content-Type': m.content_type})
                  
```

另外, `MultipartEncoder` 主要的责任应该只用于准备和流式化数据, 它不应被用于管理.