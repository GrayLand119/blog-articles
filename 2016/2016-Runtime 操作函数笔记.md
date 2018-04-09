---
title: Runtime 操作函数笔记
date: 2016-03-08 21:49:10
tags:
- Runtime
- Objc
categories:
- iOS
---

<!--# Runtime 操作函数笔记-->

## 1. 类相关操作函数
### 1.1 name

```cpp
// 获取类的类名
const char * class_getName ( Class cls ); 
```
	
### 1.2 super_class和meta-class

```cpp
// 获取类的父类
Class class_getSuperclass ( Class cls );

// 判断给定的Class是否是一个meta class
BOOL class_isMetaClass ( Class cls );
```

### 1.3 instance_size

```cpp
// 获取实例大小
size_t class_getInstanceSize ( Class cls );
```

<!-- more -->

### 1.4 成员变量(ivars)及属性

```cpp
//成员变量操作函数
// 获取类中指定名称实例成员变量的信息
Ivar class_getInstanceVariable ( Class cls, const char *name );

// 获取类成员变量的信息
Ivar class_getClassVariable ( Class cls, const char *name );

// 添加成员变量
BOOL class_addIvar ( Class cls, const char *name, size_t size, uint8_t alignment, const char *types ); //这个只能够向在runtime时创建的类添加成员变量

// 获取整个成员变量列表
Ivar * class_copyIvarList ( Class cls, unsigned int *outCount ); //必须使用free()来释放这个数组

//属性操作函数
// 获取类中指定名称实例成员变量的信息
Ivar class_getInstanceVariable ( Class cls, const char *name );

// 获取类成员变量的信息
Ivar class_getClassVariable ( Class cls, const char *name );

// 添加成员变量
BOOL class_addIvar ( Class cls, const char *name, size_t size, uint8_t alignment, const char *types );

// 获取整个成员变量列表
Ivar * class_copyIvarList ( Class cls, unsigned int *outCount );
```


### 1.5 methodLists

```cpp
// 添加方法
BOOL class_addMethod ( Class cls, SEL name, IMP imp, const char *types ); //和成员变量不同的是可以为类动态添加方法。如果有同名会返回NO，修改的话需要使用method_setImplementation

// 获取实例方法
Method class_getInstanceMethod ( Class cls, SEL name );

// 获取类方法
Method class_getClassMethod ( Class cls, SEL name );

// 获取所有方法的数组
Method * class_copyMethodList ( Class cls, unsigned int *outCount );

// 替代方法的实现
IMP class_replaceMethod ( Class cls, SEL name, IMP imp, const char *types );

// 返回方法的具体实现
IMP class_getMethodImplementation ( Class cls, SEL name );
IMP class_getMethodImplementation_stret ( Class cls, SEL name );

// 类实例是否响应指定的selector
BOOL class_respondsToSelector ( Class cls, SEL sel );
```

### 1.6 objc_protocol_list
```cpp
// 添加协议
BOOL class_addProtocol ( Class cls, Protocol *protocol );

// 返回类是否实现指定的协议
BOOL class_conformsToProtocol ( Class cls, Protocol *protocol );

// 返回类实现的协议列表
Protocol * class_copyProtocolList ( Class cls, unsigned int *outCount );
```

### 1.7 version
```cpp
// 获取版本号
int class_getVersion ( Class cls );

// 设置版本号
void class_setVersion ( Class cls, int version );
```

## 2. 动态创建类和对象相关函数
### 2.1 动态创建类
```cpp
// 创建一个新类和元类
// 如果创建的是root class，则superclass为Nil。extraBytes通常为0
Class objc_allocateClassPair ( Class superclass, const char *name, size_t extraBytes ); 

// 销毁一个类及其相关联的类
// 在运行中还存在或存在子类实例，就不能够调用这个。
void objc_disposeClassPair ( Class cls ); 

// 在应用中注册由objc_allocateClassPair创建的类
// 创建了新类后，然后使用class_addMethod，class_addIvar函数为新类添加方法，实例变量和属性后再调用这个来注册类，再之后就能够用了。
void objc_registerClassPair ( Class cls ); 
```

