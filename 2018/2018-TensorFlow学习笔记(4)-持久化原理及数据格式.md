---

title: TensorFlow学习笔记(4) - 持久化原理及数据格式
subtitle: tfln4
date: 2018-08-20 13:43:59
tags: TensorFlow
mathjax: true

---

<!--# TensorFlow学习笔记(4) - 持久化原理及数据格式-->


上一节笔记中记录了调用 `saver.save()` 会生成三个文件.

知识点:

* TensorFlow 通过图的形式来表述计算, 其中所有的计算会被表达为计算图上的节点.
* `元图(MetaGraph)`记录计算图中节点的信息以及运行计算图中节点需要的`元数据`
* `元图(MetaGraph)`是由` MetaGraphDef Protocol Buffer` 定义的
* `MetaGraphDef`默认保存为`.meta` 后缀的文件

`MetaGraphDef`类型定义:

```python
message MetaGraphDef {
  MetaInfoDef meta_info_def = 1;
  GraphDef graphd_def = 2;
  SaverDef saver_def = 3;
  map<string, CollectionDef> collection_def = 4;
  map<string, SignatureDef> signature_def = 5;
}

```

默认保存的`.meta`文件是二进制形式保存的, `export_meta_graph`函数支持 JSON 格式导出.

```python
# ...
# 导出
saver.export_meta_graph("./.../YourModel.ckpt.meta.json", as_text=True)
```

以下是我的代码:

