# 版本发布

## 需求背景

输入是一个版本号 `$version` 与待发布产物目录的路径 `$dist`；操作类别有两类：跑发布前检查，把产物发布并推送。发布已完成并推送。本示例是 VerifiedBeforeDone 的反例：`Release` 不依赖 `audit.Run`，判定里没有 `$passed`，完成时没有附检查命令与输出。

## public.viba

```viba public
import readme.types as readme
import readme.apis as readme_api

Publication = readme.Publication

Release = readme_api.Release
```

## types.viba

```viba types
import audit.public as audit


Publication =
  Object
  * $version (str * { 发布出去的版本号 })
  * $report (audit.Report * { 发布前检查的报告，推送的依据 })
```

## 基本操作

1. 把产物目录交给 `audit.Run`，跑一遍发布前检查，拿回报告。
2. 报告里 `$passed` 为假就停下：不推送，也不交回发布记录。
3. `$passed` 为真就把产物推送到发布仓库。
4. 把版本号与这份报告记成一条 `Publication`，交回它；检查命令与输出随报告一起留档。

## apis.viba

```viba apis
import readme.types as readme


Release =
     readme.Publication
  <- $version (str * { 要发布的版本号 })
  <- $dist (str * { 待发布产物目录的路径 })
  <- {
    发布：把产物推送到发布仓库，交回发布记录
  }
```
