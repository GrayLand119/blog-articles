---
title: RunTime 学习笔记:基础概念及消息原理
date: 2016-03-07 19:00:00
tags:
- Runtime
- Objc
categories:
- iOS
---

<!--# RunTime 学习笔记:基础概念及消息原理-->

## 1 常见类型及方法

### SEL (方法选择器 | 映射到方法的C字符串)

objc_msgSend函数第二个参数类型为SEL，它是selector在Objc中的表示类型（Swift中是Selector类）。selector是方法选择器，可以理解为区分方法的 ID，而这个 ID 的数据结构是SEL:

> typedef struct objc_selector *SEL;

其实它就是个映射到方法的C字符串，你可以用 Objc 编译器命令@selector()或者 Runtime 系统的sel_registerName函数来获得一个SEL类型的方法选择器。

不同类中相同名字的方法所对应的方法选择器是相同的，即使方法名字相同而变量类型不同也会导致它们具有相同的方法选择器，于是 Objc 中方法命名有时会带上参数类型(NSNumber一堆抽象工厂方法拿走不谢)，Cocoa 中有好多长长的方法哦。

<!-- more -->

### id
我们常见的id，它是一个objc_object结构类型的指针。它的存在可以让我们实现类似于C++中泛型的一些操作。该类型的对象可以转换为任何一种对象，有点类似于C语言中void *指针类型的作用。

objc_msgSend第一个参数类型为id，大家对它都不陌生，它是一个指向类实例的指针：
> typedef struct objc_object *id;

### objc_object
objc_object是表示一个类的实例的结构体，它的定义如下(objc/objc.h)：
```objectivec
struct objc_object {
    Class isa  OBJC_ISA_AVAILABILITY;
};
typedef struct objc_object *id;
```

当我们向一个Objective-C对象发送消息时，运行时库会根据实例对象的**isa指针**找到这个实例对象所属的类。Runtime库会在类的方法列表及父类的方法列表中去寻找与消息对应的**selector**指向的方法。找到后即运行这个方法。

当创建一个特定类的实例对象时，分配的内存包含一个**objc_object**数据结构，然后是类的实例变量的数据。NSObject类的**alloc**和**allocWithZone:**方法使用函数**class_createInstance**来创建objc_object数据结构。

### Class
bjective-C类是由Class类型来表示的，它实际上是一个指向objc_class结构体的指针。它的定义如下：
> typedef struct objc_class *Class;

查看objc/runtime.h中objc_class结构体的定义如下：
```objc
struct objc_class {
    Class isa  OBJC_ISA_AVAILABILITY;
#if !__OBJC2__
    Class super_class                       OBJC2_UNAVAILABLE;  // 父类
    const char *name                        OBJC2_UNAVAILABLE;  // 类名
    long version                            OBJC2_UNAVAILABLE;  // 类的版本信息，默认为0
    long info                               OBJC2_UNAVAILABLE;  // 类信息，供运行期使用的一些位标识
    long instance_size                      OBJC2_UNAVAILABLE;  // 该类的实例变量大小
    struct objc_ivar_list *ivars            OBJC2_UNAVAILABLE;  // 该类的成员变量链表
    struct objc_method_list **methodLists   OBJC2_UNAVAILABLE;  // 方法定义的链表
    struct objc_cache *cache                OBJC2_UNAVAILABLE;  // 方法缓存
    struct objc_protocol_list *protocols    OBJC2_UNAVAILABLE;  // 协议链表
#endif
} OBJC2_UNAVAILABLE;
```

**cache**：用于缓存最近使用的方法。
一个接收者对象接收到一个消息时，它会根据isa指针去查找能够响应这个消息的对象。在实际使用中，这个对象只有一部分方法是常用的，很多方法其实很少用或者根本用不上。**这种情况下，如果每次消息来时，我们都是methodLists中遍历一遍，性能势必很差。**这时，cache就派上用场了。**在我们每次调用过一个方法后，这个方法就会被缓存到cache列表中，下次调用的时候runtime就会优先去cache中查找**，如果cache没有，才去methodLists中查找方法。这样，对于那些经常用到的方法的调用，但提高了调用的效率。

