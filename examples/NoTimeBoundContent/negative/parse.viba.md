# 任务描述解析

## 需求背景

输入是一条任务描述 `$text`，里面有任务名、优先级与依赖的任务名；操作只有一类：把这三项读出来，交回一个任务。`Parse` 只负责解析，不知道任务如何排序。根 README 从这里取 `Parse`。

## public.viba

```bash public
import parse.types as parse
import parse.apis as parse_api

Job = parse.Job

Parse = parse_api.Parse
```

## types.viba

```bash types
Job =
  Object
  * $name (str * { 任务名，在一批任务里唯一 })
  * $priority (int * { 任务的优先级，数值越小越先执行 })
  * $depends_on (list[str] * { 必须先完成的任务名，按声明顺序 })
```

## 基本操作

1. 读描述文本。
2. 把第一个词记成任务名。
3. 把第二个词按整数读成优先级。
4. 其余的词记成依赖的任务名，按出现顺序保留。

## apis.viba

```bash apis
import parse.types as parse


Parse =
     parse.Job
  <- $text (str * { 一条任务描述，任务名、优先级与依赖的任务名用空白分开 })
  <- {
    解析：读出一条任务描述的任务名、优先级与依赖，交回一个任务
  }
```
