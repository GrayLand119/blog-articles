
---

title: TensorFlow学习笔记(9) - 图像处理数据
subtitle: tfln9
date: 2018-09-11 16:04:03
tags: TensorFlow
mathjax: true

---

<!--# TensorFlow学习笔记(9) - 图像处理数据-->

## TFRecord

`TFRecord`是一种输入数据格式, 方便统一记录输入数据的信息.

比如一个训练集, 一般情况下包含多个输入数据(图片或其他)和类别标签, 以及其他信息. 输入数据与类别标签之间的对应关系维护起来比较麻烦, `TFRecord`就是为了方便管理这些数据而生的.

`TFRecord`中保存的数据格式是 `tf.train.Example`, 定义如下:

```python
message Example {
  Features features = 1;
};

message Features {
  map<string, Feature> feature = 1;
};

message Feature {
  oneof kind {
    BytesList bytes_list = 1;
    FloatList float_list = 2;
    Int64List int64_list = 3;
  }
}
```

可见其数据结构比较简洁, 其主要结构就是一个字典, 维护一个`字符串类型的名称`和三个类型的数据列表(字符串, 实数, 整数)

##### TFRecord 写入/读取

写入:

```python
writer = tf.python_io.TFRecordWriter(fileName)
yourValue1 = ... # [1,2,3...]
...
feature1 = tf.train.Feature(int64_list=tf.train.Int64List(value=[yourValue1]))
feature2 = tf.train.Feature(bytes_list=tf.train.BytesList(value=[yourValue2]))
...
features = tf.train.Features(feature={
  'name':...,
  'label':...,
  'raw_data':feature1,
  'other':feature2
})

example = tf.train.Example(features=features)

writer.write(example.SerializeToString())
writer.close()
```

读取:

```python
reader = tf.TFRecordReader()
# 创建队列维护输入文件列表
filename_queue = tf.train.string_input_producer([path])

# reader.read_up_to() 一次读取多个样例
_, serialized_example = reader.read(filename_queue)

# tf.parse_example 解析多各样例
# 解析一个样例, 格式保持和写入的一致
features = tf.parse_single_example(serialized=serialized_example, features={
    'name':tf.FixedLenFeature([], tf.string),
    'label':tf.FixedLenFeature([], tf.string),
    'raw_data':tf.FixedLenFeature([], tf.int64),
    'other':tf.FixedLenFeature([], tf.uint8)
})

# 取出数据
feature1 = tf.cast(features['name'], tf.string)
feature2 = tf.cast(features['other'], tf.uint8)
# tf.decode_raw 将字符串解析成图像对应的像素数组
feature3 = tf.decode_raw(features['raw_data'], tf.int64)

with tf.Session() as sess:
    f1, f2, f3 = sess.run([feature1, feature2, feature3])
    ...
  
```

## 图像处理函数

以下部分图像处理函数加入 `random` 前缀可以使用随机处理方法. 通过随机的处理可以扩充一些样本, 从而增强训练结果的健壮性.

### 图像大小调整

`resize_images`: 缩放和拉伸的调整.
`resize_image_with_crop_or_pad`: 裁切和填充的调整.
`central_crop`: 根据中心裁切

以下是官方API的描述, 更多缩放方法可以查看官网文档:

