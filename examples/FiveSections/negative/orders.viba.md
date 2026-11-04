# 订单登记

## 需求背景

输入是一张订单草稿 `$draft`，里面有顾客编号与商品行；操作类别是下单：给订单草稿分配编号，写进订单簿，交回带编号的订单。本示例是 FiveSections 反例的模块：缺 `## 基本操作` 一节。根 README 从这里取 `Line`、`Draft`、`Order` 与 `Place`。

## public.viba

```bash public
import orders.types as orders
import orders.apis as orders_api

Line = orders.Line

Draft = orders.Draft

Order = orders.Order

Place = orders_api.Place
```

## types.viba

```bash types
Line =
  Object
  * $sku (str * { 商品编号 })
  * $quantity (int * { 数量，至少是 1 })

Draft =
  Object
  * $customer (str * { 顾客编号 })
  * $lines (list[Line] * { 顾客要的商品行 })

Order =
  Object
  * $id (str * { 订单编号，下单时分配 })
  * $customer (str * { 顾客编号 })
  * $lines (list[Line] * { 订单里的商品行 })
```

## apis.viba

```bash apis
import orders.types as orders


Place =
     orders.Order
  <- $draft (orders.Draft * { 顾客编号与商品行都已填好的订单草稿 })
  <- {
    下单：给订单草稿分配编号，写进订单簿，交回带编号的订单
  }
```
