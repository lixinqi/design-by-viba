# 日志行解析

## 需求背景

输入是一行日志的原文 `$line`；操作类别是解析：把这一行拆成时刻、级别与正文，交回一个 `Line`。根 README 从这里取 `Line` 与 `Parse`。

## public.viba

```viba public
import parse.types as parse
import parse.apis as parse_api

Line = parse.Line

Parse = parse_api.Parse
```

## types.viba

```viba types
Line =
  Object
  * $at (int * { 这一行写下的时刻，Unix 秒 })
  * $level (str * { 日志级别：info、warn、error })
  * $message (str * { 这一行的正文 })
```

## 基本操作

1. 读入一行日志的原文。
2. 把开头的时刻与级别拆出来。
3. 其余内容记成正文，交回这一行的时刻、级别与正文。

## apis.viba

```viba apis
import parse.types as parse


Parse =
     parse.Line
  <- $line (str * { 一行日志的原文 })
  <- {
    解析：把一行原文拆成时刻、级别与正文，交回这一行日志的内容
  }
```