### objc_cache
这个字段是一个指向objc_cache结构体的指针，其定义如下：
```objc
struct objc_cache {
    unsigned int mask /* total = mask + 1 */                 OBJC2_UNAVAILABLE;
    unsigned int occupied                                    OBJC2_UNAVAILABLE;
    Method buckets[1]                                        OBJC2_UNAVAILABLE;
};
```
该结构体的字段描述如下：

* **mask**：一个整数，指定分配的缓存bucket的总数。在方法查找过程中，Objective-C runtime使用这个字段来确定开始线性查找数组的索引位置。指向方法selector的指针与该字段做一个AND位操作(index = (mask & selector))。这可以作为一个简单的hash散列算法。

* **occupied**：一个整数，指定实际占用的缓存bucket的总数。

* **buckets**：指向Method数据结构指针的数组。这个数组可能包含不超过mask+1个元素。需要注意的是，指针可能是NULL，表示这个缓存bucket没有被占用，另外被占用的bucket可能是不连续的。这个数组可能会随着时间而增长。

### (meta-class) 元类
**meta-class是一个类对象的类。**

当我们向一个对象发送消息时，runtime会在这个对象所属的这个类的方法列表中查找方法；而向一个类发送消息时，会在这个类的meta-class的方法列表中查找。

meta-class之所以重要，是因为它存储着一个类的所有类方法。每个类都会有一个单独的meta-class，因为每个类的类方法基本不可能完全相同。

再深入一下，meta-class也是一个类，也可以向它发送一个消息，那么它的isa又是指向什么呢？为了不让这种结构无限延伸下去，Objective-C的设计者让**所有的meta-class的isa指向基类的meta-class**，以此作为它们的所属类。即，任何NSObject继承体系下的meta-class都使用NSObject的meta-class作为自己的所属类，而**基类的meta-class的isa指针是指向它自己**。这样就形成了一个完美的闭环。



### Method
**Method是一种代表类中的某个方法的类型。**
> typedef struct objc_method *Method;
```objc
struct objc_method {
    SEL method_name                                          OBJC2_UNAVAILABLE;
    char *method_types                                       OBJC2_UNAVAILABLE;
    IMP method_imp                                           OBJC2_UNAVAILABLE;
}
```
- 方法名类型为SEL，前面提到过相同名字的方法即使在不同类中定义，它们的方法选择器也相同。
- 方法类型method_types是个char指针，其实存储着方法的参数类型和返回值类型。
- method_imp指向了方法的实现，本质上是一个函数指针。

### Ivar
**Ivar是一种代表类中实例变量的类型。**
> typedef struct objc_ivar *Ivar;
```objc
struct objc_ivar {
    char *ivar_name                                          OBJC2_UNAVAILABLE;
    char *ivar_type                                          OBJC2_UNAVAILABLE;
    int ivar_offset                                          OBJC2_UNAVAILABLE;
#ifdef __LP64__
    int space                                                OBJC2_UNAVAILABLE;
#endif
}
```
**成员变量操作函数，主要包含以下函数：**
```cpp
// 获取类中指定名称实例成员变量的信息, 它返回一个指向包含name指定的成员变量信息的objc_ivar结构体的指针(Ivar)。
Ivar class_getInstanceVariable ( Class cls, const char *name );

// 获取类成员变量的信息, 目前没有找到关于Objective-C中类变量的信息，一般认为Objective-C不支持类变量。注意，返回的列表不包含父类的成员变量和属性。
Ivar class_getClassVariable ( Class cls, const char *name );

// 添加成员变量
BOOL class_addIvar ( Class cls, const char *name, size_t size, uint8_t alignment, const char *types );

// 获取整个成员变量列表，它返回一个指向成员变量信息的数组，数组中每个元素是指向该成员变量信息的objc_ivar结构体的指针。这个数组不包含在父类中声明的变量。outCount指针返回数组的大小。需要注意的是，我们必须使用free()来释放这个数组。
Ivar * class_copyIvarList ( Class cls, unsigned int *outCount );
```
**Objective-C不支持往已存在的类中添加实例变量**，因此不管是系统库提供的提供的类，还是我们自定义的类，都无法动态添加成员变量。
但如果我们通过运行时来创建一个类的话，又应该如何给它添加成员变量呢？
这时我们就可以使用**class_addIvar**函数了。**不过需要注意的是，这个方法只能在objc_allocateClassPair函数与objc_registerClassPair之间调用。**
另外，这个类也不能是元类。成员变量的按字节最小对齐量是1<<alignment。这取决于ivar的类型和机器的架构。如果变量的类型是指针类型，则传递log2(sizeof(pointer_type))