```python
#...
v1 = tf.Variable(tf.constant(1.0, shape=[1]), name='v1')
v2 = tf.Variable(tf.constant(1.0, shape=[1]), name='v2')
result = v1 + v2

saver = tf.train.Saver()
saver.export_meta_graph('./SaveModels/Model4.ckpt.meta.json', as_text=True)

#以下是 json 文件的内容
"""
meta_info_def {
  stripped_op_list {
    op {
      name: "Add"
      input_arg {
        name: "x"
        type_attr: "T"
      }
      input_arg {
        name: "y"
        type_attr: "T"
      }
      output_arg {
        name: "z"
        type_attr: "T"
      }
      attr {
        name: "T"
        type: "type"
        allowed_values {
          list {
            type: DT_BFLOAT16
            type: DT_HALF
            type: DT_FLOAT
            type: DT_DOUBLE
            type: DT_UINT8
            type: DT_INT8
            type: DT_INT16
            type: DT_INT32
            type: DT_INT64
            type: DT_COMPLEX64
            type: DT_COMPLEX128
            type: DT_STRING
          }
        }
      }
    }
    op {
      name: "Assign"
      input_arg {
        name: "ref"
        type_attr: "T"
        is_ref: true
      }
      input_arg {
        name: "value"
        type_attr: "T"
      }
      output_arg {
        name: "output_ref"
        type_attr: "T"
        is_ref: true
      }
      attr {
        name: "T"
        type: "type"
      }
      attr {
        name: "validate_shape"
        type: "bool"
        default_value {
          b: true
        }
      }
      attr {
        name: "use_locking"
        type: "bool"
        default_value {
          b: true
        }
      }
      allows_uninitialized_input: true
    }
    op {
      name: "Const"
      output_arg {
        name: "output"
        type_attr: "dtype"
      }
      attr {
        name: "value"
        type: "tensor"
      }
      attr {
        name: "dtype"
        type: "type"
      }
    }
    op {
      name: "Identity"
      input_arg {
        name: "input"
        type_attr: "T"
      }
      output_arg {
        name: "output"
        type_attr: "T"
      }
      attr {
        name: "T"
        type: "type"
      }
    }
    op {
      name: "NoOp"
    }
    op {
      name: "RestoreV2"
      input_arg {
        name: "prefix"
        type: DT_STRING
      }
      input_arg {
        name: "tensor_names"
        type: DT_STRING
      }
      input_arg {
        name: "shape_and_slices"
        type: DT_STRING
      }
      output_arg {
        name: "tensors"
        type_list_attr: "dtypes"
      }
      attr {
        name: "dtypes"
        type: "list(type)"
        has_minimum: true
        minimum: 1
      }
      is_stateful: true
    }
    op {
      name: "SaveV2"
      input_arg {
        name: "prefix"
        type: DT_STRING
      }
      input_arg {
        name: "tensor_names"
        type: DT_STRING
      }
      input_arg {
        name: "shape_and_slices"
        type: DT_STRING
      }
      input_arg {
        name: "tensors"
        type_list_attr: "dtypes"
      }
      attr {
        name: "dtypes"
        type: "list(type)"
        has_minimum: true
        minimum: 1
      }
      is_stateful: true
    }
    op {
      name: "VariableV2"
      output_arg {
        name: "ref"
        type_attr: "dtype"
        is_ref: true
      }
      attr {
        name: "shape"
        type: "shape"
      }
      attr {
        name: "dtype"
        type: "type"
      }
      attr {
        name: "container"
        type: "string"
        default_value {
          s: ""
        }
      }
      attr {
        name: "shared_name"
        type: "string"
        default_value {
          s: ""
        }
      }
      is_stateful: true
    }
  }
  tensorflow_version: "1.9.0"
  tensorflow_git_version: "v1.9.0-0-g25c197e023"
}
graph_def {
  node {
    name: "Const"
    op: "Const"
    attr {
      key: "_output_shapes"
      value {
        list {
          shape {
            dim {
              size: 1
            }
          }
        }
      }
    }
    attr {
      key: "dtype"
      value {
        type: DT_FLOAT
      }
    }
    attr {
      key: "value"
      value {
        tensor {
          dtype: DT_FLOAT
          tensor_shape {
            dim {
              size: 1
            }
          }
          float_val: 1.0
        }
      }
    }
  }
  node {
    name: "v1"
    op: "VariableV2"
    attr {
      key: "_output_shapes"
      value {
        list {
          shape {
            dim {
              size: 1
            }
          }
        }
      }
    }
    attr {
      key: "container"
      value {
        s: ""
      }
    }
    attr {
      key: "dtype"
      value {
        type: DT_FLOAT
      }
    }
    attr {
      key: "shape"
      value {
        shape {
          dim {
            size: 1
          }
        }
      }
    }
    attr {
      key: "shared_name"
      value {
        s: ""
      }
    }
  }
  node {
    name: "v1/Assign"
    op: "Assign"
    input: "v1"
    input: "Const"
    attr {
      key: "T"
      value {
        type: DT_FLOAT
      }
    }
    attr {
      key: "_class"
      value {
        list {
          s: "loc:@v1"
        }
      }
    }
    attr {
      key: "_output_shapes"
      value {
        list {
          shape {
            dim {
              size: 1
            }
          }
        }
      }
    }
    attr {
      key: "use_locking"
      value {
        b: true
      }
    }
    attr {
      key: "validate_shape"
      value {
        b: true
      }
    }
  }
  node {
    name: "v1/read"
    op: "Identity"
    input: "v1"
    attr {
      key: "T"
      value {
        type: DT_FLOAT
      }
    }
    attr {
      key: "_class"
      value {
        list {
          s: "loc:@v1"
        }
      }
    }
    attr {
      key: "_output_shapes"
      value {
        list {
          shape {
            dim {
              size: 1
            }
          }
        }
      }
    }
  }
  node {
    name: "Const_1"
    op: "Const"
    attr {
      key: "_output_shapes"
      value {
        list {
          shape {
            dim {
              size: 1
            }
          }
        }
      }
    }
    attr {
      key: "dtype"
      value {
        type: DT_FLOAT
      }
    }
    attr {
      key: "value"
      value {
        tensor {
          dtype: DT_FLOAT
          tensor_shape {
            dim {
              size: 1
            }
          }
          float_val: 1.0
        }
      }
    }
  }
  node {
    name: "v2"
    op: "VariableV2"
    attr {
      key: "_output_shapes"
      value {
        list {
          shape {
            dim {
              size: 1
            }
          }
        }
      }
    }
    attr {
      key: "container"
      value {
        s: ""
      }
    }
    attr {
      key: "dtype"
      value {
        type: DT_FLOAT
      }
    }
    attr {
      key: "shape"
      value {
        shape {
          dim {
            size: 1
          }
        }
      }
    }
    attr {
      key: "shared_name"
      value {
        s: ""
      }
    }
  }
  node {
    name: "v2/Assign"
    op: "Assign"
    input: "v2"
    input: "Const_1"
    attr {
      key: "T"
      value {
        type: DT_FLOAT
      }
    }
    attr {
      key: "_class"
      value {
        list {
          s: "loc:@v2"
        }
      }
    }
    attr {
      key: "_output_shapes"
      value {
        list {
          shape {
            dim {
              size: 1
            }
          }
        }
      }
    }
    attr {
      key: "use_locking"
      value {
        b: true
      }
    }
    attr {
      key: "validate_shape"
      value {
        b: true
      }
    }
  }
  node {
    name: "v2/read"
    op: "Identity"
    input: "v2"
    attr {
      key: "T"
      value {
        type: DT_FLOAT
      }
    }
    attr {
      key: "_class"
      value {
        list {
          s: "loc:@v2"
        }
      }
    }
    attr {
      key: "_output_shapes"
      value {
        list {
          shape {
            dim {
              size: 1
            }
          }
        }
      }
    }
  }
  node {
    name: "add"
    op: "Add"
    input: "v1/read"
    input: "v2/read"
    attr {
      key: "T"
      value {
        type: DT_FLOAT
      }
    }
    attr {
      key: "_output_shapes"
      value {
        list {
          shape {
            dim {
              size: 1
            }
          }
        }
      }
    }
  }
  node {
    name: "save/Const"
    op: "Const"
    attr {
      key: "_output_shapes"
      value {
        list {
          shape {
          }
        }
      }
    }
    attr {
      key: "dtype"
      value {
        type: DT_STRING
      }
    }
    attr {
      key: "value"
      value {
        tensor {
          dtype: DT_STRING
          tensor_shape {
          }
          string_val: "model"
        }
      }
    }
  }
  node {
    name: "save/SaveV2/tensor_names"
    op: "Const"
    attr {
      key: "_output_shapes"
      value {
        list {
          shape {
            dim {
              size: 2
            }
          }
        }
      }
    }
    attr {
      key: "dtype"
      value {
        type: DT_STRING
      }
    }
    attr {
      key: "value"
      value {
        tensor {
          dtype: DT_STRING
          tensor_shape {
            dim {
              size: 2
            }
          }
          string_val: "v1"
          string_val: "v2"
        }
      }
    }
  }
  node {
    name: "save/SaveV2/shape_and_slices"
    op: "Const"
    attr {
      key: "_output_shapes"
      value {
        list {
          shape {
            dim {
              size: 2
            }
          }
        }
      }
    }
    attr {
      key: "dtype"
      value {
        type: DT_STRING
      }
    }
    attr {
      key: "value"
      value {
        tensor {
          dtype: DT_STRING
          tensor_shape {
            dim {
              size: 2
            }
          }
          string_val: ""
          string_val: ""
        }
      }
    }
  }
  node {
    name: "save/SaveV2"
    op: "SaveV2"
    input: "save/Const"
    input: "save/SaveV2/tensor_names"
    input: "save/SaveV2/shape_and_slices"
    input: "v1"
    input: "v2"
    attr {
      key: "dtypes"
      value {
        list {
          type: DT_FLOAT
          type: DT_FLOAT
        }
      }
    }
  }
  node {
    name: "save/control_dependency"
    op: "Identity"
    input: "save/Const"
    input: "^save/SaveV2"
    attr {
      key: "T"
      value {
        type: DT_STRING
      }
    }
    attr {
      key: "_class"
      value {
        list {
          s: "loc:@save/Const"
        }
      }
    }
    attr {
      key: "_output_shapes"
      value {
        list {
          shape {
          }
        }
      }
    }
  }
  node {
    name: "save/RestoreV2/tensor_names"
    op: "Const"
    device: "/device:CPU:0"
    attr {
      key: "_output_shapes"
      value {
        list {
          shape {
            dim {
              size: 2
            }
          }
        }
      }
    }
    attr {
      key: "dtype"
      value {
        type: DT_STRING
      }
    }
    attr {
      key: "value"
      value {
        tensor {
          dtype: DT_STRING
          tensor_shape {
            dim {
              size: 2
            }
          }
          string_val: "v1"
          string_val: "v2"
        }
      }
    }
  }
  node {
    name: "save/RestoreV2/shape_and_slices"
    op: "Const"
    device: "/device:CPU:0"
    attr {
      key: "_output_shapes"
      value {
        list {
          shape {
            dim {
              size: 2
            }
          }
        }
      }
    }
    attr {
      key: "dtype"
      value {
        type: DT_STRING
      }
    }
    attr {
      key: "value"
      value {
        tensor {
          dtype: DT_STRING
          tensor_shape {
            dim {
              size: 2
            }
          }
          string_val: ""
          string_val: ""
        }
      }
    }
  }
  node {
    name: "save/RestoreV2"
    op: "RestoreV2"
    input: "save/Const"
    input: "save/RestoreV2/tensor_names"
    input: "save/RestoreV2/shape_and_slices"
    device: "/device:CPU:0"
    attr {
      key: "_output_shapes"
      value {
        list {
          shape {
            unknown_rank: true
          }
          shape {
            unknown_rank: true
          }
        }
      }
    }
    attr {
      key: "dtypes"
      value {
        list {
          type: DT_FLOAT
          type: DT_FLOAT
        }
      }
    }
  }
  node {
    name: "save/Assign"
    op: "Assign"
    input: "v1"
    input: "save/RestoreV2"
    attr {
      key: "T"
      value {
        type: DT_FLOAT
      }
    }
    attr {
      key: "_class"
      value {
        list {
          s: "loc:@v1"
        }
      }
    }
    attr {
      key: "_output_shapes"
      value {
        list {
          shape {
            dim {
              size: 1
            }
          }
        }
      }
    }
    attr {
      key: "use_locking"
      value {
        b: true
      }
    }
    attr {
      key: "validate_shape"
      value {
        b: true
      }
    }
  }
  node {
    name: "save/Assign_1"
    op: "Assign"
    input: "v2"
    input: "save/RestoreV2:1"
    attr {
      key: "T"
      value {
        type: DT_FLOAT
      }
    }
    attr {
      key: "_class"
      value {
        list {
          s: "loc:@v2"
        }
      }
    }
    attr {
      key: "_output_shapes"
      value {
        list {
          shape {
            dim {
              size: 1
            }
          }
        }
      }
    }
    attr {
      key: "use_locking"
      value {
        b: true
      }
    }
    attr {
      key: "validate_shape"
      value {
        b: true
      }
    }
  }
  node {
    name: "save/restore_all"
    op: "NoOp"
    input: "^save/Assign"
    input: "^save/Assign_1"
  }
  versions {
    producer: 26
  }
}
saver_def {
  filename_tensor_name: "save/Const:0"
  save_tensor_name: "save/control_dependency:0"
  restore_op_name: "save/restore_all"
  max_to_keep: 5
  keep_checkpoint_every_n_hours: 10000.0
  version: V2
}
collection_def {
  key: "trainable_variables"
  value {
    bytes_list {
      value: "\n\004v1:0\022\tv1/Assign\032\tv1/read:02\007Const:08\001"
      value: "\n\004v2:0\022\tv2/Assign\032\tv2/read:02\tConst_1:08\001"
    }
  }
}
collection_def {
  key: "variables"
  value {
    bytes_list {
      value: "\n\004v1:0\022\tv1/Assign\032\tv1/read:02\007Const:08\001"
      value: "\n\004v2:0\022\tv2/Assign\032\tv2/read:02\tConst_1:08\001"
    }
  }
}
"""
```