### 2.2 动态创建对象
```cpp
// 创建类实例
// 会在heap里给类分配内存。这个方法和+alloc方法类似。
id class_createInstance ( Class cls, size_t extraBytes ); 

// 在指定位置创建类实例
id objc_constructInstance ( Class cls, void *bytes ); 

// 销毁类实例
// 不会释放移除任何相关引用
void * objc_destructInstance ( id obj ); 
```

##3. 实例操作函数
### 3.1 整个对象操作的函数
```cpp
// 返回指定对象的一份拷贝
id object_copy ( id obj, size_t size );
// 释放指定对象占用的内存
id object_dispose ( id obj );
```

**应用场景**

```cpp
//把a转换成占用更多空间的子类b
NSObject *a = [[NSObject alloc] init];
id newB = object_copy(a, class_getInstanceSize(MyClass.class));
object_setClass(newB, MyClass.class);
object_dispose(a);
```

### 3.2 对象实例变量进行操作的函数
```cpp
// 修改类实例的实例变量的值
Ivar object_setInstanceVariable ( id obj, const char *name, void *value );
// 获取对象实例变量的值
Ivar object_getInstanceVariable ( id obj, const char *name, void **outValue );
// 返回指向给定对象分配的任何额外字节的指针
void * object_getIndexedIvars ( id obj );
// 返回对象中实例变量的值
id object_getIvar ( id obj, Ivar ivar );
// 设置对象中实例变量的值
void object_setIvar ( id obj, Ivar ivar, id value );
```

### 3.3 对对象类操作
```cpp
// 返回给定对象的类名
const char * object_getClassName ( id obj );
// 返回对象的类
Class object_getClass ( id obj );
// 设置对象的类
Class object_setClass ( id obj, Class cls );
```

### 3.4 获取类定义
```cpp
// 获取已注册的类定义的列表
int objc_getClassList ( Class *buffer, int bufferCount );

// 创建并返回一个指向所有已注册类的指针列表
Class * objc_copyClassList ( unsigned int *outCount );

// 返回指定类的类定义
Class objc_lookUpClass ( const char *name );
Class objc_getClass ( const char *name );
Class objc_getRequiredClass ( const char *name );

// 返回指定类的元类
Class objc_getMetaClass ( const char *name );
```

### 3.5 objc_property_t
属性类型，指向objc_property结构体
> typedef struct objc_property *objc_property_t;

通过class_copyPropertyList和protocol_copyPropertyList方法获取类和协议的属性
> objc_property_t *class_copyPropertyList(Class cls, unsigned int *outCount)
> objc_property_t *protocol_copyPropertyList(Protocol *proto, unsigned int *outCount)

### 3.6 objc_property_attribute_t
也是结构体，定义属性的attribute
```cpp
typedef struct {
     const char *name; // 特性名
     const char *value; // 特性值
} objc_property_attribute_t;
```

### 3.7 关联对象
```cpp
//将一个对象连接到其它对象
static char myKey;
objc_setAssociatedObject(self, &myKey, anObject, OBJC_ASSOCIATION_RETAIN);

//获取一个新的关联的对象
id anObject = objc_getAssociatedObject(self, &myKey);

//使用objc_removeAssociatedObjects函数移除一个关联对象
objc_removeAssociatedObjects(self);
```

## 4. 成员变量和属性的操作方法
### 4.1 成员变量
```cpp
// 获取成员变量名
const char * ivar_getName ( Ivar v );
// 获取成员变量类型编码
const char * ivar_getTypeEncoding ( Ivar v );
// 获取成员变量的偏移量
ptrdiff_t ivar_getOffset ( Ivar v );
```
### 4.2 Associated Objects
```cpp
// 设置关联对象
void objc_setAssociatedObject(id object, const void *key, id value, objc_AssociationPolicy policy);
// 获取关联对象
id objc_getAssociatedObject ( id object, const void *key );
// 移除关联对象
void objc_removeAssociatedObjects ( id object );

//上面方法以键值对的形式动态的向对象添加，获取或者删除关联值。其中关联政策是一组枚举常量。这些常量对应着引用关联值机制，也就是Objc内存管理的引用计数机制。
enum {
     OBJC_ASSOCIATION_ASSIGN = 0,
     OBJC_ASSOCIATION_RETAIN_NONATOMIC = 1,
     OBJC_ASSOCIATION_COPY_NONATOMIC = 3,
     OBJC_ASSOCIATION_RETAIN = 01401,
     OBJC_ASSOCIATION_COPY = 01403
};
```
### 4.3 属性
```cpp
// 获取属性名
const char * property_getName ( objc_property_t property );
// 获取属性特性描述字符串
const char * property_getAttributes ( objc_property_t property );
// 获取属性中指定的特性
char * property_copyAttributeValue ( objc_property_t property, const char *attributeName );
// 获取属性的特性列表
objc_property_attribute_t * property_copyAttributeList ( objc_property_t property, unsigned int *outCount );
```

