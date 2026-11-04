# 报表导出

## 需求背景

输入是报表的标题 `$title` 与明细行的清单 `$rows`；操作只有一类：把明细行拼成正文，连同标题交回一份可以导出的报表。本示例是 FunctionScope 的正例：`Join` 自己决定行与行之间的分隔符，也自己判断哪一行是末项。

## public.viba

```bash public
import readme.types as readme
import readme.apis as readme_api

Report = readme.Report

Export = readme_api.Export
```

## types.viba

```bash types
Report =
  Object
  * $title (str * { 报表的标题，写在正文上方 })
  * $body (str * { 明细行拼成的正文 })
```

## 基本操作

1. 收下报表的标题与明细行。
2. 把明细行整份交给 `Join`，拼成正文；分隔符与末项都由 `Join` 决定。
3. 把标题与正文记成 `Report` 交回。

## apis.viba

```bash apis
import readme.types as readme
import join.public as join


Export =
     readme.Report
  <- $title (str * { 报表的标题 })
  <- $rows (list[join.Row] * { 报表的明细行，按导出顺序排列 })
  <- {
    导出：把明细行拼成正文，连同标题交回一份报表
  }
  <- $join (join.Join * { 拼接：交回拼好的报表正文，用它和标题一起组成报表 })
```
