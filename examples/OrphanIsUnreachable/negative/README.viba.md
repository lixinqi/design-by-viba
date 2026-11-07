# 日志写入

## 需求背景

输入是一个日志目录的路径 `$dir`；操作类别是写入：把目录里每个日志文件逐行解析，按读到的顺序写成一条日志，交回这条日志。本示例是 OrphanIsUnreachable 的反例：`Draft` 表示一条还没定稿的日志条目，没有写进 `readme.public`，也没有被任何字段或操作引用，README 的基本操作却说它是设计的一部分，先留着。

## public.viba

```viba public
import readme.types as readme
import readme.apis as readme_api

Log = readme.Log

Write = readme_api.Write
```

## types.viba

```viba types
import parse.public as parse


Entry =
  Object
  * $source (str * { 这一行来自哪个日志文件 })
  * $line (parse.Line * { 这一行的时刻、级别与正文 })

Log =
  Object
  * $entries (list[Entry] * { 写进这条日志的条目，按写入顺序 })

Draft =
  Object
  * $text (str * { 还没定稿的日志正文 })
  * $author (str * { 写下这条草稿的人 })
```

## 基本操作

1. 读出目录里的每个日志文件，把每一行交给 `Parse`，收下它交回的行。
2. 记下这一行来自哪个文件，把它与这一行一起记成一条日志条目。
3. 把全部日志条目按读到的顺序排好，交回这条日志。

`Draft` 是设计的一部分，先留着。

## apis.viba

```viba apis
import readme.types as readme
import parse.public as parse


Write =
     readme.Log
  <- $dir (str * { 日志文件所在目录的路径 })
  <- {
    写入：把目录里每个日志文件逐行解析，按读到的顺序写成一条日志，交回这条日志
  }
  <- $parse (parse.Parse * { 解析：交回一行原文的时刻、级别与正文，用它组成一条日志条目 })
```
