---
title: iOS使用dumpdecrypted砸壳笔记
subtitle: iOSCNote
date: 2017-08-14 13:42:00
tags: iOS逆向
---

<!--# iOS使用dumpdecrypted砸壳笔记-->

## Cydia 安装 OpenSSH
## Cydia 安装 Cycript
## SSH 到手机
> ssh root@`手机IP地址`

初始密码:
>alpine

改密码:
> passwd root

查看进程:
> ps -e

查看指定进程:
> ps -e | grew `AppName`
	
	
## 执行 su mobile

如果砸壳出现 killed 9 错误, 请先执行:
> su mobile

## 附加到进程

使用 `Cycript` 工具, 附加到进程, 可以使用 `Cycript`下的 `JS-ObjectiveC` 语言进行调试.

执行命令:
> cycript -p `AppName`

例如:

```
// 弹出Alert窗口
[[[UIAlertView alloc]initWithTitle:@"Notice" message:@"debug" delegate:ni cancelButtonTitle:@"ok" otherButtonTitles:nil, nil] show]
// 获取对象
var delegate = UIApp.delegate
var window = delegate.window
var rootVC = window.rootViewController
// 获取沙盒目录
[[NSFileManager defaultManager] URLsForDirectory:NSDocumentDirectory inDomains:NSUserDomainMask][0]

```

## 拷贝 dumpdecrypted.dylib 到应用沙盒目录

> scp `dumpdecrypted.dylib路径` `沙盒路径`

## 开始砸壳

切换到沙盒目录下:
> cd `沙盒目录`

开始砸壳:
> DYLD_INSERT_LIBRARIES=dumpdecrypted.dylib `app二进制文件所在路径` mach-o decryption dumper

完成后在`沙盒目录`下产生文件 `AppName.decrypted`

> scp `AppName.decrypted` `YourPath`

查看二进制文件是否砸壳:
> otool -l `App.decrypted` | grep crypt

## class-dump 导出头文件

> class-dump -H spacewalk.decrypted -o output/

## 查看架构

> lipo -info XXXX.framework/XXXX


## 分离合并架构

首先从framework中分离出armv7 arm64，或者还有armv7s

> lipo XXXX.framework/XXXX -thin arm64 -output XXXX.framework/XXXX-arm64

> lipo XXXX.framework/XXXX -thin armv7 -output XXXX.framework/XXXX-armv7

然后合并分离出的两种架构

> lipo -create XXXX.framework/XXXX-armv7 XXXX.framework/XXXX-arm64 -output XXXX.framework/XXXX


## Cycript 使用

加载到进程:
> cycript -p xxxx

```
function printMethods(className) {
	var count = new new Type("I");
	var methods = class_copyMethodList(objc_getClass(className), count);
	var methodsArray = [];
	for(var i = 0; i < *count; i++) {
		var method = methods[i];
		methodsArray.push({selector:method_getName(method), implementation:method_getImplementation(method)});
	}
	free(methods);
	free(count);
	return methodsArray;
}
```