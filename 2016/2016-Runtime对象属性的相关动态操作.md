---
title: iOS Runtime 对象属性的相关动态操作笔记
subtitle: OCRTNote
date: 2016-09-04 00:00:00
tags: 
- iOS
- Runtime
---

<!--# iOS Runtime 对象属性的相关动态操作笔记-->

## 动态获取属性

动态获取属性变量名, 类型, atomic/nonatomic, strong/weak/copy/retain/assgn, read
相关函数:

* objc_getClass or [self class] 获取类
* class_copyIvarList 获取变量列表
* ivar_getName 获取变量名称
* ivar_getTypeEncoding 获取变量相关类型属性, 通过 `Type encoding` 表示. [Type Coding](https://developer.apple.com/library/content/documentation/Cocoa/Conceptual/ObjCRuntimeGuide/Articles/ocrtTypeEncodings.html#//apple_ref/doc/uid/TP40008048-CH100)
* class_getProperty
* property_getName
* property_getAttributes

```cpp
/** 
 * Describes the instance variables declared by a class.
 * 
 * @param cls The class to inspect.
 * @param outCount On return, contains the length of the returned array. 
 *  If outCount is NULL, the length is not returned.
 * 
 * @return An array of pointers of type Ivar describing the instance variables declared by the class. 
 *  Any instance variables declared by superclasses are not included. The array contains *outCount 
 *  pointers followed by a NULL terminator. You must free the array with free().
 * 
 *  If the class declares no instance variables, or cls is Nil, NULL is returned and *outCount is 0.
 */
OBJC_EXPORT Ivar *class_copyIvarList(Class cls, unsigned int *outCount) 
     OBJC_AVAILABLE(10.5, 2.0, 9.0, 1.0);
```

通过 `class_copyIvarList` 函数获取 `Ivar` 变量. 该函数返回一个 `Ivar` 数组.

需要注意的是, 该函数只显示当前类的变量, 父类的不显示. 如果当前类没有定义属性变量, 或者输入的 `cls` 为 Nil, 返回的 `*outcount` 值为0.

若要获取包含父类的所有成员变量, 可以参考 `MJExtension` 的实现, 代码在 `NSObject+MJMember.h` 文件中.

```objc
/**
 *  遍历所有的成员变量
 */
- (void)enumerateIvarsWithBlock:(MJIvarsBlock)block;
```

回到主题, 获取到 `Ivar` 之后, 通过 `ivar_getName` 可以获取到变量的名称, 使用自动合成属性时变量名前会加入下划线 `_`.

使用 `ivar_getTypeEncoding` 获取变量的类型, NSFoundation对象返回的字符串是其类型名, 如 "NSNumber" 类型的变量, 则返回 `@"NSNumber"`.

其他返回类型使用 [Type Coding](https://developer.apple.com/library/content/documentation/Cocoa/Conceptual/ObjCRuntimeGuide/Articles/ocrtTypeEncodings.html#//apple_ref/doc/uid/TP40008048-CH100)
.

| Code | Meaning |
| :---: | :--- |
| c | A char |
|i |An int
|s |A short
|l|A long |l is treated as a 32-bit quantity on 64-bit programs.
|q |A long long
|C |An unsigned char
|I |An unsigned int
|S |An unsigned short
|L |An unsigned long
|Q |An unsigned long long
|f |A float
|d |A double
|B |A C++ bool or a C99 _Bool
|v |A void
|* |A character string (char *)
|@ |An object (whether statically typed or typed id)
|# |A class object (Class)
|: |A method selector (SEL)
|[array type] |An array
|{name=type...} |A structure
|(name=type...) |A union
|bnum |A bit field of num bits
|^type |A pointer to type
|? |An unknown type (among other things, this code is used for function pointers)

