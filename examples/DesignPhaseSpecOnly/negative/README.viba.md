# 任务调度器

## 需求背景

输入是一份任务清单的路径 `$path`；操作类别有两类：解析任务清单，把任务排成执行顺序。本示例是 DesignPhaseSpecOnly 的反例：仓库根目录留着 `scheduler.py`，把 `Schedule` 实现出来了；从 public 出发没有一条边能到这份文件，设计阶段没有删掉它。

## public.viba

```viba public
import readme.types as readme
import readme.apis as readme_api

Plan = readme.Plan

Schedule = readme_api.Schedule
```

## types.viba

```viba types
import parse.public as parse


Plan =
  Object
  * $order (list[parse.Task] * { 排好的任务，按执行顺序 })
  * $finish_seconds (int * { 全部任务跑完的耗时，单位秒 })
```

## 基本操作

1. 收下任务清单的路径。
2. 把路径交给 `Parse`，取回清单里的每个任务，带上它的依赖与耗时。
3. 按依赖关系排出执行顺序：一个任务排在它依赖的任务之后。
4. 从排好的顺序算出全部任务跑完的耗时。
5. 交回顺序与耗时。

## apis.viba

```viba apis
import readme.types as readme
import parse.public as parse


Schedule =
     readme.Plan
  <- $path (str * { 任务清单的路径 })
  <- {
    排程：按依赖关系排出执行顺序并算出全部任务跑完的耗时，交回排好的顺序与耗时
  }
  <- $parse (parse.Parse * { 解析：交回任务清单里的每个任务，带上它的依赖与耗时，用它排顺序 })
```
