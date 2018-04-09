---
title: Xcode环境变量
subtitle: XCENVP
date: 2016-08-12 00:00:00
tags: Xcode
---

* `SYSTEM_LIBRARY_DIR`: 系统库路径，默认为：/System/Library
* `$SYSTEM_LIBRARY_DIR/Extensions` 系统核心扩展工程目录，里面放的都是.kext/.plugin/.bundle 等类型的文件
* `$USER_LIBRARY_DIR/Automator` : Action project.
* `$HOME/Applications` : Application project.
* `$HOME/Library/Bundles`: Audio unit and bundle projects.
* `$HOME/bin`: Command-line utility project. * $DSTROOT: Apple plug-in project (complete path depends on specific project template).
* `/usr/local/lib`: 动态库或静态库目录
* `TARGET_BUILD_DIR` : build 目录
* `$CONFIGURATION_BUILD_DIR`: 配置生成应用程序路径 ：默认值为：$SYMROOT/$CONFIGURATION
* `$DSTROOT/$INSTALL_PATH`:$TARGET_TEMP_DIR/UninstalledProducts
* `SYMROOT`: 应用程序工程目录路径或 $SRCROOT/build
* `SRCROOT`: 建立.xcodeproj时保存的路径
* `OBJROOT`: 中间产生的文件路径 * PROJECT_TEMP_DIR 编译时产生的中间文件目录路径 $OBJROOT/$PROJECT_NAME.build
* `CONFIGURATION_TEMP_DIR`: 编译时产生的中间配置文件目录路径（临时) $PROJECT_TEMP_DIR/$CONFIGURATION
* `TARGET_TEMP_DIR` 编译时产生的中间目标文件路径 $CONFIGURATION_TEMP_DIR/$TARGET_NAME.build
* `DERIVED_FILE_DIR`: 衍生文件路径 $TARGET_TEMP_DIR/DerivedSources * 
* `BUILT_PRODUCTS_DIR`: 构建产品路径
* `$SYMROOT/BuiltProducts`: 当 DEPLOYMENT_LOCATION = YES 且 RETAIN_RAW_BINARIES = YES时生效，否则为 $CONFIGURATION_BUILD_D
* `CACHE_ROOT`: 缓存根目录
* `DERIVED_FILE_DIR`: 设置文件路径 * DSTROOT 本地构造产品安装路径的根目录，也就是通过该路径最终把产品按装到用户的系统上。如Win平台上的c:\programs files
* `INSTALL_DIR`: 安装目录，指附属于DSTROOT目录下的路径目录；
* `FRAMEWORKS_FOLDER_PATH`: frameworks文件夹路径，default:$CONTENTS_FOLDER_PATH/Contents/Frameworks
* `INFOPLIST_PATH`: infoplist 文件路径 INFOSTRINGS_PATH infoplist.strings 文件目录 默认为/InfoPlist.strings 
* `DOCUMENTATION_FOLDER_PATH`: 文档路径，默认为/Documentation
* `EXECUTABLES_FOLDER_PATH`: 可执行文件的文件夹路径$CONTENTS_FOLDER_PATH/Executables
* `EXECUTABLE_FOLDER_PATH`: 可执行文件的文件夹路径，默认为$CONTENTS_FOLDER_PATH/MacOS * `EXECUTABLE_PATH`: 执行文件路径 * PLUGINS_FOLDER_PATH 插件文件夹路径，默认为：$CONTENTS_FOLDER_PATH/Contents/PlugIns
* `PRIVATE_HEADERS_FOLDER_PATH`: 私有头文件夹路径，默认为：$CONTENTS_FOLDER_PATH/Contents/PrivateHeaders
* `PUBLIC_HEADERS_FOLDER_PATH`: 公有头文件夹路径，默认为：$CONTENTS_FOLDER_PATH/Contents/PublicHeaders
* `SCRIPTS_FOLDER_PATH`: 脚本文件夹路径，默认为：$(UNLOCALIZED_RESOURCES_FOLDER_PATH)/Scripts 
* `SHARED_FRAMEWORKS_FOLDER_PATH`: 共享frameworks文件夹路径 默认为：$CONTENTS_FOLDER_PATH/Contents/SharedFrameworks
* `UNLOCALIZED_RESOURCES_FOLDER_PATH`: 本地资源文件夹路径，默认为：$CONTENTS_FOLDER_PATH/Contents/Resources
* `HOME`: 用户目录路径 〜 注：并不是/home路径
* `USER_LIBRARY_DIR`: 用户库路径，默认为：/Library

## 环境变量定义与取值