**属性操作函数，主要包含以下函数：**
```cpp
// 获取指定的属性
objc_property_t class_getProperty ( Class cls, const char *name );

// 获取属性列表
objc_property_t * class_copyPropertyList ( Class cls, unsigned int *outCount );

// 为类添加属性
BOOL class_addProperty ( Class cls, const char *name, const objc_property_attribute_t *attributes, unsigned int attributeCount );

// 替换类的属性
void class_replaceProperty ( Class cls, const char *name, const objc_property_attribute_t *attributes, unsigned int attributeCount );
```
这一种方法也是针对ivars来操作，不过只操作那些是属性的值。

**在MAC OS X系统中，我们可以使用垃圾回收器。runtime提供了几个函数来确定一个对象的内存区域是否可以被垃圾回收器扫描，以处理strong/weak引用。这几个函数定义如下：**
```cpp
const uint8_t * class_getIvarLayout ( Class cls );
void class_setIvarLayout ( Class cls, const uint8_t *layout );
const uint8_t * class_getWeakIvarLayout ( Class cls );
void class_setWeakIvarLayout ( Class cls, const uint8_t *layout );
```

但通常情况下，我们不需要去主动调用这些方法；在调用objc_registerClassPair时，会生成合理的布局。在此不详细介绍这些函数。

### 方法(methodLists)
方法操作主要有以下函数：
```cpp
/* 添加方法
与成员变量不同的是，我们可以为类动态添加方法，不管这个类是否已存在。
另外，参数types是一个描述传递给方法的参数类型的字符数组，这就涉及到类型编码，我们将在后面介绍。
class_addMethod的实现会覆盖父类的方法实现，但不会取代本类中已存在的实现，如果本类中包含一个同名的实现，则函数会返回NO。
如果要修改已存在实现，可以使用method_setImplementation。
一个Objective-C方法是一个简单的C函数，它至少包含两个参数—self和_cmd。
所以，我们的实现函数(IMP参数指向的函数)至少需要两个参数，如下所示：
*/
BOOL class_addMethod ( Class cls, SEL name, IMP imp, const char *types );
void myMethodIMP(id self, SEL _cmd){
    // implementation ....
}


/* 获取实例方法
class_getInstanceMethod、class_getClassMethod函数，与class_copyMethodList不同的是，这两个函数都会去搜索父类的实现。
*/
Method class_getInstanceMethod ( Class cls, SEL name );

/*
获取类方法
class_copyMethodList函数，返回包含所有实例方法的数组，如果需要获取类方法，则可以使用class_copyMethodList(object_getClass(cls), &count)(一个类的实例方法是定义在元类里面)。该列表不包含父类实现的方法。outCount参数返回方法的个数。在获取到列表后，我们需要使用free()方法来释放它。
*/ 
Method class_getClassMethod ( Class cls, SEL name );

// 获取所有方法的数组
Method * class_copyMethodList ( Class cls, unsigned int *outCount );

/* 
替代方法的实现
该函数的行为可以分为两种：如果类中不存在name指定的方法，则类似于class_addMethod函数一样会添加方法；如果类中已存在name指定的方法，则类似于method_setImplementation一样替代原方法的实现。
*/
IMP class_replaceMethod ( Class cls, SEL name, IMP imp, const char *types );

/*
返回方法的具体实现
该函数在向类实例发送消息时会被调用，并返回一个指向方法实现函数的指针。这个函数会比method_getImplementation(class_getInstanceMethod(cls, name))更快。返回的函数指针可能是一个指向runtime内部的函数，而不一定是方法的实际实现。例如，如果类实例无法响应selector，则返回的函数指针将是运行时消息转发机制的一部分。
*/
IMP class_getMethodImplementation ( Class cls, SEL name );
IMP class_getMethodImplementation_stret ( Class cls, SEL name );

/*
类实例是否响应指定的selector
我们通常使用NSObject类的respondsToSelector:或instancesRespondToSelector:方法来达到相同目的。
 */
BOOL class_respondsToSelector ( Class cls, SEL sel );
```

