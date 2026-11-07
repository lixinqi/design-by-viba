# 分组日报

## 需求背景

输入是明细行的清单 `$rows`；操作有两类：按分组汇总金额，把明细排成一份表头带合计的日报。本示例是 HintAddsInformation 的反例：`Report` 的依赖提示写成“汇总：汇总各分组”，只把 `Sum` 的名字换了个说法；删掉这条提示，`$sum` 这个参数还是只有名字。

## public.viba

```viba public
import readme.types as readme
import readme.apis as readme_api

Sheet = readme.Sheet

Report = readme_api.Report
```

## types.viba

```viba types
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

```viba apis
import readme.types as readme
import sum.public as sum


Report =
     readme.Sheet
  <- $rows (list[sum.Row] * { 要写进日报的明细行，顺序不限 })
  <- {
    生成：把明细按分组排成一份日报，交回表头与明细行
  }
  <- $sum (sum.Sum * { 汇总：汇总各分组 })
```