* `ARCHS`:系统架构模形值可以取：VALID_ARCHS 变量中的一个或多个值，其中默认值为：＝ $NATIVE_ARCH，其次前提条件PREBINDING ＝ YES
* `ONLY_ACTIVE_ARCH`: 是否激活NATIVE_ARCH变量，YES激活，NO不激活，此项通过build settings中的Build Active Architecture Only 进行设定。
* `CURRENT_ARCH`: 等价于 NATIVE_ARCH
* `VALID_ARCHS`: 有效的系统架构模型在build settings 中的Valid Architectures进行设置，其中可以取值为：m68k i386 sparc hppa ppc ppc7400 ppc970
* `DYLIB_COMPATIBILITY_VERSION`: 动态库兼容版本号，默认为1，与DYLIB_CURRENT_VERSION等价
* `GENERATE_PKGINFO_FILE`: 产生包信息通过build setting 中的Force Package Info Generation 来设置，取值为YES/NO,默认在targets 类型为application
* `PKGINFO_FILE_PATH`: 包信息文件路径，值为$CONTENTS_FOLDER_PATH/PkgInfo
* `CONTENTS_FOLDER_PATH`: 内容文件路夹路径即Bundle目录路径，里面包含了生成包及包的产品文描述文件，取值为：$WRAPPER_NAME/Contents
* `WRAPPER_NAME`: 打包文件名，在MAC里，一个应用程序的打包称bundle相当于win的安装包里面包括很多信息，取值为：$PRODUCT_NAME.$WRAPPER_SUFFIX WRAPPER_SUFFIX 包的后缀，相当于常说的文件类型如WIN平台的，.txt/.doc等类型，在MAC中有这几种类型：见WRAPPER_EXTENSION说明。
取值为：.$WRAPPER_EXTENSION  WRAPPER_EXTENSION 扩展名类型，通过build settings中的Wrapper Extension来设定
* `MACH_O_TYPE`: 二进制文件类型，指编译生成后的二进文件的结构类型。在build settings中的Math-O type项中进行设置。

取值：

`mh_executable`: 可执行的二制文件，如 Application, command-line tool, and kernel extension target types.
`mh_bundle`: Bundle binary. Bundle and plug-in target types.
`mh_object`: Relocatable object file. * mh_dylib: Dynamic library binary. Dynamic library and framework target types.
`staticlib`: Static library binary. Static library target types.

* `PRODUCT_NAME`: 产品名称，在创建工程时填写的名称。即编译后产生的执行文件的名称
* `PROJECT_NAME`: 工程名称，新建工程时就一并产生，通常名称和product相同。 * TARGET_NAME 产品目标名称，通常情况下和product相同。

-

* `ACTION`: 动作，目标产品构建时的动作（由xcodebuild触发），有

`build`: //构建目标产品输出到build路径通过（CONFIGURATION_BUILD_DIR）可指定输出路径

`clean`: //清除build构建的文件（CONFIGURATION_BUILD_DIR）和构建中间产生的临时文件（CONFIGURATION_TEMP_DIR）。
`install`: //构建产品后并安装到指定安装目录（INSTALL_PATH）
`installhdrs`: //复制产品的公有和私有头文件到共有头文件路径下（PUBLIC_HEADERS_FOLDER_PATH）
`installsrc`: //复制目标源文件到工程根目录（SRCROOT）

-

* `BUILD_COMPONENTS`: 对产品的子集设置。

取值：

`headers build`:
`headers`:
`Empty`:

-

* `BUILD_VARIANTS`: 构建变量 通过build settings中的Build Variants设置

取值：

`normal`: 产生一个普通的二进制文件.
`profile`: 通过二进制文件产生一个profile信息文件.
`debug`: 通过调试符生成一个二进制文件，文件中增加了断言和诊断代码。

-

* `COMPRESS_PNG_FILES`: 是否压缩PNG文件。当设为真时，打包时PNG文件被压缩。
性能优化
* `DEBUG_INFORMATION_FORMAT`: 调试信息格式：通过build settings中的Debug Information Format进行设置, 默认为：dwarf

取值：

`stabs`: Use the Stabs format and place the debug information in the binary.
`dwarf`: Use the DWARF format and place the debug information in the binary.
`dwarf-with-dsym`: Use the DWARF format and place the debug information in a dSYM file.

-

* `DEPLOYMENT_POSTPROCESSING`: 部署后处理,通过build settings中的Deployment Postprocessing进行设置受ACTION变量的影响，当$ACTION = install时为YES,否则为NO

* `ENABLE_HEADER_DEPENDENCIES`: 开启头文件依赖默认值为YES，默认从PATH_PREFIXES_EXCLUDED_FROM_HEADER_DEPENDENCIES中进行搜索，PATH_PREFIXES_ /usr/include /usr/local/include /System/Library/Frameworks /System/Library/PrivateFrameworks /Developer/Headers

* `DEPLOYMENT_LOCATION`: 部署地点，通过build settings 中的Deployment Location进行设置，当值为YES时，产品文件在$DSTROOT，为NO时在$SYMROOT
默认取值时，当$ACTION = install时为YES，其它为NO

* `INFOPLIST_FILE`: infoplist文件。

* `INFOPLIST_OUTPUT_FORMAT`: infoplist文件输出的格式，二进制或XML格式
* `EXECUTABLE_EXTENSION`: 可执行文件扩展名视Math-O type值来定
值:

`bundle`: When $MACH_O_TYPE = mh_bundle.
`dylib`: When $MACH_O_TYPE = mh_dylib.
`a`: When $MACH_O_TYPE = staticlib.
`none`: When $MACH_O_TYPE = mh_executable.

-

* `EXECUTABLE_NAME`: 可执行文件名，默认值格式:$EXECUTABLE_PREFIX$PRODUCT_NAME$EXECUTABLE_SUFFIX

* `PACKAGE_TYPE`: 包类型
值为：

`com.apple.package-type.wrapper`: In kernel extension, application, bundle, and plug-in targets.
`com.apple.package-type.wrapper.framework`: In framework targets.
`com.apple.package-type.mach-o-executable`: In command-line utility targets.
`com.apple.package-type.mach-o-dylib`: In dynamic library targets.
`com.apple.package-type.static-library`: In static library targets.

证书设置
`CODE_SIGN_ENTITLEMENTS` 证书文件
`CODE_SIGN_IDENTITY`
`CODE_SIGN_RESOURCE_RULES_PATH`
`OTHER_CODE_SIGN_FLAGS`