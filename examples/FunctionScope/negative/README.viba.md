# 报表导出

## 需求背景

输入是报表的标题 `$title` 与明细行的清单 `$rows`；操作只有一类：把明细行拼成正文，连同标题交回一份可以导出的报表。本示例是 FunctionScope 的反例：`Join` 多收一个 `$is_last (bool)`，哪一行是末项由 `Join` 的调用方按位置判断，`Join` 不再自己决定。

## public.viba

```viba public
import readme.types as readme
import readme.apis as readme_api

Report = readme.Report

Export = readme_api.Export
```

## types.viba

```viba types
Report =
  Object
  * $title (str * { 报表的标题，写在正文上方 })
  * $body (str * { 明细行拼成的正文 })
```

## 基本操作

1. 收下报表的标题与明细行。
2. 按导出顺序逐行交给 `Join`；`Join` 的调用方自己看这一行是不是最后一行，把判断结果当 `$is_last` 传进去。
3. 把 `Join` 交回的每一段按顺序接成正文，连同标题记成 `Report` 交回。

## apis.viba

```viba apis
import readme.types as readme
import join.public as join


Export =
     readme.Report
  <- $title (str * { 报表的标题 })
  <- $rows (list[join.Row] * { 报表的明细行，按导出顺序排列 })
  <- {
    导出：逐行拼成正文，连同标题交回一份报表
  }
  <- $join (join.Join * { 拼接：交回一行拼好的一段；`Join` 的调用方按位置传 `$is_last`，再用它拼出正文 })
```
