# 任务登记与推进

## 需求背景

输入是一个任务的名字 `$name`，以及任务的当前状态；操作有两类：登记一个任务，按当前状态推进一个任务。本示例是 NoRecordPlusKind 正例的任务模块：`Task` 的状态写成和类型，每个变体带着自己的类型，每一种情况只带它自己的数据。根 README 从这里取 `Task`、`Register` 与 `Advance`。

## public.viba

```viba public
import task.types as task
import task.apis as task_api

Task = task.Task

Register = task_api.Register

Advance = task_api.Advance
```

## types.viba

```viba types
Task =
  Object
  * $name (str * { 任务的名字 })
  * $state (TaskState * { 任务当前处在哪一种情况 })

TaskState =
  Oneof
  | $waiting ($registered_at str * { 还没开始，带登记的时刻 })
  | $running ($executor str * { 已经开始，带执行者的账号 })
  | $done ($result str * { 正常结束，带任务交回的结果 })
  | $failed ($reason str * { 中途失败，带失败的原因 })
```

## 基本操作

1. 按名字建一个任务，状态记成还没开始。
2. 取任务当前的状态，算出下一步。
3. 把状态换掉，交回推进后的任务。

## apis.viba

```viba apis
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
