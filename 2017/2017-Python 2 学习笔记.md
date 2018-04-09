---
title: Python 2 学习笔记
subtitle: p2note
date: 2017-06-06 17:22:00
tags: Python
---

<!--# Python 2 学习笔记-->

### 常用指令
* print 打印
* id 显示内存地址
* help 帮助
* div
* type

### 整数溢出

利用模块解决除法和编码格式（支持中文）的方法

### 引入模块

1. import math
2. from xxxx1 import xxxx2 //  xxxx2是xxxx1大模块中的小模块

###  数和四则运算
divmod(5,2) 5 % 2 模

round(2.222) 四舍五入

### 字符串
```
> "Py" + "thon"

> a = 1234
  print "hehe" + `a` // 引号是1旁边的那个` 
  print "hehe" + str(a)
  print "hehe" + repr(a) // repr() is a function instead of ``
  
> name = raw_input("input your name:")

> a = 10; b = 20
> print a,b

> c = "C:\news"
> print c
> print r"C:\news"

> ord('b') // 98
> chr(98) // 'b'

> c = "abc"
> c * 3 // 'abcabcabc'
> "+" * 20 // out put 20 '+' 
```
raw_input(...) </br>

raw_input([prompt]) -> string </br>Read a string from standard input. The trailing newline is stripped.</br>If the user hits EOF (Unix: Ctl-D, Windows: Ctl-Z+Return), raise EOFError.</br>
On Unix, GNU readline is used if enabled. The prompt string, if given,is printed without a trailing newline before reading. </br>

### 基本操作
1. len()
2. in // return False or Ture
3. max()
4. min()
5. cmp(str1,str2) // same is 0, less is -1 , bigger is 1
6. +

### 格式化输出
```
> a = "grayland"
> "my name is %s" % a
> "my name is {}".format(a)
> "my name is {name}, age is {age}".format(name=a, age=27) // 推荐
> "my name is %(name)s"%{"name":a}
```

### 常用方法
```
> a = "my name is grayland"
> a.split(" ") // return a list, 反过来是 join

> a.strip() // 去掉左右空格
> a.lstrip(), a.rstrip()

> a.upper()
> a.lower()
> a.capitalize() // First character uppper
> a.isupper()
> a.islower()
> a.istitle()
```

## Python 避免中文是乱码

1. \# -*- coding: utf-8 -*- // -*- 没有用
2. \# coding:utf-8
3. unicode_str = unicode('中文', encoding='utf-8') // 遇到字符(节)串，立刻转化为 unicode，不要用 str()，直接使用 unicode()
4. import codecs</br>codecs.open('filename', encoding='utf8') </br>遇到字符(节)串，立刻转化为 unicode，不要用 str()，直接使用 unicode()

## 索引和切片

```
> a = "python"
  a[0]
  // p
  a[1]
  // y
  a.index("p")
  // 0
  a[1:3]
  // 'yt'
  a[1:99999]
  a[1:] // index 1 to end
  a[:] // get all
  a[:3] // first to 3
  
