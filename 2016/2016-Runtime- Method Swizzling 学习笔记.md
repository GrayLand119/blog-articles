---
title: Runtime:Method Swizzling 学习笔记
date: 2016-03-08 19:49:10
tags:
- Runtime
- Objc
categories:
- iOS
---

<!--# Runtime: Method Swizzling 学习笔记-->

## 简述
是改变一个selector实际实现的技术，可以在运行时修改selector对应的函数来修改Method的实现。前面的消息转发很强大，但是需要能够修改对应类的源码，但是对于有些类无法修改其源码时又要更改其方法实现时可以使用Method Swizzling，通过重新映射方法来达到目的，但是跟消息转发比起来调试会困难。

## 应用场景
假设我们想跟踪在一个iOS应用中每个视图控制器展现给用户的次数, 我们可以给每个视图控制器对应的viewWillAppear:实现方法中增加相应的跟踪代码，但是这样做会产生大量重复的代码。
子类化可能是另一个选择，但要求你将UIViewController、 UITableViewController、 UINavigationController 以及所有其他视图控制器类都子类化，这也会导致代码重复。

<!-- more -->


```objc
#import <objc/runtime.h>

@implementation UIViewController (Tracking)

+ (void)load {
     static dispatch_once_t onceToken;
     dispatch_once(&onceToken, ^{
          Class class = [self class];
          // When swizzling a class method, use the following:
          // Class class = object_getClass((id)self);

          //通过method swizzling修改了UIViewController的@selector(viewWillAppear:)的指针使其指向了自定义的xxx_viewWillAppear
          SEL originalSelector = @selector(viewWillAppear:);
          SEL swizzledSelector = @selector(xxx_viewWillAppear:);

          Method originalMethod = class_getInstanceMethod(class, originalSelector);
          Method swizzledMethod = class_getInstanceMethod(class, swizzledSelector);

          BOOL didAddMethod = class_addMethod(class,
               originalSelector,
               method_getImplementation(swizzledMethod),
               method_getTypeEncoding(swizzledMethod));

          //如果类中不存在要替换的方法，就先用class_addMethod和class_replaceMethod函数添加和替换两个方法实现。但如果已经有了要替换的方法，就调用method_exchangeImplementations函数交换两个方法的Implementation。
          if (didAddMethod) {
               class_replaceMethod(class,
                    swizzledSelector,
                    method_getImplementation(originalMethod),
               method_getTypeEncoding(originalMethod));
          } else {
               method_exchangeImplementations(originalMethod, swizzledMethod);
          }
     });
}

#pragma mark - Method Swizzling
- (void)xxx_viewWillAppear:(BOOL)animated {
     [self xxx_viewWillAppear:animated];
     NSLog(@"viewWillAppear: %@", self);
}

@end
```
method_exchangeImplementations做的事情和如下代码是一样的:

```cpp
IMP imp1 = method_getImplementation(m1);
IMP imp2 = method_getImplementation(m2);
method_setImplementation(m1, imp2);
method_setImplementation(m2, imp1);
```

另一种Method Swizzling的实现

```objc
- (void)replacementReceiveMessage:(const struct BInstantMessage *)arg1 {
     NSLog(@"arg1 is %@", arg1);
     [self replacementReceiveMessage:arg1];
}
+ (void)load {
     SEL originalSelector = @selector(ReceiveMessage:);
     SEL overrideSelector = @selector(replacementReceiveMessage:);
     Method originalMethod = class_getInstanceMethod(self, originalSelector);
     Method overrideMethod = class_getInstanceMethod(self, overrideSelector);
     if (class_addMethod(self, originalSelector, method_getImplementation(overrideMethod), method_getTypeEncoding(overrideMethod))) {
          class_replaceMethod(self, overrideSelector, method_getImplementation(originalMethod), method_getTypeEncoding(originalMethod));
     } else {
          method_exchangeImplementations(originalMethod, overrideMethod);
     }
}
```

这里有几个关于Method Swizzling的资源可以参考

