# 任务登记与推进

## 需求背景

输入是一个任务的名字 `$name`，以及任务的当前状态；操作有两类：登记一个任务，按当前状态推进一个任务。本示例是 NoRecordPlusKind 反例的任务模块：`Task` 的状态写成 `$kind` 字段加一个纯字符串枚举 `Kind`。根 README 从这里取 `Task`、`Register` 与 `Advance`。

## public.viba

```bash public
import task.types as task
import task.apis as task_api

Task = task.Task

Register = task_api.Register

Advance = task_api.Advance
```

## types.viba

```bash types
Task =
  Object
  * $name (str * { 任务的名字 })
  * $kind (Kind * { 任务当前处在哪一种情况 })
  * $detail (str * { 这一种情况附带的说明：还没开始时是登记的时刻，已经开始时是执行者的账号，正常结束时是结果，中途失败时是原因 })

Kind =
  Oneof
  | "waiting"
  | "running"
  | "done"
  | "failed"
```

## 基本操作

1. 按名字建一个任务，状态记成还没开始。
2. 取任务当前的状态，算出下一步。
3. 把状态换掉，交回推进后的任务。

## apis.viba

```bash apis
import task.types as task

Register =
     task.Task
  <- $name (str * { 任务的名字 })
  <- {
    登记：按名字建一个还没开始的任务，交回这个任务
  }

Advance =
     task.Task
  <- $task (task.Task * { 要推进的任务 })
  <- {
    推进：按任务当前的状态算出下一步，交回推进后的任务
  }
```