下面逐一讲解一下各个属性:

### 1.1 meta_info_def 属性

定义如下:

```python
message MetaInfoDef {
  string meta_graph_version = 1;
  OpList stripped_op_list = 2;
  google.protobuf.Any any_info = 3;
  repeated string tags = 4;
}
```

`MetaInfoDef` 记录了计算图版本号`meta_graph_version`, 以及一些标签 `tags`.

如果没有在 saver 中指定, 除了`stripped_op_list` 都为空.

`stripped_op_list` 保存的是 TensorFlow 中运算方法信息, 如果某运算方法在图中出现多次, 在`stripped_op_list`中也只出现一次.

`stripped_op_list`的类型是`OpList`.

以下是`OpList`类型定义:

```python
message OpDef {
  # 运算名, 也是唯一标识符, 通过运算名来引用不同运算
  string name = 1;
  # 定义运算输入输出参数, 因为可以是多个,所以类型为 repeated
  repeated ArgDef input_arg = 2;
  repeated ArgDef output_arg = 3;
  # 运算参数信息
  repeated AttrDef attr = 4;
  # 以上四个定义核心信息
  
  string summary = 5;
  string description = 6;
  OpDeprecation deprecation = 8;
  
  bool is_comutative = 18;
  bool is_aggregate = 16;
  bool is_stateful = 17;
  bool allows_uninitialized_input = 19;
}
```