```python
resize_images(images, size, method=0, align_corners=False, preserve_aspect_ratio=False)
    Resize `images` to `size` using the specified `method`.
    
    Resized images will be distorted if their original aspect ratio is not
    the same as `size`.  To avoid distortions see
    @{tf.image.resize_image_with_pad}.
    
    `method` can be one of:
    
    *   <b>`ResizeMethod.BILINEAR`</b>: [Bilinear interpolation.](
      https://en.wikipedia.org/wiki/Bilinear_interpolation)
    *   <b>`ResizeMethod.NEAREST_NEIGHBOR`</b>: [Nearest neighbor interpolation.](
      https://en.wikipedia.org/wiki/Nearest-neighbor_interpolation)
    *   <b>`ResizeMethod.BICUBIC`</b>: [Bicubic interpolation.](
      https://en.wikipedia.org/wiki/Bicubic_interpolation)
    *   <b>`ResizeMethod.AREA`</b>: Area interpolation.
    
    The return value has the same type as `images` if `method` is
    `ResizeMethod.NEAREST_NEIGHBOR`. It will also have the same type as `images`
    if the size of `images` can be statically determined to be the same as `size`,
    because `images` is returned in this case. Otherwise, the return value has
    type `float32`.
    
    Args:
      images: 4-D Tensor of shape `[batch, height, width, channels]` or
              3-D Tensor of shape `[height, width, channels]`.
      size: A 1-D int32 Tensor of 2 elements: `new_height, new_width`.  The
            new size for the images.
      method: ResizeMethod.  Defaults to `ResizeMethod.BILINEAR`.
      align_corners: bool.  If True, the centers of the 4 corner pixels of the
          input and output tensors are aligned, preserving the values at the
          corner pixels. Defaults to `False`.
      preserve_aspect_ratio: Whether to preserve the aspect ratio. If this is set,
        then `images` will be resized to a size that fits in `size` while
        preserving the aspect ratio of the original image. Scales up the image if
        `size` is bigger than the current size of the `image`. Defaults to False.
    
    Raises:
      ValueError: if the shape of `images` is incompatible with the
        shape arguments to this function
      ValueError: if `size` has invalid shape or type.
      ValueError: if an unsupported resize method is specified.
    
    Returns:
      If `images` was 4-D, a 4-D float Tensor of shape
      `[batch, new_height, new_width, channels]`.
      If `images` was 3-D, a 3-D float Tensor of shape
      `[new_height, new_width, channels]`.
      
resize_image_with_crop_or_pad(image, target_height, target_width)
    Crops and/or pads an image to a target width and height.
    
    Resizes an image to a target width and height by either centrally
    cropping the image or padding it evenly with zeros.
    
    If `width` or `height` is greater than the specified `target_width` or
    `target_height` respectively, this op centrally crops along that dimension.
    If `width` or `height` is smaller than the specified `target_width` or
    `target_height` respectively, this op centrally pads with 0 along that
    dimension.
    
    Args:
      image: 4-D Tensor of shape `[batch, height, width, channels]` or
             3-D Tensor of shape `[height, width, channels]`.
      target_height: Target height.
      target_width: Target width.
    
    Raises:
      ValueError: if `target_height` or `target_width` are zero or negative.
    
    Returns:
      Cropped and/or padded image.
      If `images` was 4-D, a 4-D float Tensor of shape
      `[batch, new_height, new_width, channels]`.
      If `images` was 3-D, a 3-D float Tensor of shape
      `[new_height, new_width, channels]`.

central_crop(image, central_fraction)
    Crop the central region of the image(s).
    
    Remove the outer parts of an image but retain the central region of the image
    along each dimension. If we specify central_fraction = 0.5, this function
    returns the region marked with "X" in the below diagram.
    
         --------
        |        |
        |  XXXX  |
        |  XXXX  |
        |        |   where "X" is the central 50% of the image.
         --------
    
    This function works on either a single image (`image` is a 3-D Tensor), or a
    batch of images (`image` is a 4-D Tensor).
    
    Args:
      image: Either a 3-D float Tensor of shape [height, width, depth], or a 4-D
        Tensor of shape [batch_size, height, width, depth].
      central_fraction: float (0, 1], fraction of size to crop
    
    Raises:
      ValueError: if central_crop_fraction is not within (0, 1].
    
    Returns:
      3-D / 4-D float Tensor, as per the input.
```
### 图像翻转

`tf.image.flip_up_down`: 上下翻转
`tf.image.flip_left_right`: 左右翻转
`tf.image.transpose_image`: 对角线翻转

### 色彩调整

`tf.image.adjust_brightness`: 调整亮度, 类似的还有:

* adjust_contrast
* adjust_gamma
* adjust_hue
* adjust_jpeg_quality
* adjust_saturation

### 处理标注框

`tf.image.draw_bounding_boxes`: 处理标注框, 参数 images, boxes 都是多一维的数据, 使得其一次处理一个 batch 的数据. 故使用前需要注意, 将1张图片扩充1个维度. 如下代码:

```python
batched = tf.expand_dims(tf.image.convert_image_dtype(img_data_org, tf.float32), 0)
boxes = tf.constant([[[0., 0., 0.3, 0.3], [0.5, 0.5, 0.6, 0.6]]])
img_note = tf.image.draw_bounding_boxes(batched, boxes)
```


