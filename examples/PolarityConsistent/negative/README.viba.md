# 发布前检查

## 需求背景

输入是版本号 `$version` 与源码目录的路径 `$source`；操作有两类：跑发布流水线里的构建与测试，把没有通过的检查记成发布的阻塞项。本示例是 PolarityConsistent 的反例：`Success` 是正面名，它的两个变体 `$build_failed`、`$test_failed` 都是负面名，类型名与变体名冲突。

## public.viba

```bash public
import readme.types as readme
import readme.apis as readme_api

Release = readme.Release

Prepare = readme_api.Prepare
```

## types.viba

```bash types
import pipeline.public as pipeline

Release =
  Object
  * $version (str * { 待发布的版本号 })
  * $blockers (list[pipeline.Success] * { 发布前查出的阻塞项；空列表表示构建与测试都通过 })
```

## 基本操作

1. 收下版本号与源码目录的路径。
2. 把源码目录的路径交给 `Run`，取回没有通过的检查清单。
3. 把版本号与清单里的每一项记成一份 `Release`；清单为空时 `$blockers` 为空列表，表示可以发布。

## apis.viba

```bash apis
import readme.types as readme
import pipeline.public as pipeline

Prepare =
     readme.Release
  <- $version (str * { 待发布的版本号 })
  <- $source (str * { 源码目录的路径 })
  <- {
    准备：跑一遍发布前检查，把没有通过的检查记成发布的阻塞项
  }
  <- $check (pipeline.Run * { 跑检查：交回没有通过的检查清单，用它填发布阻塞项 })
```