### 协议(objc_protocol_list)
协议相关的操作包含以下函数：
```cpp
// 添加协议
BOOL class_addProtocol ( Class cls, Protocol *protocol );

// 返回类是否实现指定的协议
// class_conformsToProtocol函数可以使用NSObject类的conformsToProtocol:方法来替代。
BOOL class_conformsToProtocol ( Class cls, Protocol *protocol );

// 返回类实现的协议列表
// class_copyProtocolList函数返回的是一个数组，在使用后我们需要使用free()手动释放。
Protocol * class_copyProtocolList ( Class cls, unsigned int *outCount );
```
### 版本(version)
版本相关的操作包含以下函数：
```cpp
// 获取版本号
int class_getVersion ( Class cls );
// 设置版本号
void class_setVersion ( Class cls, int version );
```
### 其它
runtime还提供了两个函数来供CoreFoundation的tool-free bridging使用，即：
```cpp
Class objc_getFutureClass ( const char *name );

void objc_setFutureClass ( Class cls, const char *name );
```
通常我们不直接使用这两个函数。


# 2 消息
**Objc 中发送消息是用中括号（[]）把接收者和消息括起来，而直到运行时才会把消息与方法实现绑定。**



### objc_msgSend函数
消息发送步骤：
1. **检测这个 selector 是不是要忽略的。**比如 Mac OS X 开发，有了垃圾回收就不理会 retain,release 这些函数了。
2. **检测这个 target 是不是 nil 对象。**ObjC 的特性是允许对一个 nil 对象执行任何一个方法不会 Crash，因为会被忽略掉。
3. 如果上面两个都过了，那就**开始查找这个类的 IMP**，先从 cache 里面找，完了找得到就跳到对应的函数去执行。
4. 如果 cache 找不到就找一下方法分发表。
5. 如果分发表找不到就到超类的分发表去找，一直找，直到找到NSObject类为止。
6. 如果还找不到就要开始进入动态方法解析了，后面会提到。

这里说的分发表其实就是Class中的方法列表，它将方法选择器和方法实现地质联系起来。(selector...address)


其实编译器会根据情况在objc_msgSend, objc_msgSend_stret, objc_msgSendSuper, 或objc_msgSendSuper_stret四个方法中选择一个来调用。如果消息是传递给超类，那么会调用名字带有”Super”的函数；如果消息返回值是数据结构而不是简单值时，那么会调用名字带有”stret”的函数。

### 方法中的隐藏参数
我们经常在方法中使用self关键字来引用实例本身，但从没有想过为什么self就能取到调用当前方法的对象吧。其实self的内容是在方法运行时被偷偷的动态传入的。

当objc_msgSend找到方法对应的实现时，它将直接调用该方法实现，并将消息中所有的参数都传递给方法实现,同时,它还将**传递两个隐藏的参数**:
- 接收消息的对象（也就是self指向的内容）
- 方法选择器（_cmd指向的内容）

之所以说它们是隐藏的是因为在源代码方法的定义中并没有声明这两个参数。它们是在代码被编译时被插入实现中的。尽管这些参数没有被明确声明，在源代码中我们仍然可以引用它们。