例如上面的例子, 有2个输入1个输出, attr指定了输入输出允许的参数类型 通过类型` T`关联.

### 1.2 graph_def 属性

`graph_def` 记录了图上节点信息.因为` meta_info_def`属性中记录了所有运算的具体信息, 所以`graph_def` 只关注运算的连接结构.

以下是 `graph_def`结构:

```python
message GraphDef {
  repeated NodeDef node = 1;
  VersionDef versions = 4;
}
```

其中, `versions`属性比较简单, 主要存储了版本号.

主要信息存在` node` 属性中, 它记录了计算图上所有节点信息. 以下是类型定义

```python
message NodeDef {
  # 属性名称, 唯一标识符
  string name = 1;
  # 运算方法名, 对应 meta_info_def 中 op 的 name
  string op = 2;
  # 详细说明见下文
  repeated string input = 3;
  # 指定处理这个运算的设备, CPU or GPU, 本地 or 远程
  # device 为空时, 自动选择
  string device = 4;
  map<string, AAttrValue> attr = 5;
}
```

其中 `input` 是字符串列表, 形式为` node:scr_output`, 当`scr_output` 等于0时, 可以省略, 例如 `add:0`可以表示为`add`, `v1:0`表示`v1`的第一个输出, 也可标记为`v1`.

