# 任务调度器

## 需求背景

输入是一批任务描述 `$descriptions`，每条描述带任务名、优先级与依赖的任务名；操作有两类：解析单条任务描述，把整批任务排成一份执行计划。本示例是 NoTimeBoundContent 的反例：`Schedule` 的基本操作没有写明适用条件。

## public.viba

```bash public
import readme.types as readme
import readme.apis as readme_api

Plan = readme.Plan

Schedule = readme_api.Schedule
```

## types.viba

```bash types
import parse.public as parse


Plan =
  Object
  * $order (list[parse.Job] * { 排进执行计划的任务，按执行顺序排列 })
  * $deferred (list[parse.Job] * { 依赖没满足、没排进执行计划的任务，按输入顺序排列 })
```

## 基本操作

1. 把每条任务描述交给 `Parse`。
2. 按优先级与依赖排好执行顺序；依赖没满足的任务记进 `$deferred`。
3. 本次先不做重试，下次再说。

## apis.viba

```bash apis
import readme.types as readme
import parse.public as parse


Schedule =
     readme.Plan
  <- $descriptions (list[str] * { 一批任务描述，每条描述一行 })
  <- {
    调度：把每条描述解析成任务，按优先级与依赖排好执行顺序，交回执行计划
  }
  <- $parse (parse.Parse * { 解析：交回一条任务描述的任务名、优先级与依赖，用它排执行顺序 })
```
