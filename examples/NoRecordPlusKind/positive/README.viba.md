# 任务队列

## 需求背景

输入是一批任务的名字 `$names`；操作有两类：登记单个任务，把整批任务登记后推进一次。本示例是 NoRecordPlusKind 的正例：`Task` 的状态写成带载荷的和类型，每一种情况只带它自己的数据。

## public.viba

```bash public
import readme.types as readme
import readme.apis as readme_api

Queue = readme.Queue

Schedule = readme_api.Schedule
```

## types.viba

```bash types
import task.public as task

Queue =
  Object
  * $tasks (list[task.Task] * { 按登记顺序排好的任务 })
```

## 基本操作

1. 按名字逐个登记任务，交给 `Register`。
2. 把每个任务交给 `Advance`，拿回推进后的任务。
3. 按登记顺序把任务排成队列，交回。

## apis.viba

```bash apis
import readme.types as readme
import task.public as task

Schedule =
     readme.Queue
  <- $names (list[str] * { 要登记的任务名字，按登记顺序排 })
  <- {
    排程：按名字登记整批任务，把每个任务推进一次，按登记顺序交回整批任务
  }
  <- $register (task.Register * { 登记：按名字交回一个还没开始的任务，用它把每个名字变成任务 })
  <- $advance (task.Advance * { 推进：按任务当前的状态交回推进后的任务，用它把任务就地换掉 })
```
