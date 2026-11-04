# 任务清单解析

## 需求背景

输入是一份任务清单的路径 `$path`；操作是把清单里的每个任务读出来，记下它的依赖与耗时。`Parse` 只读清单，不排执行顺序。根 README 从这里取 `Task` 与 `Parse`。

## public.viba

```bash public
import parse.types as parse
import parse.apis as parse_api

Task = parse.Task

Parse = parse_api.Parse
```

## types.viba

```bash types
Task =
  Object
  * $name (str * { 任务名，清单里唯一 })
  * $duration (int * { 跑完这个任务要的秒数 })
  * $depends_on (list[str] * { 这个任务依赖的任务名，先跑完它们才轮到这个任务 })
```

## 基本操作

1. 读任务清单。
2. 把每个任务的名称、耗时与依赖记成一条 `Task`。
3. 交回任务列表，顺序与清单一致。

## apis.viba

```bash apis
import parse.types as parse


Parse =
     list[parse.Task]
  <- $path (str * { 任务清单的路径 })
  <- {
    解析：读出清单里的每个任务，带上它的依赖与耗时，交回任务列表
  }
```
