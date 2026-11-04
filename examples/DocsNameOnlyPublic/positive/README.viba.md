# 日志解析服务

## 需求背景

输入是一个日志文件的路径 `$path`；操作有两类：解析单行日志，把整个文件汇总成一份报告。本示例是 DocsNameOnlyPublic 的正例：README 的正文只提解析文档 public 里的 `Parse`，解析文档的内部操作一概不提。

## public.viba

```bash public
import readme.types as readme
import readme.apis as readme_api

Report = readme.Report

Analyze = readme_api.Analyze
```

## types.viba

```bash types
import parse.public as parse


Report =
  Object
  * $records (list[parse.Record] * { 解析出来的记录，顺序与文件一致 })
  * $failed (int * { 解析失败的行数 })
```

## 基本操作

1. 按行读日志文件。
2. 把每一行交给 `Parse`，收下它交回的一条记录。
3. 记下解析失败的行数，把记录与失败行数写进报告。

## apis.viba

```bash apis
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
