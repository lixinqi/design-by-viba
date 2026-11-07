# 事件解析

## 需求背景

输入是一个事件文件的路径 `$path`；操作是解析，把文件里的每一行读成一条事件。根 README 从这里取 `Event` 与 `Parse`。

## public.viba

```viba public
import parse.types as parse
import parse.apis as parse_api

Event = parse.Event

Parse = parse_api.Parse
```

## types.viba

```viba types
Event =
  Object
  * $metric (str * { 指标名 })
  * $value (float * { 一条事件的数值 })
  * $at (int * { 事件发生的时间，Unix 秒 })
```

## 基本操作

1. 打开事件文件。
2. 把每一行按制表符拆成指标名、数值、时间。
3. 按行序交回事件清单。

## apis.viba

```viba apis
import parse.types as parse


Parse =
     list[parse.Event]
  <- $path (str * { 事件文件的路径 })
  <- {
    解析：把文件里的每一行读成一条事件，交回这个文件的事件清单
  }
```