## 5. Method相关操作函数
### 5.1 Method
```cpp
// 调用指定方法的实现，返回的是方法实现时的返回，参数receiver不能为空，这个比method_getImplementation和method_getName快
id method_invoke ( id receiver, Method m, ... );
// 调用返回一个数据结构的方法的实现
void method_invoke_stret ( id receiver, Method m, ... );
// 获取方法名，希望获得方法明的C字符串，使用sel_getName(method_getName(method))
SEL method_getName ( Method m );
// 返回方法的实现
IMP method_getImplementation ( Method m );
// 获取描述方法参数和返回值类型的字符串
const char * method_getTypeEncoding ( Method m );
// 获取方法的返回值类型的字符串
char * method_copyReturnType ( Method m );
// 获取方法的指定位置参数的类型字符串
char * method_copyArgumentType ( Method m, unsigned int index );
// 通过引用返回方法的返回值类型字符串
void method_getReturnType ( Method m, char *dst, size_t dst_len );
// 返回方法的参数的个数
unsigned int method_getNumberOfArguments ( Method m );
// 通过引用返回方法指定位置参数的类型字符串
void method_getArgumentType ( Method m, unsigned int index, char *dst, size_t dst_len );
// 返回指定方法的方法描述结构体
struct objc_method_description * method_getDescription ( Method m );
// 设置方法的实现
IMP method_setImplementation ( Method m, IMP imp );
// 交换两个方法的实现
void method_exchangeImplementations ( Method m1, Method m2 );
```

### 5.2 Method的SEL

```cpp
// 返回给定选择器指定的方法的名称
const char * sel_getName ( SEL sel );
// 在Objective-C Runtime系统中注册一个方法，将方法名映射到一个选择器，并返回这个选择器
SEL sel_registerName ( const char *str );
// 在Objective-C Runtime系统中注册一个方法
SEL sel_getUid ( const char *str );
// 比较两个选择器
BOOL sel_isEqual ( SEL lhs, SEL rhs );
```

### 5.3 获取Method地址
使用NSObject提供的methodForSelector:方法可以获得Method的指针，通过指针调用实现代码。

```cpp
void (*setter)(id, SEL, BOOL);
int i;
setter = (void (*)(id, SEL, BOOL))[target
     methodForSelector:@selector(setFilled:)];
for ( i = 0 ; i < 1000 ; i++ )
     setter(targetList[i], @selector(setFilled:), YES);
```

### 5.4 Method转发
如果使用[object message]调用方法，object无法响应message时就会报错。用performSelector...调用就要等到运行时才确定是否能接受，不能才崩溃。

```cpp
//先调用respondsToSelector:来判断一下
if ([self respondsToSelector:@selector(method)]) {
     [self performSelector:@selector(method)];
}
```

**Method转发机制分为三步：**
- 动态方法解析 
例如可以用@dynamic关键字在类的实现文件中写个属性
```objc
//这个表明会为这个属性动态提供set get方法，就是编译器是不会默认生成setPropertyName:和propertyName方法，需要动态提供。可以通过重载resolveInstanceMethod:和resolveClassMethod:方法分别添加实例方法和类方法实现。最后用class_addMethod完成添加特定方法实现的操作
@dynamic propertyName;

```
- 重定向接收者
如果无法处理消息会继续调用下面的方法，同时在这里Runtime系统实际上是给了一个替换消息接收者的机会，但是替换的对象千万不要是self，那样会进入死循环。

