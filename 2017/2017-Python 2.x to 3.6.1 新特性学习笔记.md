---
title: Python 2.x to 3.6.1 新特性学习笔记
subtitle: p2t3note
date: 2017-06-12 11:30:00
tags: Python
---

<!--# Python 2.x to 3.6.1 新特性学习笔记-->

先附上官方英文文档地址 : [https://docs.python.org/3/whatsnew/3.6.html](https://docs.python.org/3/whatsnew/3.6.html)

## 3.6 新特性

###  新语法特性:

* 新的格式化字符串方式: f-strings.</br>在格式化字符串前加入前缀 'f' 或 'F' 等同于 str.format() </br>

```
> name = 'GrayLand'
> b = f'My name is {name}.'
'My name is GrayLand.'
> f'My name is {name!r}.' # !r == repr(), name!r = repr(name)
> # !r = repr(), !a = ascii(), !s = str()
"My name is 'GrayLand'."

> width = 10
> precision = 4
> value = decimal.Decimal("12.3456789") #import decimal
> f"result:{value:{width}.{precision}}"
'result:      12.35'

```

* 数字中可以增加下划线以增强可读性.

```
> 1_000_000_000
1000000000

```

* 变量增加注释, 只有在 class 中才有 \_\_annotations\_\_ 属性.

```
# a: [int] = [1,2,3,4]
# b: [str, int] = {'age':123}
# c: str = 'grayland'

>>> class Person:
...     info:[str,str] = []
... 
>>> Person.__annotations__
{'info': [<class 'str'>, <class 'str'>]}
```

* 异步生成器

```
async def ticker(delay, to):
    """Yield numbers from 0 to *to* every *delay* seconds."""
    for i in range(to):
        yield i
        await asyncio.sleep(delay)
```

* asynchronous comprehensions


### 新的库:

* secrets 

### CPython 实现增强:

* dict 重写实现方法, 相比 python3.5 内存减少20%~25%.
* 简化自定义类的创建语法. 自定义一个子类的时候可以不使用 \_\_metaclass\_\_ , 一个类被继承的时候,自动调用 \_\_init\_subclass\_\_.
* 类属性定义顺序现在是被保护的.
* \**kwargs 中排列的元素和调用函数传入的对应关键字参数一致.
* DTrace 和 SystemTap 探索支持.
* 新的 PYTHONMALLOC 环境变量可以用于内存申请和访问的诊断.