```

## 列表 List
相当于 NSArray. 列表可以无限大.

* insert(index, obj) 
* append 添加元素 listA.append(obj), obj必须是 iterable 可迭代的.
* extend 扩展 listA.extend(listB)
* remove(obj) only remove the first object, if obj not exist cause an error.
* pop(index) if index not exist , then remove the last.
* reverse()
* sort()
* + same as extend

list str 转化:

* split
* join


判断对象是否可迭代:</br>
判断其属性有 '__iter__'属性</br>
> hasattr(obj, '__iter__') // Trure or False

## 元组 tuple

元组是用圆括号括起来的，其中的元素之间用逗号隔开。</br>
元组中的元素类型是任意的 Python 数据。</br>
元组不能修改, list 和 str 的融合产物

* tuple 操作比 list 快.
* 不能修改数据, 安全
* tuple 可以用作 key,list 不可以
* tuple 可以用在字符串格式化总

> a = 111,222,'ccc' // then a is tuple

元组可以用于格式化:
> "my name is %s, age is %d"%("grayland", 27)

## 字段 dict

创建字典:

```
> dictA = {}
> dictA = {'key'='value'}
> dictA['key'] = 'value'
> dictA = dict((['key1':'value1'], ['key2':'value2'])) // 利用元组构造
> dictA = dict(key='value',key2='value')
> dictA = {}.formkeys(('key1','key2'), 'value')
```

访问字典:

```
> D = {'name':'grayland, 'age':27}
> D['gender'] // Error
> D.get('gender') // get nothing
```

其他方法:

* len(dictX) // get the num of key-value.
* del d[key] // delete the key-value pair in the dict 'd'.
* key in d
* copy // a = b.copy(), **import copy, can use copy.deepcopy(obj)**
* clear()->None // Remove all items
* get(key)
* get(key, default) // If key no exist, return default.
* setdefault() // as get(key,default), but if key not exist then add to de dict
* items() // return list[(tuple), (tuple), ...]
* pop(key)
* popitems() // Random to pop 1 key-value pair
* update(dictX) // Cover with dictX
* has_key(key)

字符串格式化输出:

> "my name is %(key)s" % {'key':'value'} // >> 'my name is value'

## 集合 Set

无序，不重复.</br>
tuple 类似 list 和 str 的集合. </br>
set 类似 list 和 dict 的集合.</br>

```
> s1 = set('abcdefff')
  set(['a', 'c', 'b', 'e', 'd', 'f']) // It haven't repeat element
  s1 = {'a','b','c','d','e','f','f','f'} same as set(...)
```

其他:
> add(obj)
> pop()
> remove(obj)
> discard(obj) // same as remove(obj), but if not exist do nothing.
> clear()
> issubset(setB)
> | 
> &
> diffenece(setB) // 取反

## 语句

print obj, // 用在循环中, 不换行. 否则换行

### import

```
> import math

> from math import pow

> from math import pow as pingfang

> from math import pow, e, pi

> from math import *
```

###  赋值语句
```
> x,y,z = 1,2,3
> x = 1,2,3
> x,y = y,x // 相当于 a=x;x=y;y=a; 实现对调
> x = y = 123 // 链式赋值, x = 123, y = 123 , 指向同一个地址.
> 
```

###  条件语句

```
// If/else/elif
// 必须通过缩进方式来表示语句块的开始和结束.
// 缩进使用四个空格
if xxx in xxxx:
...
elif:
...
else:
...

```

### while

```
// while ...
while True:
	if a:
		break

//while...else
while ...:
	...
else:
	...

// for...else
for ... in ...:
	...
else:
	...



```

###  三元操作符

> a = y if x else z // 如果 x is True return y else return z.

### 循环

```
> for i in "hello":
> for i in listA:
> for i in range(start, stop, step)
> for key in dictA:
> for k,v in dictA.items():
> for k,v in dictA.iteritems():
```

### 并行迭代

```
> a = [1,2,3,4,5]
> b = [9,8,7,6,5]
> // 求 ab 每项的和
> for i in range(len(a)):
>     c.append(a[i]+b[i])
> // c = [10,10,10,10,10]
> 
> for x,y in zip(a,b):
>     c.append(x+y)
> // c = [10,10,10,10,10]
> 
```

enumerate(listA) -> (index, listA[index])
enumerate(listA, start=10) -> (index+10, listA[index])


### list 解析

for i in range(1,4):
	a.append(i**2)

\> [1,4,9]

list 解析:
a = [x**2 for x in range(1,4)]

\> a = [1,4,9]


##  打开文件

```
> f = open("xxx.txt")
> for line in f:
> 	print line,

// f 类型是 file
// 此时 f 已经到了文件的末尾, 再遍历将不会输出东西. 
// close() 关闭并保存

with ... as ...: // 可以实现保存

```

## 文件状态

import os

os 模块中有 文件状态的方法 stat(path)

import time // 时间相关模块

### read/readline/readlines

#### read:

read([size]) -> read at most size bytes, returned as a string.
If the size argument is negative or omitted, read until EOF is reached. Notice that when in non-blocking mode, less data than what was requested may be returned, even if no size parameter was given.

#### readline:

readline([size]) -> next line from the file, as a string.
Retain newline. A non-negative size argument limits the maximum number of bytes to return (an incomplete line may be returned then). Return an empty string at EOF.

#### readlines:

readlines([size]) -> list of strings, each a line from the file.
Call readline() repeatedly and return a list of the lines so read.The optional size argument, if given, is an approximate bound on the total number of bytes in the lines returned.* seek(offset, whence) // whence default = 0, </br>0 - offset from begin offset must be positive +</br>1 - offset from current, offset should be positive/nagative +/-</br> 2 - offset from the end, offset must be nagative. -
* tell() // get current position

## 迭代
### 逐个访问
```
> lst = ['g', 'r', 'a', 'y', 'l', 'a', 'n', 'd']

> for s in lst:
> 
> lst_iter = iter(lst)
> lst_iter.next()
> lst_iter.next()
> lst_iter.next()
> ...
> 
> 
```

### 文件迭代器
```
> f = open(...)
> f.readline() 
> f.next()
> is same.
> 
> listA = list(open(...)) // 可以获得文件的内容
> tupleA = tuple(open(...))
> 
> "stringAppend".join(open(...)) // file.readline->append(..>) then join
> a,b,c,d,e = open(...) // a,b,c,d,e 分别赋值 file.readline()
> 
```


## 自省

1. help() 进入 help 模式
2. help(...)
3. dir(...)
4. \_\_doc\_\_
5. \_\_builtins\_\_
6. callable() 测试函数可调用性
7. isinstance('strxxxxx', str) -> True
8. issubclass(classB, classA) -> BOOL


##  函数

f(x) = ax + b

...

**变量本质上是一个占位符**

### 定义

**def func(inputA, inputB,...):**

**def func(X=default,Y=default):**

**def func(a,*arg):** // *arg表示多个可变参数 (tuple 类型传递)

变量无类型,对象有类型

Python 中为对象编写接口,而不是为数据类型

### 命名

* 文件名:全小写,可以使用下划线
* 函数名:小写,可以用下划线风格增加可读性 或 类似myFunction这样的驼峰命名法
* 变量:全小写

### 文档

\#: 注释

""" ... """: 三个引号包围表示文档, 可以用 \_\_doc\_\_ 查看

### 传值方式

```
> def funA(a,b):
> funA(1,2)
> input = (1,2)
> funA(input) // 元组参数
> 
> funB(**dict) // 字典参数
> func(*args) // 可变参数
```
### 特殊函数

* filter(func, seq) // func(x)->bool
* map(func, seq) // excute func(x) in seq
* reduce(func, seq) // func(func(func(0,1),2),3),...
* lambda // lambda input:output
* yield


lambda:

```
> nums = range(10)
> [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
所有数+3
// Normal:
> result = [i+3 for i in nums]
// lambda:
> lam = lambda x:x+3
> for i in numbers:
>     result.append(lam(i))
// map:
> def add(x):
> ...
> map(add,nums)
// filter: 
// 过滤大于5的数
> [x for x in nums if x>5] // Mathod1
> filter(lambda x:x>5, nums) // Mathod2

```

## 类 class

对象的相关定义:

* 对象
* 状态
* 行为
* 标识

简化后就是: 属性和方法


### 定义
####  旧类

深

```
> class Person:
>     pass
> ...
> oldClass = Person()
> oldClass.__class__
> <class __main__.Person at 0x10a644ef0>
> type(Person)
> <type 'classobj'>
```
#### 新类

广

```
> class NewPerson(object):
>     pass
> ...
> newClass = NewPerson()
> type(newClass)
> <class '__main__.NewPerson'>
> type(NewPerson)
> <class '__main__.NewPerson'>
> 
> __metaclass__ = type // 写在这句之下的都是新类,即便没有(object)
> 
```

(object) 表示继承自 object 类. Python3 中全部继承自 object 类.


### 初始化

```
> def __init__(self, *args) // self 是必须的
```

###  类属性和实例属性

可以动态修改和增加
```
> Person.propertyA = 'new value'
> obj1 = Person()
> obj1.newProperty = 'new value'
```

### 命名空间


* 内置命名空间(Built-in Namespaces):Python 运行起来，它们就存在了。内置函数的命名空间都属于内 置命名空间，所以，我们可以在任何程序中直接运行它们，比如前面的 id(),不需要做什么操作，拿过来就直 接使用了。
* 全局命名空间(Module:Global Namespaces):每个模块创建它自己所拥有的全局命名空间，不同模块的全 局命名空间彼此独立，不同模块中相同名称的命名空间，也会因为模块的不同而不相互干扰。
* 本地命名空间(Function&Class: Local Namespaces):模块中有函数或者类，每个函数或者类所定义的命 名空间就是本地命名空间。如果函数返回了结果或者抛出异常，则本地命名空间也结束了。

 查看命名空间:

> print locals()

> print golbals()
 
###  多重继承顺序

#### 广度优先

```
> def class A1(B1, B2):
> def class A2(B1, B2):
> def class C1(A1, A2):
> 
> C1.func()
> C1->A1->A2->B1->B2 // 广度优先 新类
> C1->A1->B1->B2->A2->B1->B2 // 深度优先 旧类
```

### super 函数

super(Class, self).__init__()

### 绑定方法

def func() 就是绑定方法

### 非绑定方法

父类的方法都是非绑定方法

### 调用非绑定方法

super(BaseClass, self).function()

### 静态方法和类方法

* @staticmethod
* @classmethod

静态方法参数没有 self.
类方法参数没有 self. 但是有 cls.

### 封装和私有化

私有化:
方法数据名字前面加双下划线.

在方法前加 @property ,  obj.fun()-> obj.fun

###  特殊方法

```
__dict__:
动态添加修改删除属性的保存字典, 存储对象成员.


__slots__:
锁定类型, __dict__将不存在, 所有的属性都是类属性, 实例访问是 readonly, 不能进行修改, 若要修改,只能通过类调用修改.

__setattr__(self,name,value):
obj.property = xxxx, 赋值时候调用 __setattr__, 可以重写其拦截.

__getattr__(self,name) old:
__getattribute__(self,name):
obj.property , 获取值时调用.

newProperty = propetty(getFunc,setFunc) # 第一个是 getter,第二个是 setter.顺序不能换
obj.newProperty = xxx ->obj.setFunc

```

##  迭代器

重写 \_\_iter\_\_ , next() -> raise StopIteration()

## 生成器

### 简单的生成器

把含有 yield 的语句函数称作生成器. 生成器是一种用普通函数语法定义的迭代器. 生成器也是迭代器, 使用 yield 语句,普通的函数就成了生成器,且具备迭代器功能特性.

```
> a = (x*x for x in range(4)) # 迭代的, 遍历一遍后再输出就没有
> for i in a:
>     print i,

> a = [x*x for x in range(4)] # 生成全部, 遍历输出一直有值
> 
> def g():
>     yiled 0
>     yiled 1
>     yiled 2
> 
> a = g()
> a.next() 
> ...
> 
> 
```

生成器解析式是有很多用途的，在不少地方替代列表，是一个不错的选择。特别是针对大量值的时候，如上节所说的，列表占内存较多，迭代器(生成器是迭代器)的优势就在于少占内存，因此无需将生成器(或者说是迭代器)实例化为一个列表，直接对其进行操作，方显示出其迭代的优势。比如:

```
> sum(i*i for i in range(10)) # 可以少写一个 ()
```

### yiled

yiled 和 retur 的区别:

一般函数遇到 return 则返回并停止.</br>
遇到 yield 则挂起, 再遇到则从挂起位置继续运行,直到结束抛出异常 StopIteration()

### 生成器方法

python2.5以后, 生成器可以在运行后给其提供新的值.

```
> def r(n):
> 		while True:
> 			n = (yield n)
> 
> a = r(n)
> a.send('xxx') # Error, 要先启动(next())才能 send.
> a.next() # 4
> a.next() # 4
> a.send('xxx') # 'xxx'
> a.next() # 空 None
> 
```

调用一次 send(None)就是触发一次 参数是 None 的 next. </br>
调用一次 next()就是触发一次 send(n),但 send(n)之后的 yield n -> None

* throw(type, value=None, traceback=None):用于在生成器内部(生成器的当前挂起处，或未启动时在定 义处)抛出一个异常(在 yield 表达式中)。
* close():调用时不用参数，用于关闭生成器。

	
##  错误和异常
### 错误

语法错误和逻辑错误, 遇到错误, 抛出异常.

### 异常

当 Python 抛出异常的时候，首先有“跟踪记录(Traceback)”，还可以给它取一个更优雅的名字“回溯”。后 面显示异常的详细信息。异常所在位置(文件、行、在某个模块)。最后一行是错误类型以及导致异常的原因。

| 异常 | 描述 |
|:--|:--|
| NameError | 尝试访问一个没有申明的变量 |
| ZeroDivisionError | 除数为 0 |
| SyntaxError | 语法错误 |
| IndexError | 索引超出序列范围 |
| KeyError | 请求一个不存在的字典关键字 |
| IOError | 输入输出错误(比如你要读的文件不存在) |
| AttributeError | 尝试访问未知的对象属性 |### 处理异常

try...except...(else...)(finally...)

try...except...except... 处理多个异常

try...except (Error1,Error2):...

try...except (Error1,Error2), e: ...

try...except Exception,e

Python3.x:</br>
try...except(Error1,Error2) as e: ...

except 后面也可以没有任何异常类型，即无异常参数。如果这样，不论 try 部分发生什么异常，都会执行 excep t。

raise 将异常信息抛出

```
> try:
> 	pass
> except NameError:
> 	pass
> 
> ...

```
	eval(...)

### assert

assert 1 # Fine

assert 0 # Throw Error

* 防御性的编程* 运行时对程序逻辑的检测* 合约性检查(比如前置条件，后置条件) 
* 程序中的常量* 检查文档


##  模块

模块是程序 .py 文件.

自定义模块还需要 python 能找到你的文件. 

```
> import sys 
> sys.path.append(yourPath)
> impot YourPythonModule
> YourPythonModule.protery
> YourPythonModule.func()
> ...
```
之后会增加 YourPythonModule.pyc 文件

如果是作为程序执行
```
 __name__ == "__main__" 
 ```

如果作为模块引入 ```__name__ == "YourPythonModule"```

在一般情况下，如果仅仅是用作模块引入，可以不写 ```if __name__ == "__main__"``` 。

### PYTHONPATH 环境变量

### \_\_init__.py 方法

是一个空文件，将它放在某个目录中，就可以将该目录中的其它 .py 文件作为模块被引用。

## 标准库
### 引用方式

import xxxxx

```
> import pprint
> pprint.pprint(xxxx)

> from pprint import pprint
> pprint(xxxx)

> import pprint as p
> p.pprint(xxxx)

```

\_\_file__ 查看库的源文件


### sys
#### argv

```
import sys
sys.argv #入口参数 第一个一般是文件名

print "The file name: ", sys.argv[0]print "The number of argument", len(sys.argv) 
print "The argument is: ", str(sys.argv)

```

#### exit

* sys.exit() 		# 退出当前程序 返回 SystemExit
* sys.exit(0) 	# 正常退出
* sys.exit('some infomation')
* sys_exit() 		# 退出当前程序

#### path
查找模块的搜索目录

#### stdin,stdout,stderr

变量都是类文件流对象.

stdin-> raw_input() -> python3.x -> input()

print() -> stdout.write(obj+'\n')

输出到文件中:
```
> f = open(path,'w')
> sys.stdout = f
> ...
> print '...' # 写到文件中
> ...
> f.close()
```

### OS
#### 重命名,删除文件

* rename(old,new)
* remove(path) #删除文件, 不能删除目录
* listdir()
* getcwd() #当前工作目录
* chdir(path) #改变当前工作目录 -> cd
* pardir() #获得父级目录 -> ..
* makedir
* makedirs #中间的目录也会被建立起来
* removedirs #删除空目录
* shutil.rmtree(dir)

#### 文件和目录属性

* stat(path)
* chmod()
* system(shellCommand) #当前线程执行
* exec() or execvp() #新的进程中执行

#### 打开浏览器

```
> import os
> os.system(browserPath + " www.baidu.com")

> import webbrowser as w
> w.open(url)

```

### heapq

['__about__', '__all__', '__builtins__', '__doc__', '__file__', '__name__', '__package__', '_heapify_max', '_heappushpop_max', '_nlargest', '_nsmallest', '_siftdown', '_siftdown_max', '_siftup', '_siftup_max', 'chain', 'cmp_lt', 'count', 'heapify', 'heappop', 'heappush', 'heappushpop', 'heapreplace', 'imap', 'islice', 'itemgetter', 'izip', 'merge', 'nlargest', 'nsmallest', 'tee']

* heappush(heap, item)
* heappop() # pop minimun item
* heapify() # list to heap
* heapreplace(heap, item) # pop then push

### deque

['__class__', '__copy__', '__delattr__', '__delitem__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__iadd__', '__init__', '__iter__', '__le__', '__len__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', 'append', 'appendleft', 'clear', 'count', 'extend', 'extendleft', 'maxlen', 'pop', 'popleft', 'remove', 'reverse', 'rotate']

* deque(list)->deque object
* append(item) #right
* appendleft(item) #left
* pop() #right
* popleft() #left
* extend() #left
* extendleft() #right
* rotate(offset) #正数, 指针左移. 负数,指针右移


### calendar

import calendar

['Calendar', 'EPOCH', 'FRIDAY', 'February', 'HTMLCalendar', 'IllegalMonthError', 'IllegalWeekdayError', 'January', 'LocaleHTMLCalendar', 'LocaleTextCalendar', 'MONDAY', 'SATURDAY', 'SUNDAY', 'THURSDAY', 'TUESDAY', 'TextCalendar', 'TimeEncoding', 'WEDNESDAY', '_EPOCH_ORD', '__all__', '__builtins__', '__doc__', '__file__', '__name__', '__package__', '_colwidth', '_locale', '_localized_day', '_localized_month', '_spacing', 'c', 'calendar', 'datetime', 'day_abbr', 'day_name', 'error', 'firstweekday', 'format', 'formatstring', 'isleap', 'leapdays', 'main', 'mdays', 'month', 'month_abbr', 'month_name', 'monthcalendar', 'monthrange', 'prcal', 'prmonth', 'prweek', 'setfirstweekday', 'sys', 'timegm', 'week', 'weekday', 'weekheader']

* calendar(year) # 打印日历
* isleap # 是否是闰年
* leapdays(y1,y2) # 两年之间的闰年总数
* month(year,month) # 打印月份
* monthcalendar(year,month) #返回当月天数的嵌套数组
* monthrange(year,month) #->(a,b) 该月第一天是星期几, 一共有几天
* wekkday(year,month,day) #-> 星期几


### time

import time

* time() # -> now
* localtime() # -> year,month,monthday,hour,min,sec,wday,yday,isdst(夏令时)
* gmtime() # 格林威治时间 GMT
* asctime() # friendly ui like ->  Mon Jan 12 00:00:00 2017
* mktime(timelist) -> number
* strftime(fmt) # strftime('%Y-%m-%d %H:%M:%S')->'2017-06-09 16:09:45'
* strptime(input, fmt) # -> numbers strftime 的反转换

### datetime

* date: 日期类，常用的属性有 year/month/day
* date.today()
* date.ctime()
* date.timetuple()
* date.toordinal()
* time: 时间类，常用的有 hour/minute/second/microsecond
* datetime:  期时间类
* timedelta: 时间间隔类
* tzinfo: 时区类

### urllib

网络模块
 
['ContentTooShortError', 'FancyURLopener', 'MAXFTPCACHE', 'URLopener', '__all__', '__builtins__', '__doc__', '__file__', '__name__', '__package__', '__version__', '_asciire', '_ftperrors', '_get_proxies', '_get_proxy_settings', '_have_ssl', '_hexdig', '_hextochr', '_hostprog', '_is_unicode', '_localhost', '_noheaders', '_nportprog', '_passwdprog', '_portprog', '_queryprog', '_safe_map', '_safe_quoters', '_tagprog', '_thishost', '_typeprog', '_urlopener', '_userprog', '_valueprog', 'addbase', 'addclosehook', 'addinfo', 'addinfourl', 'always_safe', 'base64', 'basejoin', 'c', 'ftpcache', 'ftperrors', 'ftpwrapper', 'getproxies', 'getproxies_environment', 'getproxies_macosx_sysconf', 'i', 'localhost', 'noheaders', 'os', 'pathname2url', 'proxy_bypass', 'proxy_bypass_environment', 'proxy_bypass_macosx_sysconf', 'quote', 'quote_plus', 're', 'reporthook', 'socket', 'splitattr', 'splithost', 'splitnport', 'splitpasswd', 'splitport', 'splitquery', 'splittag', 'splittype', 'splituser', 'splitvalue', 'ssl', 'string', 'sys', 'test1', 'thishost', 'time', 'toBytes', 'unquote', 'unquote_plus', 'unwrap', 'url2pathname', 'urlcleanup', 'urlencode', 'urlopen', 'urlretrieve']


```
> import urllib as T
> data = T.urlopen("http:....")
> print data.read()
> 
> #data Is iterable
> data.info()
> data.getcode() # return status code - 200
> data.geturl()
> 
```

* **urlopen(url,PostData,proxies)** -> 'class to add info() and geturl() methods to an open file.'
* **urlretrieve(url,localpathname, 回调=None,请求数据=None)** # 回调 args->a,b,c progress = 100.0 * a * b / c


#### 编解码

* quite(string[,safe]): 对字符串进行编码。参数 safe 指定了不需要编码的字符
* urllib.unquote(string) :对字符串进行解码
* quote_plus(string [ , safe ] ) :与 urllib.quote 类似，但这个方法用'+'来替换空格 ' ' ，而 quote 用'%2 0'来代替空格
* unquote_plus(string ) :对字符串进行解码;
* urllib.urlencode(query[, doseq]):将 dict 或者包含两个元素的元组列表转换成 url 参数。例如{'name': 'laoqi', 'age': 40}将被转换为"name=laoqi&age=40"
* pathname2url(path):将本地路径转换成 url 路径


### urllib2

urllib2 是另外一个模块，它跟 urllib 有相似的地方——都是对 url 相关的操作，也有不同的地方。

['AbstractBasicAuthHandler', 'AbstractDigestAuthHandler', 'AbstractHTTPHandler', 'BaseHandler', 'CacheFTPHandler', 'FTPHandler', 'FileHandler', 'HTTPBasicAuthHandler', 'HTTPCookieProcessor', 'HTTPDefaultErrorHandler', 'HTTPDigestAuthHandler', 'HTTPError', 'HTTPErrorProcessor', 'HTTPHandler', 'HTTPPasswordMgr', 'HTTPPasswordMgrWithDefaultRealm', 'HTTPRedirectHandler', 'HTTPSHandler', 'OpenerDirector', 'ProxyBasicAuthHandler', 'ProxyDigestAuthHandler', 'ProxyHandler', 'Request', 'StringIO', 'URLError', 'UnknownHandler', '__builtins__', '__doc__', '__file__', '__name__', '__package__', '__version__', '_cut_port_re', '_have_ssl', '_opener', '_parse_proxy', '_safe_gethostbyname', 'addinfourl', 'base64', 'bisect', 'build_opener', 'ftpwrapper', 'getproxies', 'hashlib', 'httplib', 'install_opener', 'localhost', 'mimetools', 'os', 'parse_http_list', 'parse_keqv_list', 'posixpath', 'proxy_bypass', 'quote', 'random', 'randombytes', 're', 'request_host', 'socket', 'splitattr', 'splithost', 'splitpasswd', 'splitport', 'splittag', 'splittype', 'splituser', 'splitvalue', 'ssl', 'sys', 'time', 'toBytes', 'unquote', 'unwrap', 'url2pathname', 'urlopen', 'urlparse', 'warnings']

#### Request

```
// 请求一个页面数据
> req = urllib2.Request("...") #建立连接
> response = urllib2.urlopen(req)
> page = response.read()
> print page

// 一个 POST 例子
> url = '...'
> 
> userAgent = 'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/58.0.3029.110 Mobile/13B143 Safari/601.1.46'
> headers = {'User-Agent':userAgent}
> params = {key:value,...}
> 
> data = urllib.urlencode(params) #编码
> req = urllib2.Request(url,data,headers) #请求
> response = urllib2.urlopen(req) #开始请求并接受返回信息
> pagedata = response.read() #读取反馈内容
> 
// 除此之外还可以设置:
// HTTP Proxy
// Timeout
// redirect
// cookit
```

## XML

Summary from w3school:

* XML 指可扩展标记语言(EXtensible Markup Language)* XML 是一种标记语言，很类似 HTML* XML 的设计宗 是传输数据，而非显示数据* XML 标签没有被预定义。您需要自行定义标签。* XML 被设计为具有自我描述性。* XML 是 W3C 的推荐标准

import xml

xml.\_\_all\_\_ </br>
['dom', 'parsers', 'sax', 'etree']:

* xml.dom.* 模块:</br>Document Object Model。适合用于处理 DOM API。它能够将 xml 数据在内存中解析 成一个树，然后通过对树的操作来操作 xml。但是，这种方式由于将 xml 数据映射到内存中的树，导致比较 慢，且消耗更多内存。* xml.sax.* 模块:</br>simple API for XML。由于 SAX 以流式读取 xml 文件，从而速度较快，切少占用内 存，但是操作上稍复杂，需要用户实现回调函数。* xml.parser.expat:</br>是一个直接的，低级一点的基于 C 的 expat 的语法分析器。 expat 接口基于事件反 馈，有点像 SAX 但又不太像，因为它的接口并不是完全规范于 expat 库的。* xml.etree.ElementTree (以下简称 ET):</br>元素树。它提供了轻量级的 Python 式的 API，相对于 DOM，E T 快了很多 ，而且有很多令人愉悦的 API 可以使用;相对于 SAX，ET 也有 ET.iterparse 提供了 “在空 中” 的处理方式，没有必要加载整个文档到内存，节省内存。ET 的性能的平均值和 SAX 差不多，但是 API 的效率更高一点而且使用起来很方便。

 所以, 推荐使用 ElementTree:
 
```
// Python2.x> try:> 	import xml.etree.cElementTree as et> except ImportError:> 	import xml.etree.ElementTree as et
// Python3.x
> import xml.etree.ElementTree as et

```

2.x的 ElementTree 模块已经跟教程不一样了..之后再学3.x 的教程.

## JSON

* key-value pairs: Named object/record/struct/dictionary/hash table/keyed list/associative array in difference language.
* order list of array: In mostly language , it construed array.

Function:

* encoding: python object to json string
* decoding: json string to python object

Object -> JSON : json.dumps(obj)
JSON -> Object : json.loads(...)

but after ljson.loads(...), result have a char type, here is the char type list:

|Python==>|JSON|
| :-: | :-: |
|dict|object|
|list, tuple| array|
|str,unicode|string|
|int ,long ,float|number|
|True|true|
|False|false|
|None|null|

|JSON==>|Python|
| :-: | :-: |
|object|dict|
|array|list|
|string|unicode|
|number(int)|int,long|
|number(real)|float|
|true|True|
|false|False|
|null|None|

## Third Part Lib

Install mathod:

1. With code file: Python setup.py install , 这种是在本地的
2. pip: 官方推荐 pip , 第三方库管理工具.[https://pypi.python.org/pypi](https://pypi.python.org/pypi)

For example, use requests lib:

```
pip install requests
> import requests
> #get
> r = requests.get(url)
> r.cookies
> r.headers
> r.encoding # UTF-8
> r.status_code # 200 
> print r.text # ...
> r.content
> #post
> params = {key:value,...}
> r = requests.post(url, params)
> #http header
> r.headers['content-type'] # 不用区分大小写
> 
```

## 数据读写

### pickle/cpickle

pickle/cpickle 后者更快.

```
> import pickle
> f = open(path, 'wb')
> pickle.dump(listA/dictA, f, protocol=0) # protocol = 1 or True then use binary zip to achrive
> f.close()
```

### shelve

pickle 的升级版, 处理复杂数据.

```
#write
> import shelve
> s = shelve.open(path, writeback=True) # writeback=True 才可以修改已有的值
> s['name'] = 'grayland'
> ...
> s['data'] = {...}
> ...
> s.close()
#read
> s = shelve.open(path)
> name = s['name']
> ...
> data = s['data']
> ...
> for k in s:
> 	pass
> ...
> 
> 
```

## mysql

到目前为止，地球上有三种类型的数据:
* 关系型数据库:MySQL、Microsoft Access、SQL Server、Oracle、... 
* 非关系型数据库:MongoDB、BigTable(Google)、...* 键值数据库:Apache Cassandra(Facebook)、LevelDB(Google) ...
在本教程中，我们主要介绍常用的开源的数据库，其中 MySQL 是典型代表。

### 安装

```sudo apt-get install mysql-server```

### 配置

```service mysqld start```

创建好后的 root 没有密码:

```$mysql -u rootfirehare ```

进入 mysql 之后，会看到>符号开头，这就是 mysql 的命令操作界面了。

设置密码:

```mysql> GRANT ALL PRIVILEGES ON *.* TO root@localhost IDENTIFIED BY "123456";```

### 运行

```
$ mysql -u root -p Enter password:
```

```
mysql> show databases; 
+--------------------+ | Database | +--------------------+ | information_schema ||| || carstore | cutvideo | itdiffer| mysql|| performance_schema || test | +--------------------+
```

### 安装 Python-MySQLdb

Python-MySQLdb 是一个接口程序，Python 通过它对 mysql 数据实现各种操作。

如果要源码安装，可以这里下载 [Python-mysqldb](https://pypi.Python.org/pypi/MySQL-Python/)

```
sudo apt-get install build-essential Python-dev libmysqlclient-dev 
sudo apt-get install Python-MySQLdb

```

pip安装:

```
pip install mysql-Python
```

使用:

```
> import MySQLdb
```


## SQLite 
### 建立连接对象

```
> import sqlite3
> conn = sqlite3.connect("23302.db")
```

### 游标对象

```
> cur = conn.cursor()
```

* close()
* execute()
* executemany()
* fetchall()

### 创建数据库表

```
> create_table = "create table book (title text, author text, lang text)"
> cur.execute(create_table)

#添加数据
> cur.execute("insert in to books values("BookName","GrayLand", "Chinese")")
> 
> conn.commit()
> cur.close()
> conn.close() 
```

###  查询

```
> conn = sqlite3.connect(path)
> cur = conn.cursor()
> cur.execute("select * from books")
> print cur.fetchall()
> 
> #批量插入
> books = [tuple(xx,xx,xx),...]
> 
> cur.executemany("insert into book values (?,?,?)", books)
> conn.commit()
> 
> #查询插入结果
> 
> rows = cur.execute("select * from books")
> for row in rows:
> 	 print row
> 
> ...
> 
> #更新
> cur.execute("update books set title='xxx' where author='value')
> conn.commit()
> 
> cur.fetchone()
> ...
> cur.fetchall()
> ...
> 
> #删除
> cur.execute("delete from books where author='xxx'")
> conn.commit()
> 
> 
> cur.close()
> conn.close()
```

 更多参考资料 : [http s://docs.Python.org/2/library/sqlite3.html](http s://docs.Python.org/2/library/sqlite3.html)
 
 