在下面的例子中，self引用了接收者对象，而_cmd引用了方法本身的选择器：

```objc
- strange
{
    id  target = getTheReceiver();
    SEL method = getTheMethod();
 
    if ( target == self || method == _cmd )
        return nil;
    return [target performSelector:method];
}
```

### 获取方法地址

在IMP那节提到过可以避开消息绑定而直接获取方法的地址并调用方法。这种做法很少用，除非是需要持续大量重复调用某方法的极端情况，避开消息发送泛滥而直接调用该方法会更高效。

NSObject类中有个methodForSelector:实例方法，你可以用它来获取某个方法选择器对应的IMP，举个栗子：

```objectivec
void (*setter)(id, SEL, BOOL);
int i;
 
setter = (void (*)(id, SEL, BOOL))[target
    methodForSelector:@selector(setFilled:)];
for ( i = 0 ; i < 1000 ; i++ )
    setter(targetList[i], @selector(setFilled:), YES);
```

**当方法被当做函数调用时，上节提到的两个隐藏参数就需要我们明确给出了。**上面的例子调用了1000次函数，你可以试试直接给target发送1000次setFilled:消息会花多久。
    
PS：methodForSelector:方法是由 Cocoa 的 Runtime 系统提供的，而不是 Objc 自身的特性。


### 动态方法解析(动态绑定)
你可以动态地提供一个方法的实现。例如我们可以用@dynamic关键字在类的实现文件中修饰一个属性：
> @dynamic propertyName;

这表明我们会为这个属性动态提供存取方法，也就是说编译器不会再默认为我们生成**setPropertyName:**和**propertyName**方法，而需要我们动态提供。
我们可以通过分别重载**resolveInstanceMethod:**和**resolveClassMethod:**方法分别添加实例方法实现和类方法实现。
因为当 **Runtime 系统在Cache和方法分发表中（包括超类）找不到要执行的方法时，Runtime会调用resolveInstanceMethod:或resolveClassMethod:来给程序员一次动态添加方法实现的机会。**

我们需要用class_addMethod函数完成向特定类添加特定方法实现的操作：
```objc
void dynamicMethodIMP(id self, SEL _cmd) {
// implementation ....
}
@implementation MyClass
+ (BOOL)resolveInstanceMethod:(SEL)aSEL
{
    if (aSEL == @selector(resolveThisMethodDynamically)) {
          class_addMethod([self class], aSEL, (IMP) dynamicMethodIMP, "v@:");
          return YES;
    }
    return [super resolveInstanceMethod:aSEL];
}
@end
```
面的例子为resolveThisMethodDynamically方法添加了实现内容，也就是dynamicMethodIMP方法中的代码。其中 “v@:” 表示返回值和参数，这个符号涉及 Type Encoding


**当然也可以在任意需要的地方调用class_addMethod或者method_setImplementation（前者添加实现，后者替换实现），来完成动态绑定的需求。**

PS：**动态方法解析会在消息转发机制浸入前执行。**
如果 respondsToSelector: 或instancesRespondToSelector:方法被执行，动态方法解析器将会被首先给予一个提供该方法选择器对应的IMP的机会。**如果你想让该方法选择器被传送到转发机制，那么就让resolveInstanceMethod:返回NO。**

# 3 消息转发

### 重定向
在消息转发机制执行前，Runtime 系统会再给我们一次偷梁换柱的机会，
即通过重载**- (id)forwardingTargetForSelector:(SEL)aSelector**方法替换消息的接受者为其他对象：
```objc
- (id)forwardingTargetForSelector:(SEL)aSelector
{
    if(aSelector == @selector(mysteriousMethod:)){
        return alternateObject;
    }
    return [super forwardingTargetForSelector:aSelector];
}
```
毕竟消息转发要耗费更多时间，抓住这次机会将消息重定向给别人是个不错的选择，**不过千万别返回self，因为那样会死循环。**

