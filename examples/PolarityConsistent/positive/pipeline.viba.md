# 发布流水线

## 需求背景

输入是源码目录的路径 `$source`；操作是跑发布流水线：构建与测试分别跑一遍，交回没有通过的检查清单。本示例是 PolarityConsistent 正例的依赖方：`Failure` 与它的两个变体 `$build_failed`、`$test_failed` 都是负面名，指的是没有通过的检查。根 README 从这里取 `Failure` 与 `Run`。

## public.viba

```bash public
import pipeline.types as pipeline
import pipeline.apis as pipeline_api

Failure = pipeline.Failure

Run = pipeline_api.Run
```

## types.viba

```bash types
BuildFailure =
  Object
  * $log (str * { 构建的完整日志 })

TestFailure =
  Object
  * $test (str * { 第一个没有通过的测试名 })
  * $log (str * { 该测试的完整日志 })

Failure =
  Oneof
  | $build_failed (BuildFailure * { 构建没有通过 })
  | $test_failed (TestFailure * { 测试没有通过 })
```

## 基本操作

1. 在源码目录里构建。
2. 构建没有通过，就把构建失败的日志记成 `$build_failed`。
3. 在源码目录里跑测试。
4. 测试没有通过，就把第一个没有通过的测试名与日志记成 `$test_failed`。
5. 把两项检查查出的失败列成清单交回；都通过时清单为空。

## apis.viba

```bash apis
import pipeline.types as pipeline

Run =
     list[pipeline.Failure]
  <- $source (str * { 源码目录的路径 })
  <- {
    跑检查：构建与测试分别跑一遍，交回没有通过的检查清单；空列表表示都通过
  }
```
