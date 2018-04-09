
---
title: iOS App重签名方法及例子
subtitle: iOSRCS
date: 2017-01-10 03:52:00
tags: iOS逆向
categories: iOS
---

<!--# iOS App重签名方法及例子-->

(1)解压qq.ipa 找到Payload文件

> unzip qq.ipa //命令行解压

(2)将Payload目录中的_CodeSignature文件删除
> rm -rf Payload/*.app/_CodeSignature/

(3）将自己app打包导出ipa文件 解压后找到 embedded.mobileprovision 文件 并替换qq.ipa中的embedded.mobileprovision 文件

> cp embedded.mobileprovision Payload/*.app/embedded.mobileprovision

检查:
> security cms -D -i example.mobileprovision

（4)重新签名，“iPhone Distribution: XXXXXX”这个指的是自己的embedded.mobileprovision文件用到的签名证书名称，在xcode或钥匙串中可以找到

> /usr/bin/codesign -f -s "iPhone Distribution: XXXXXX" --resource-rules Payload/*.app/ResourceRules.plist Payload/*.app/
> /usr/bin/codesign -f -s "iPhone Developer: xxxxxx(2F4935C2YD)" --entitlements entitlements.plist Payload/*.app/

没有文件entitlements.plist:

> security cms -D -i 你要签名的mobileprovision路径 \> t_entitlements_full.plist
> /usr/libexec/PlistBuddy -x -c 'Print:Entitlements' t_entitlements_full.plist \> t_entitlements.plist
最终得到 t_entitlements.plist 即是需要的plist

检查App:
> codesign -d --entitlements - Example.app


(5)重新打包

> zip -r qq.ipa Payload



### 显示签名
> security find-identity -v -p codesigning    


【需要cd到Payload文件下，才可以生成】
/usr/libexec/PlistBuddy -x -c "print :Entitlements " /dev/stdin \<\<\< $(security cms -D -i production.app/embedded.mobileprovision) \> Entitlements.plist
/usr/libexec/PlistBuddy -c 'Set :get-task-allow true' Entitlements.plist

/usr/libexec/PlistBuddy -x -c "print :Entitlements " /dev/stdin \<\<\< $(security cms -D -i WeChat.app/embedded.mobileprovision) \> Entitlements.plist


把ipa包内的PlugIns和Watch文件夹删了，重新签名就可以了。

extension可以全部删掉