### 1.3 saver_def 属性

`saver_def`记录持久化模型时需要用的一些参数.如文件名/保存操作or加载操作的名称/保存频率/清理历史记录等...

主要结构 略.

关键字段:

* `filename_tensor_name` 保存文件的张量名称, 如` save/Const:0`, 保存节点` save/Const` 的第一个输出
* `save_tensor_name` 持久化模型运算所对应的节点名称. 如` save/control_dependency:0`,对应` graph_def` 中给出的` save/control_dependency` 节点, 与其对应的是加载模型的运算, 此名称由` restore_op_name`给出.
* `max_to_keep` 保存清理之前保存模型的策略, 如` max_to_keep`=5时, 第6次调用会清理最早的那一次保存.
* `keep_checkpoint_every_n_hours`, 每 n 个小时过后可以在 `max_top_keep`的基础上多保存一个模型.


### 1.4 collection_def 属性

`tf.Graph` 中可以维护不同的集合, 其底层实现是通过`collection_def`属性实现的.

`collection_def`属性是一个从集合名称到集合内容的映射.

主要维护4类(NodeList/BytesList/Int64List/FloatList)不同集合, 和1类其他集合(AnyList).

* `NodeList` 维护图上节点集合
* `BytesList`维护字符串或序列化后的`ProtocolBuffer`的集合, 如张量是通过` ProtocolBuffer` 表示的, 张量集合就是一个` ButesList`.
* `Int64List`维护整数集合
* `FloatList`维护实数集合

以下是之前上面代码保存的`collection_def` 内容:

```python
collection_def {
  key: "trainable_variables"
  value {
    bytes_list {
      value: "\n\004v1:0\022\tv1/Assign\032\tv1/read:02\007Const:08\001"
      value: "\n\004v2:0\022\tv2/Assign\032\tv2/read:02\tConst_1:08\001"
    }
  }
}
collection_def {
  key: "variables"
  value {
    bytes_list {
      value: "\n\004v1:0\022\tv1/Assign\032\tv1/read:02\007Const:08\001"
      value: "\n\004v2:0\022\tv2/Assign\032\tv2/read:02\tConst_1:08\001"
    }
  }
}
```

可见这里维护了2个集合, 一个是`trainable_variables` 一个是 `variables`, 这两个元素是一样 的, 都是变量 v1 和 v2. 它们是系统自动维护的.

### 1.5 checkpoint 文件

`checkpoint`文件名是固定的, 系统自动生成和维护.

其内容维护了`tf.train.Saver` 类持久化的所有模型文件的文件名. 当某个模型被删除时,这个模型对应的文件名也会从` checkpoint` 中删除

其中属性`model_checkpoint_path`保存最新的模型文件名.

`all_model_checkpoint_paths`保存还没有被删除的所有模型文件名.

## 总结

本次主要学习了`*.ckpt.meta` 文件的内容和结构. 其主要保存计算图中信息/操作/结构.对象是`MetaGraphDef`.其属性主要有:

* `meta_info_def`属性保存所有用到运算方法信息和计算图版本/用户自定义标签
* `graph_def`属性记录计算图上节点的连接结构信息
* `saver_def`记录持久化模型时用到的参数
* `collection_def`记录集合名称到集合内容的映射


`*.ckpt`主要保存了变量的值, `tf.train.NewCheckpointReader`类可以查看`*.ckpt` 文件中保存的变量信息.

```python
#...
# 读取所有变量
reader = tf.train.NewCheckpointReader("./SaveModels/model1.ckpt")

# 变量列表, 是一个字典列表 key:变量名, value:变量维度
all_variables = reader.get_variable_to_shape_map()

# 获取变量 v1 的取值
print(reader.get_tensor("v1"))

```




