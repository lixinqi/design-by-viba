# 版本发布

## 需求背景

输入是一个版本号 `$version` 与待发布产物目录的路径 `$dist`；操作类别有两类：跑发布前检查，把产物发布并推送。本示例是 VerifiedBeforeDone 的正例：`Release` 依赖 `audit.Run`，判定里带 `$passed`，为真才推送，完成时附上检查命令与输出。

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
import audit.public as audit


Release =
     readme.Publication
  <- $version (str * { 要发布的版本号 })
  <- $dist (str * { 待发布产物目录的路径 })
  <- {
    发布：先跑发布前检查，`$passed` 为真才把产物推送到发布仓库，交回发布记录
  }
  <- $audit (audit.Run * { 检查：交回检查命令、输出与 `$passed`，用它决定推不推送 })
```