```cpp
- (id)forwardingTargetForSelector:(SEL)aSelector
{
     if(aSelector == @selector(mysteriousMethod:)){
          return alternateObject;
     }
     return [super forwardingTargetForSelector:aSelector];
}
```

- 消息转发
如果以上两种都没法处理未知消息就需要完整消息转发了。调用如下方法
```objc
//这一步是最后机会将消息转发给其它对象，对象会将未处理的消息相关的selector，target和参数都封装在anInvocation中。forwardInvocation:像未知消息分发中心，将未知消息转发给其它对象。注意的是forwardInvocation:方法只有在消息接收对象无法正常响应消息时才被调用。
- (void)forwardInvocation:(NSInvocation *)anInvocation
//必须重写这个方法，消息转发使用这个方法获得的信息创建NSInvocation对象。
- (NSMethodSignature *)methodSignatureForSelector:(SEL)aSelector
```

## 6. Protocol操作函数

```
// 返回指定的协议
Protocol * objc_getProtocol ( const char *name );
// 获取运行时所知道的所有协议的数组
Protocol ** objc_copyProtocolList ( unsigned int *outCount );
// 创建新的协议实例
Protocol * objc_allocateProtocol ( const char *name );
// 在运行时中注册新创建的协议
void objc_registerProtocol ( Protocol *proto ); //创建一个新协议后必须使用这个进行注册这个新协议，但是注册后不能够再修改和添加新方法。
// 为协议添加方法
void protocol_addMethodDescription ( Protocol *proto, SEL name, const char *types, BOOL isRequiredMethod, BOOL isInstanceMethod );
// 添加一个已注册的协议到协议中
void protocol_addProtocol ( Protocol *proto, Protocol *addition );
// 为协议添加属性
void protocol_addProperty ( Protocol *proto, const char *name, const objc_property_attribute_t *attributes, unsigned int attributeCount, BOOL isRequiredProperty, BOOL isInstanceProperty );
// 返回协议名
const char * protocol_getName ( Protocol *p );
// 测试两个协议是否相等
BOOL protocol_isEqual ( Protocol *proto, Protocol *other );
// 获取协议中指定条件的方法的方法描述数组
struct objc_method_description * protocol_copyMethodDescriptionList ( Protocol *p, BOOL isRequiredMethod, BOOL isInstanceMethod, unsigned int *outCount );
// 获取协议中指定方法的方法描述
struct objc_method_description protocol_getMethodDescription ( Protocol *p, SEL aSel, BOOL isRequiredMethod, BOOL isInstanceMethod );
// 获取协议中的属性列表
objc_property_t * protocol_copyPropertyList ( Protocol *proto, unsigned int *outCount );
// 获取协议的指定属性
objc_property_t protocol_getProperty ( Protocol *proto, const char *name, BOOL isRequiredProperty, BOOL isInstanceProperty );
// 获取协议采用的协议
Protocol ** protocol_copyProtocolList ( Protocol *proto, unsigned int *outCount );
// 查看协议是否采用了另一个协议
BOOL protocol_conformsToProtocol ( Protocol *proto, Protocol *other );
```

## 7. Block操作函数
```
// 创建一个指针函数的指针，该函数调用时会调用特定的block
IMP imp_implementationWithBlock ( id block );

// 返回与IMP(使用imp_implementationWithBlock创建的)相关的block
id imp_getBlock ( IMP anImp );

// 解除block与IMP(使用imp_implementationWithBlock创建的)的关联关系，并释放block的拷贝
BOOL imp_removeBlock ( IMP anImp );
```

## 8. 最后

- 通过Method Swizzling可以把事件代码或Logging，Authentication，Caching等跟主要业务逻辑代码解耦。这种处理方式叫做[Cross Cutting Concerns](http://en.wikipedia.org/wiki/Cross-cutting_concern)
- 用Method Swizzling动态给指定的方法添加代码解决Cross Cutting Concerns的编程方式叫[Aspect Oriented Programming](http://en.wikipedia.org/wiki/Aspect-oriented_programming)
- 目前有些第三方库可以很方便的使用AOP，比如[Aspects](https://github.com/steipete/Aspects), 这里是使用Aspects的[范例](https://github.com/okcomp/AspectsDemo)
