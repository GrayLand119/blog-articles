---
title: Xcode LLDB使用
date: 2016-03-17 17:36:23
tags:
- Xcode
- lldb
categories:
- Xcode
---

<!--# Xcode LLDB使用-->

[原文出处](http://www.dreamingwish.com/article/lldb-usage-a.html)

LLDB是个开源的内置于XCode的具有REPL(read-eval-print-loop)特征的Debugger，其可以安装C++或者Python插件。
本系列针对于已经知道何为debugger，且有gdb或者lldb使用经验的读者。对于lldb的娴熟使用者，也可以用来作为查阅手册。
这一篇，我们讲述lldb内建的命令。
lldb与gdb命令名的[对照表](http://lldb.llvm.org/lldb-gdb.html)

<!-- more -->

## 1.help命令
单单执行help命令会列出所有命令列表，用户加载的插件一般来说列在最后。
执行help 可以打印指定command的帮助信息，至于插件提供的命令，其帮助信息取决于插件本身的实现。
例如 help print会打印内建命令print的使用帮助。

## 2.print命令
print命令的简化方式有prin pri p，唯独pr不能用来作为检查，因为会和process混淆，幸运的是p被lldb实现为特指print。
实际上你会发现，lldb对于命令的简称，是头部匹配方式，只要不混淆，你可以随意简称某个命令。

	int count = 100;
>(lldb) print count
>(int) $0 = 100

\$0 是返回结果的引用名 <br>
\$0可以被用于任何其他表达式或者接收参数的命令。

## 3.expression命令
expression命令可以用来修改变量的值，当然大部分情况下，使用xcode提供的可视化编辑器更方便。
```
(lldb) p count
(NSUInteger) $4 = 12
(lldb)e count = 42
(NSUInteger) $5 = 42
```
> 实际上print相当于expression --，而--的意思是命令的参数终止，跟在--后面的都是命令的输入数据。

要打印一个对象，则需要使用e -O -- anObj，而e -O -- 的缩写正是我们常用的po命令：

```
(lldb) po $8
(
foo,
bar
)
```
要按特定格式来打印一个变量则使用p/:
```
(lldb) p 16
16
(lldb)p/x 16
0x10
(lldb) p/t 16
0b00000000000000000000000000010000
(lldb) p/t (char)16
0b00010000
```
或者使用p/c打印字符，p/s打印c字符串，详细格式查阅
[Output Formats](https://sourceware.org/gdb/onlinedocs/gdb/Output-Formats.html)

既然我们已经知道print实际上是expression --的简写，那么在p（或者po）后面跟上复杂的表达式则可以先计算表达式再打印最后的计算结果。
```
(lldb) e int $a = 2
(lldb) p $a * 19
38
(lldb) e NSArray *$array = @[ @"Saturday", @"Sunday", @"Monday" ]
(lldb) p [$array count]
3
(lldb) po [[$array objectAtIndex:0] uppercaseString]
SATURDAY
(lldb) p [[$array objectAtIndex:$a] characterAtIndex:0]
error: no known method '-characterAtIndex:'; cast the message send to the method's return type
error: 1 errors parsing expression
```
值得注意的是，一旦出现了上述错误提示，说明lldb无法判定某一步的计算结果是什么数据类型，这时需要强制类型转换来告诉lldb：
```
(lldb) p (char)[[$array objectAtIndex:$a] characterAtIndex:0]
'M'
(lldb) p/d (char)[[$array objectAtIndex:$a] characterAtIndex:0]
77
```

## 4.流程控制命令

实际上使用xcode自带的可视化工具来控制“继续”“暂停”“下一步”“进入”“跳出”更简单，但这里还是列出其所对应的命令名：

* 继续：process continue, continue, c
* 下一步：thread step-over, next, n
* 进入：thread step-in, step, s
* 跳出：thread step-out, finish, f

## 5.thread return命令
执行thread return命令可以使得当前函数立即返回，也就是说，后续代码都不会执行了。当然执行此命令可能会使得arc的计数追踪出现错乱。

> thread return命令需要一个参数来指明函数强制返回时的返回值。

## 6.断点命令

一般来说，在xcode中新建/删除“行断点”是很容易的，但是断点还有很多进阶使用方法：
条件断点、条件执行、记录日志、自动继续、重复断点跳过。
使用xcode提供的可视化工具来操作是很容易的：
![Alt text](./lldb-command-breakpoint.jpg)


## 7.在debugger中执行任意代码
```
(lldb) e char *$str = (char *)malloc(128)
(lldb) e (void)strcpy($str, "wxrld of warcraft")
(lldb) e $str[1] = 'o'
(char) $0 = 'o'
(lldb) p $str
(char *) $str = 0x00007fd04a900040 "world of warcraft"
(lldb) e (void)free($str)
```

## 8.watchpoint
watchpoint可以在某个变量被写入/读取时暂停程序运行：
```
(lldb) watchpoint set expression -- (int*)&_abc4
Watchpoint created: Watchpoint 7: addr = 0x15e36d3c size = 4 state = enabled type = w
    new value: 0x00000000
(lldb) watchpoint set v -w read _abc4
Watchpoint created: Watchpoint 8: addr = 0x15e36d3c size = 4 state = enabled type = r
    watchpoint spec = '_abc4'
    new value: 0
(lldb) watchpoint set v -w read_write _abc3
Watchpoint created: Watchpoint 9: addr = 0x15e36d38 size = 4 state = enabled type = rw
    watchpoint spec = '_abc3'
    new value: 0
```

实际上可以使用watchpoint来监视任意一段内存的读写。
使用XCode也可以方便地创建watchpoint。

> XCode的可视化debug工具中的watch是一个write类型watchpoint(也就是默认的)

另外，上述语句中 v是variable的简写，同样的，set可以简写为s，watch可以简写为wa，而-w后面的参数是不可以简写的必须为read、write或者read_write。

> 当前在arm和x86上，我们一次最多创建4个watchpoint，继续创建会提示错误。

## 9.符号断点
用xcode的可视化工具创建符号断点很简单，在Add symbolic breakpoint中填入符号名即可，这里给出objective-c的函数符号断点的写法：
```
-[MyViewController viewDidAppear:]
+[MyViewController sharedInstance]
```

## 10.查看内存

使用XCode的可视化工具来查看memory，要注意watch memory of "p" 和watch memory of "*p"的区别。
手动执行命令可以help x或者 help memory。


## 小结

lldb的用法很灵活多样，但是XCode的可视化调试工具覆盖面有限，一些高级用法仍需手动输入命令，甚至结合python脚本。
    