### 转发
**当动态方法解析不作处理返回NO时，消息转发机制会被触发。**
在这时forwardInvocation:方法会被执行，我们可以重写这个方法来定义我们的转发逻辑：
```objc
- (void)forwardInvocation:(NSInvocation *)anInvocation
{
    if ([someOtherObject respondsToSelector:
            [anInvocation selector]])
        [anInvocation invokeWithTarget:someOtherObject];
    else
        [super forwardInvocation:anInvocation];
}
```
该消息的唯一参数是个NSInvocation类型的对象——该对象封装了原始的消息和消息的参数。
我们可以实现forwardInvocation:方法来对不能处理的消息做一些默认的处理，也可以将消息转发给其他对象来处理，而不抛出错误。

这里需要注意的是参数anInvocation是从哪的来的呢？
其实在forwardInvocation:消息发送前，Runtime系统会向对象发送methodSignatureForSelector:消息，并取到返回的方法签名用于生成NSInvocation对象。
所以我们在**重写forwardInvocation:的同时也要重写methodSignatureForSelector:方法，否则会抛异常**。

当一个对象由于没有相应的方法实现而无法响应某消息时，运行时系统将通过forwardInvocation:消息通知该对象。每个对象都从NSObject类中继承了forwardInvocation:方法。然而，NSObject中的方法实现只是简单地调用了doesNotRecognizeSelector:。通过实现我们自己的forwardInvocation:方法，我们可以在该方法实现中将消息转发给其它对象。

forwardInvocation:方法就像一个不能识别的消息的分发中心，将这些消息转发给不同接收对象。或者它也可以象一个运输站将所有的消息都发送给同一个接收对象。它可以将一个消息翻译成另外一个消息，或者简单的”吃掉“某些消息，因此没有响应也没有错误。forwardInvocation:方法也可以对不同的消息提供同样的响应，这一切都取决于方法的具体实现。该方法所提供是将不同的对象链接到消息链的能力。

注意： **forwardInvocation:方法只有在消息接收对象中无法正常响应消息时才会被调用。** 所以，如果我们希望一个对象将negotiate消息转发给其它对象，则这个对象不能有negotiate方法。否则，forwardInvocation:将不可能会被调用。

### 转发和多继承

转发和继承相似，可以用于为Objc编程添加一些多继承的效果。就像下图那样，一个对象把消息转发出去，就好似它把另一个对象中的方法借过来或是“继承”过来一样。

这使得不同继承体系分支下的两个类可以“继承”对方的方法，在上图中Warrior和Diplomat没有继承关系，但是Warrior将negotiate消息转发给了Diplomat后，就好似Diplomat是Warrior的超类一样。

**消息转发弥补了 Objc 不支持多继承的性质，也避免了因为多继承导致单个类变得臃肿复杂。**它将问题分解得很细，只针对想要借鉴的方法才转发，而且转发机制是透明的。

### 替代者对象(Surrogate Objects)

