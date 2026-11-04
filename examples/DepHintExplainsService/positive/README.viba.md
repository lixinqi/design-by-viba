# 分组报表

## 需求背景

输入是明细行的清单 `$rows`；操作有两类：按分组汇总金额，把明细排成一张分组合计的报表。本示例是 DepHintExplainsService 的正例：`Report` 依赖 `Sum`，依赖提示写清 `Sum` 交回什么、`Report` 拿它做什么。

## public.viba

```bash public
import readme.types as readme
import readme.apis as readme_api

Sheet = readme.Sheet

Report = readme_api.Report
```

## types.viba

```bash types
Sheet =
  Object
  * $header (list[str] * { 表头行：每个分组名后面跟着这一组的合计 })
  * $lines (list[str] * { 明细行：分组名与金额，按分组排好 })
```

## 基本操作

1. 把明细行交给 `Sum`，拿到每个分组的合计。
2. 用合计写表头：每个分组一项，写成分组名与合计。
3. 把明细行按分组排好，接在表头下面，交回表头与明细行。

## apis.viba

```bash apis
import readme.types as readme
import sum.public as sum


Report =
     readme.Sheet
  <- $rows (list[sum.Row] * { 要写进报表的明细行 })
  <- {
    生成：把明细按分组排成一张报表，交回表头与明细行
  }
  <- $sum (sum.Sum * { 汇总：交回各分组的合计，用它写表头 })
```
