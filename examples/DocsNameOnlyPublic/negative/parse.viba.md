# 日志行解析

## 需求背景

输入是一行日志的文本 `$line`；操作是解析：把这一行读成时刻、级别与消息，交回一条记录。根 README 从这里取 `Record` 与 `Parse`。

## public.viba

```viba public
import parse.types as parse
import parse.apis as parse_api

Record = parse.Record

Parse = parse_api.Parse
```

## types.viba

```viba types
Record =
  Object
  * $time (str * { 日志行的时刻，按原写法保留 })
  * $level (str * { 日志级别，如 INFO 或 ERROR })
  * $message (str * { 时刻与级别之后的消息 })
```

## 基本操作

1. 读入一行日志。
2. 读出时刻、级别与消息。
3. 把三者记成一条记录。

## apis.viba

```viba apis
import parse.types as parse


RawParse =
     list[str]
  <- $line (str * { 一行日志 })
  <- {
    切分：把一行日志按空白切成时刻、级别与消息
  }

Parse =
     parse.Record
  <- $line (str * { 一行日志 })
  <- {
    解析：读出时刻、级别与消息，交回一条记录
  }
```
