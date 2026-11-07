# 发布前检查

## 需求背景

输入是待发布产物目录的路径 `$dist`；操作只有一类：对产物目录跑一遍发布前检查，交回一份报告。根 README 从这里取 `Report` 与 `Run`。

## public.viba

```viba public
import audit.types as audit
import audit.apis as audit_api

Report = audit.Report

Run = audit_api.Run
```

## types.viba

```viba types
Report =
  Object
  * $command (str * { 跑过的检查命令，逐字记下 })
  * $output (str * { 命令的输出，逐字记下 })
  * $passed (bool * { 全部检查项通过为真 })
```

## 基本操作

1. 读产物目录里的文件。
2. 跑一遍检查命令，把命令与它的输出逐字记下。
3. 按输出逐项判断是否通过，全部通过时 `$passed` 为真。
4. 把命令、输出与判定记成一份 `Report`，交回它。

## apis.viba

```viba apis
import audit.types as audit


Run =
     audit.Report
  <- $dist (str * { 待发布产物目录的路径 })
  <- {
    检查：跑一遍发布前检查，交回检查命令、输出与判定
  }
```
