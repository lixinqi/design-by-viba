# 分组合计

## 需求背景

输入是明细行的清单 `$rows`；操作只有一类：按分组累加金额，交回每个分组的合计。根 README 从这里取 `Sum`。

## public.viba

```bash public
import sum.types as sum
import sum.apis as sum_api

Row = sum.Row

GroupTotal = sum.GroupTotal

Sum = sum_api.Sum
```

## types.viba

```bash types
Row =
  Object
  * $group (str * { 分组名 })
  * $amount (int * { 这一行的金额，单位元 })

GroupTotal =
  Object
  * $group (str * { 分组名 })
  * $total (int * { 这一组的金额合计，单位元 })
```

## 基本操作

1. 逐行取分组名与金额。
2. 同一分组累加金额。
3. 每个分组交回一条合计。

## apis.viba

```bash apis
import sum.types as sum


Sum =
     list[sum.GroupTotal]
  <- $rows (list[sum.Row] * { 要汇总的明细行 })
  <- {
    汇总：按分组累加金额，交回每个分组的合计
  }
```
