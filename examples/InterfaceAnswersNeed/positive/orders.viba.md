# 订单明细

## 需求背景

输入是一个订单明细 CSV 文件的路径 `$path`；操作只有一类：把每个订单行读成区域与金额。本示例是 InterfaceAnswersNeed 正例的依赖方：`Load` 只负责读行，按区域汇总由根 README 的 `Report` 完成。根 README 从这里取 `Load`。

## public.viba

```viba public
import orders.types as orders
import orders.apis as orders_api

Order = orders.Order

Load = orders_api.Load
```

## types.viba

```viba types
Order =
  Object
  * $region (str * { 订单行上写的区域名 })
  * $amount (int * { 这一行的订单金额，单位元 })
```

## 基本操作

1. 打开 CSV 文件。
2. 每行取区域名与金额。
3. 按行序交回订单行的清单。

## apis.viba

```viba apis
import orders.types as orders


Load =
     list[orders.Order]
  <- $path (str * { 订单明细 CSV 文件的路径 })
  <- {
    读取：把文件里的每个订单行读成区域与金额，交回订单行的清单
  }
```
