# 日志写入

## 需求背景

输入是一个日志目录的路径 `$dir`；操作类别是写入：把目录里每个日志文件逐行解析，按读到的顺序写成一条日志，交回这条日志。本示例是 OrphanIsUnreachable 的正例：`Entry` 表示一条日志条目，没有写进 `readme.public`，但被 `Log.$entries` 引用，从根 public 出发做可达性检查能走到它，所以保留。

## public.viba

```bash public
import readme.types as readme
import readme.apis as readme_api

Log = readme.Log

Write = readme_api.Write
```

## types.viba

```bash types
import parse.public as parse


Entry =
  Object
  * $source (str * { 这一行来自哪个日志文件 })
  * $line (parse.Line * { 这一行的时刻、级别与正文 })

Log =
  Object
  * $entries (list[Entry] * { 写进这条日志的条目，按写入顺序 })
```

## 基本操作

1. 读出目录里的每个日志文件，把每一行交给 `Parse`，收下它交回的行。
2. 记下这一行来自哪个文件，把它与这一行一起记成一条日志条目。
3. 把全部日志条目按读到的顺序排好，交回这条日志。

## apis.viba

```bash apis
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
