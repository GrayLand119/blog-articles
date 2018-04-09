---
title: iOS中使用OpenCV进行线性拟合(直线and曲线)
subtitle: iOSOCVFL
date: 2017-03-28 11:20:00
tags: OpenCV
---

先上[Github地址](https://github.com/GrayLand119/FittingAlgorithm)

线性拟合的应用领域比较广泛, 如运动轨迹计算、数据分析、图像处理等领域,  故在此写一篇学习相关文章.

# 直线拟合

在说直线拟合前我们先来复习一下**直线方程**. 直线方程的表达式有以下几种([引用自百度](http://baike.baidu.com/item/%E7%9B%B4%E7%BA%BF%E6%96%B9%E7%A8%8B?fr=aladdin)):

1. [一般式](http://baike.baidu.com/item/%E4%B8%80%E8%88%AC%E5%BC%8F):**Ax+By+C=0**(A、B不同时为0)【适用于所有直线】
A1/A2=B1/B2≠C1/C2←→两直线平行
A1/A2=B1/B2=C1/C2←→两直线重合
横截距a=-C/A
纵截距b=-C/B
2. [点斜式](http://baike.baidu.com/item/%E7%82%B9%E6%96%9C%E5%BC%8F):**y-y0=k(x-x0) 【**适用于不垂直于x轴的直线**】**
表示斜率为k，且过（x0,y0）的直线
3. [截距式](http://baike.baidu.com/item/%E6%88%AA%E8%B7%9D%E5%BC%8F):**x/a+y/b=1**【适用于不过原点或不垂直于x轴、y轴的直线】
表示与x轴、y轴相交，且x轴截距为a，y轴截距为b的直线
4. [斜截式](http://baike.baidu.com/item/%E6%96%9C%E6%88%AA%E5%BC%8F):y**=kx+b【**适用于不垂直于x轴的直线**】**
表示斜率为k且y轴截距为b的直线
5. [两点式](http://baike.baidu.com/item/%E4%B8%A4%E7%82%B9%E5%BC%8F):【适用于不垂直于x轴、y轴的直线】
表示过（x1,y1）和(x2,y2)的直线
**(y-y1)/(y2-y1)=(x-x1)/(x2-x1) **(****x1≠x2，y1≠y2****)****
6. 交点式:f1(x,y) *m+f2(x,y)=0 【适用于任何直线】
表示过直线f1(x,y)=0与直线f2(x,y)=0的交点的直线
7. 点平式:f(x,y) -f(x0,y0)=0【适用于任何直线】
表示过点（x0,y0）且与直线f（x,y）=0平行的直线
8. [法线](http://baike.baidu.com/item/%E6%B3%95%E7%BA%BF)式：**x·cosα+ysinα-p=0【适用于不平行于坐标轴的直线】**
过原点向直线做一条的垂线段，该垂线段所在直线的倾斜角为α，p是该线段的长度
9. [点向式](http://baike.baidu.com/item/%E7%82%B9%E5%90%91%E5%BC%8F)：**(x-x0)/u=(y-y0)/v (u≠0,v≠0)【适用于任何直线】**
表示过点(x0,y0)且方向[向量](http://baike.baidu.com/item/%E5%90%91%E9%87%8F)为（u,v ）的直线
10. 法向式：**a（x-x0）+b（y-y0）=0**【适用于任何直线】****
表示过点（x0，y0）且与向量（a，b）垂直的直线

在OpenCV中使用的是[点向式](http://baike.baidu.com/item/%E7%82%B9%E5%90%91%E5%BC%8F)：**(x-x0)/u=(y-y0)/v (u≠0,v≠0)**

在OpenCV中我们可以主要使用fitLine函数进行直线拟合, 其算法基于最小二乘法实现的, 关于最小二乘法后续再作详细介绍. fitLine函数定义如下:

```cpp
void fitLine( InputArray points, OutputArray line, int distType, double param, double reps, double aeps );
```

该方法可以对二维或三维的点集进行拟合,  在二维模式下返回一个Vec4f的元素, 分别是点向式中的**(u,v,x,y)**

参数介绍:
**points**
输入一个二维或三维的向量, 数据结构可以是std::vector<> 或 Mat(推荐使用).

**line**
二维模式下返回Vec4f的元素(u,v,x,y), 三维模式下返回Vec6f的元素(vx, vy, vz, x0, y0, z0)

**distType**
拟合算法, 这里的拟合算法基于[M-estimators](http://en.wikipedia.org/wiki/M-estimator)实现, 有以下几种:

```cpp
enum DistanceTypes {
    DIST_USER    = -1,  //!< User defined distance
    DIST_L1      = 1,   //!< distance = |x1-x2| + |y1-y2|
    DIST_L2      = 2,   //!< the simple euclidean distance
    DIST_C       = 3,   //!< distance = max(|x1-x2|,|y1-y2|)
    DIST_L12     = 4,   //!< L1-L2 metric: distance = 2(sqrt(1+x*x/2) - 1))
    DIST_FAIR    = 5,   //!< distance = c^2(|x|/c-log(1+|x|/c)), c = 1.3998
    DIST_WELSCH  = 6,   //!< distance = c^2/2(1-exp(-(x/c)^2)), c = 2.9846
    DIST_HUBER   = 7    //!< distance = |x|<c ? x^2/2 : c(|x|-c/2), c=1.345
};
```

其算法主要使用的是加权最小二乘法, 分别采用如下算法:

![DistanceTypes](http://upload-images.jianshu.io/upload_images/1084866-673d820bbc31ea36.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

其中CV_DIST_L2为最简单快速的最小二乘法, 推荐使用.

**param**
拟合算法中的的C参, 设置为0时系统自动选用最优值.

**reps**
算法精度radius, 官方推荐0.01

**aeps**
算法精度angle, 官方推荐0.01

# 曲线拟合

首先，曲线的函数类型有:双曲线型、对数型、指数型、多项式型等。

对于最常见的曲线, 其特征接近于多项式型, 所以这里的曲线拟合问题就变成了多项式回归求解.
一般情况下,对实际的点数据进行求解是无解的, 所以我们需要引入最小二乘法来求解.(对于最小二乘法的原理和求解过程,后续再详细介绍)

在OpenCV中没有找到拟合曲线的算子, 这里使用C++来实现. 此算法迭代次数大于10时求解均为0. 若有更优的算法可以在评论中交流.

```cpp
bool fittingCurve(vector<Point2f> &vec,int times,float *p) // 输入点数据, 迭代次数, 输出多项式参数
{
    float *py = new float[vec.size()];
    float *px = new float[times*vec.size()];
    int i = 0;
    
    for(vector<Point2f>::iterator itr = vec.begin();itr!=vec.end();++itr) {
        
        py[i] = (*itr).y;
        int j=0;
        while (j<times)
        {
            px[times*i+j] = pow(((*itr).x),float(j));
            j++;
        }
        i++;
    }
    
    Mat X = Mat((int)vec.size(),times,CV_32FC1,px);
    Mat X_T;
    transpose(X,X_T);
    
    Mat Y = Mat((int)vec.size(),1,CV_32FC1,py);
    Mat para = ((X_T*X).inv())*X_T*Y;
    
    for (int s = 0; s<times;s++){
        p[s] = para.at<float>(s);
    }
    
    delete[] px;
    delete[] py;
    
    return true;
}
```
下面我们来验证一组数据:

```cpp
        int x[]={50,100,150,200,250,300,350,400,450,500,550,600,650,700,750};
        int y[]={428,454,480,506,532,458,384,210,636,662,688,778,504,430,456};
```

当迭代次数为3的时候求解结果为:
```cpp
381.534
0.575073
-0.000505627
```
即:y = 381.534 + 0.575073x + -0.000505627x², 图像如下:

![](//upload-images.jianshu.io/upload_images/1084866-c2309feb690782b8.jpg)

当迭代次数为7的时候求解结果为:
```cpp
-210.757
17.1697
-0.132375
0.000430976
-6.52814e-07
4.45947e-10
-1.06088e-13
```

图像如下:
![](//upload-images.jianshu.io/upload_images/1084866-27510e1eb2eadb07.jpg)

以下是一些自己测试的数据:

![](//upload-images.jianshu.io/upload_images/1084866-8fd65adeebad5459.gif)