- [How do I implement method swizzling?](http://stackoverflow.com/questions/5371601/how-do-i-implement-method-swizzling)
- [Method Swizzling](http://nshipster.com/method-swizzling/)
- [What are the Dangers of Method Swizzling in Objective C?](http://stackoverflow.com/questions/5339276/what-are-the-dangers-of-method-swizzling-in-objective-c)
- [JRSwizzle](https://github.com/rentzsch/jrswizzle)

## 使用method swizzling需要注意的问题
- **Swizzling应该总在+load中执行：**Objective-C在运行时会自动调用类的两个方法+load和+initialize。+load会在类初始加载时调用，和+initialize比较+load能保证在类的初始化过程中被加载.
通常你替换一个方法的实现，是希望它在整个程序的生命周期里有效的。也就是说，你会把 method swizzling 修改方法实现的操作放在一个加号方法 +(void)load里，并在应用程序的一开始就调用执行。你将不会碰到并发问题。假如你在 +(void)initialize初始化方法中进行swizzle，那么……rumtime可能死于一个诡异的状态。
- **Swizzling应该总是在dispatch_once中执行：**swizzling会改变全局状态，所以在运行时采取一些预防措施，使用dispatch_once就能够确保代码不管有多少线程都只被执行一次。这将成为method swizzling的最佳实践。
- **Selector，Method和Implementation：**这几个之间关系可以这样理解，一个类维护一个运行时可接收的消息分发表，分发表中每个入口是一个Method，其中key是一个特定的名称，及SEL，与其对应的实现是IMP即指向底层C函数的指针。
- **Changes behavior of un-owned code:**这是swizzling的一个问题。我们的目标是改变某些代码。swizzling方法是一件灰常灰常重要的事，当你不只是对一个NSButton类的实例进行了修改，而是程序中所有的NSButton实例。因此在swizzling时应该多加小心，但也不用总是去刻意避免。
想象一下，如果你重写了一个类的方法，而且没有调用父类的这个方法，这可能会引起问题。大多数情况下，父类方法期望会被调用（至少文档是这样说的）。如果你在swizzling实现中也这样做了，这会避免大部分问题。还是调用原始实现吧，如若不然，你会费很大力气去考虑代码的安全问题。
- **命名冲突:**命名冲突贯穿整个Cocoa的问题. 我们常常在类名和类别方法名前加上前缀。不幸的是，命名冲突仍是个折磨。但是swizzling其实也不必过多考虑这个问题。我们只需要在原始方法命名前做小小的改动来命名就好，比如通常我们这样命名：
 **[self swizzle:@selector(setFrame:) with:@selector(my_setFrame:)];** 
 但是如果my_setFrame: 在别处被定义了会引发不可预期的错误
 这个问题不仅仅存在于swizzling， 用函数指针代替，这样避免了selector的命名冲突:

```
typedef IMP *IMPPointer;  

BOOL class_swizzleMethodAndStore(Class class, SEL original, IMP replacement, IMPPointer store) {  
    IMP imp = NULL;  
    Method method = class_getInstanceMethod(class, original);  
    if (method) {  
        const char *type = method_getTypeEncoding(method);  
        imp = class_replaceMethod(class, original, replacement, type);  
        if (!imp) {  
            imp = method_getImplementation(method);  
        }  
    }  
    if (imp && store) { *store = imp; }  
    return (imp != NULL);  
}  
  
@implementation NSObject (FRRuntimeAdditions)  
+ (BOOL)swizzle:(SEL)original with:(IMP)replacement store:(IMPPointer)store {  
    return class_swizzleMethodAndStore(self, original, replacement, store);  
}  
@end  

@implementation NSView (MyViewAdditions)  

static void MySetFrame(id self, SEL _cmd, NSRect frame);  
static void (*SetFrameIMP)(id self, SEL _cmd, NSRect frame);  
 
static void MySetFrame(id self, SEL _cmd, NSRect frame) {  
    // do custom work  
    SetFrameIMP(self, _cmd, frame);  
}  
  
  
+ (void)load {  
    [self swizzle:@selector(setFrame:) with:(IMP)MySetFrame store:(IMP *)&SetFrameIMP];  
}  

@end 

```

- **Swizzling changes the method's arguments: **  
例如: 直接调用my_setFrame:  **[self my_setFrame:frame];**  ，
runtime做的是 **objc_msgSend(self, @selector(my_setFrame:), frame);** 
runtime去寻找my_setFrame:的方法实现, _cmd参数为 my_setFrame: ，但是事实上runtime找到的方法实现是原始的 setFrame: 的。
一个简单的解决办法：使用上面介绍的swizzling定义。

- **The order of swizzles matters:**
多个swizzle方法的执行顺序也需要注意。假设 setFrame: 只定义在NSView中，想像一下按照下面的顺序执行：

```
[NSButton swizzle:@selector(setFrame:) with:@selector(my_buttonSetFrame:)];  
[NSControl swizzle:@selector(setFrame:) with:@selector(my_controlSetFrame:)];  
[NSView swizzle:@selector(setFrame:) with:@selector(my_viewSetFrame:)];  
```
多个有继承关系的类的对象swizzle时，先从父对象开始。 这样才能保证子类方法拿到父类中的被swizzle的实现。在+(void)load中swizzle不会出错，就是因为load类方法会默认从父类开始调用。
```
[NSView swizzle:@selector(setFrame:) with:@selector(my_viewSetFrame:)];  
[NSControl swizzle:@selector(setFrame:) with:@selector(my_controlSetFrame:)];  
[NSButton swizzle:@selector(setFrame:) with:@selector(my_buttonSetFrame:)];  
```

