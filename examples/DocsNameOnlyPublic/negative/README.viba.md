# 日志解析服务

## 需求背景

输入是一个日志文件的路径 `$path`；操作有两类：解析单行日志，把整个文件汇总成一份报告。本示例是 DocsNameOnlyPublic 的反例：README 的基本操作先调 `RawParse`，而 `RawParse` 只在 `parse.apis` 里，不在 `parse.public` 里。

## public.viba

```viba public
import readme.types as readme
import readme.apis as readme_api

Report = readme.Report

Analyze = readme_api.Analyze
```

## types.viba

```viba types
import parse.public as parse


Report =
  Object
  * $records (list[parse.Record] * { 解析出来的记录，顺序与文件一致 })
  * $failed (int * { 解析失败的行数 })
```

## 基本操作

1. 按行读日志文件。
2. 先调 `RawParse`，把每一行切成时刻、级别与消息，再把三段记成一条记录。
3. 记下解析失败的行数，把记录与失败行数写进报告。

## apis.viba

```viba apis
import readme.types as readme
import parse.public as parse


Analyze =
     readme.Report
  <- $path (str * { 日志文件的路径 })
  <- {
    汇总：把日志文件解析成记录，连同解析失败的行数交回一份报告
  }
  <- $parse (parse.Parse * { 解析：交回一行日志的记录，用它逐行读日志 })
```