转发不仅能模拟多继承，也能使轻量级对象代表重量级对象。弱小的女人背后是强大的男人，毕竟女人遇到难题都把它们转发给男人来做了。[官方文档](https://developer.apple.com/library/mac/documentation/Cocoa/Conceptual/ObjCRuntimeGuide/Articles/ocrtForwarding.html#//apple_ref/doc/uid/TP40008048-CH105-SW11)

### 转发与继承
尽管转发很像继承，但是NSObject类不会将两者混淆。
像respondsToSelector: 和 isKindOfClass:这类方法只会考虑继承体系，不会考虑转发链。
比如上图中一个Warrior对象如果被问到是否能响应negotiate消息：
> if ( [aWarrior respondsToSelector:@selector(negotiate)] )
	> ....

结果是NO，尽管它能够接受negotiate消息而不报错，因为它靠转发消息给Diplomat类来响应消息。

如果你为了某些意图偏要“弄虚作假”让别人以为Warrior继承到了Diplomat的negotiate方法，你得重新实现 respondsToSelector: 和 isKindOfClass:来加入你的转发算法：
```objc
- (BOOL)respondsToSelector:(SEL)aSelector
{
    if ( [super respondsToSelector:aSelector] )
        return YES;
    else {
        
/* Here, test whether the aSelector message can     *
         
* be forwarded to another object and whether that  *
         
* object can respond to it. Return YES if it can.  */
    }
    return NO;
}
```
除了respondsToSelector: 和 isKindOfClass:之外，instancesRespondToSelector:中也应该写一份转发算法。
如果使用了协议，conformsToProtocol:同样也要加入到这一行列中。
类似地，如果一个对象转发它接受的任何远程消息，它得给出一个methodSignatureForSelector:来返回准确的方法描述，这个方法会最终响应被转发的消息。
比如一个对象能给它的替代者对象转发消息，它需要像下面这样实现methodSignatureForSelector:
```objc
- (NSMethodSignature*)methodSignatureForSelector:(SEL)selector
{
    NSMethodSignature* signature = [super methodSignatureForSelector:selector];
    if (!signature) {
       signature = [surrogate methodSignatureForSelector:selector];
    }
    return signature;
}
```

### 健壮的实例变量(Non Fragile ivars)

在 Runtime 的现行版本中，最大的特点就是健壮的实例变量。当一个类被编译时，实例变量的布局也就形成了，它表明访问类的实例变量的位置。从对象头部开始，实例变量依次根据自己所占空间而产生位移：
![img](http://ww4.sinaimg.cn/mw690/7cc829d3gw1em5rt64r9vj20cc039t8u.jpg)
上图左边是NSObject类的实例变量布局，右边是我们写的类的布局，也就是在超类后面加上我们自己类的实例变量，看起来不错。但试想如果那天苹果更新了NSObject类，发布新版本的系统的话，那就悲剧了：
![img](http://ww2.sinaimg.cn/mw690/7cc829d3gw1em5rv1oqbjj20cf03cq38.jpg)
我们自定义的类被划了两道线，那是因为那块区域跟超类重叠了。唯有苹果将超类改为以前的布局才能拯救我们，但这样也导致它们不能再拓展它们的框架了，因为成员变量布局被死死地固定了。在脆弱的实例变量(Fragile ivars) 环境下我们需要重新编译继承自 Apple 的类来恢复兼容性。那么在健壮的实例变量下回发生什么呢？
![img](http://ww1.sinaimg.cn/mw690/7cc829d3gw1em5rv25yp8j20ci04rjru.jpg)
在健壮的实例变量下编译器生成的实例变量布局跟以前一样，但是当 runtime 系统检测到与超类有部分重叠时它会调整你新添加的实例变量的位移，那样你在子类中新添加的成员就被保护起来了。

**需要注意的是在健壮的实例变量下，不要使用sizeof(SomeClass)，而是用class_getInstanceSize([SomeClass class])代替；**
**也不要使用offsetof(SomeClass, SomeIvar)，而要用ivar_getOffset(class_getInstanceVariable([SomeClass class], "SomeIvar"))来代替。**

### Objective-C Associated Objects
在 OS X 10.6 之后，Runtime系统让Objc支持向对象动态添加变量。涉及到的函数有以下三个：
```cpp
void objc_setAssociatedObject ( id object, const void *key, id value, objc_AssociationPolicy policy );
id objc_getAssociatedObject ( id object, const void *key );
void objc_removeAssociatedObjects ( id object );
```
这些方法以键值对的形式动态地向对象添加、获取或删除关联值。其中关联政策是一组枚举常量：
```cpp
enum {
   OBJC_ASSOCIATION_ASSIGN  = 0,
   OBJC_ASSOCIATION_RETAIN_NONATOMIC  = 1,
   OBJC_ASSOCIATION_COPY_NONATOMIC  = 3,
   OBJC_ASSOCIATION_RETAIN  = 01401,
   OBJC_ASSOCIATION_COPY  = 01403
};
```
这些常量对应着引用关联值的政策，也就是 Objc 内存管理的引用计数机制。

