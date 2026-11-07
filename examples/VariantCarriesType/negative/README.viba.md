# 订单事件处理

## 需求背景

输入是一条订单记录的文本 `$record`；操作有两类：把记录解析成一条事件，按事件推进订单。本示例是 VariantCarriesType 的反例：`Event` 的变体只有标签、后面没有类型，推进订单时仍要从事件里取订单号。

## public.viba

```viba public
import readme.types as readme
import readme.apis as readme_api

Order = readme.Order

Advance = readme_api.Advance
```

## types.viba

```viba types
import parse.public as parse


Order =
  Object
  * $order_no (str * { 订单号 })
  * $event (parse.Event * { 推进订单的那条事件 })
```

## 基本操作

1. 把记录交给 `Parse`，取回一条事件。
2. 从事件带的类型里取订单号。
3. 把订单号与事件记成一份订单。

## apis.viba

```viba apis
import readme.types as readme
import parse.public as parse


Advance =
     readme.Order
  <- $record (str * { 一条订单记录的文本 })
  <- {
    推进：把记录解析成一条事件，从事件带的类型里取订单号，连同事件记成一份订单
  }
  <- $parse (parse.Parse * { 解析：交回一条事件，用它推进订单 })
```
