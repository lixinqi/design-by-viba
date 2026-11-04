# 订单记录解析

## 需求背景

输入是一条订单记录的文本 `$record`；操作是把记录解析成一条事件：下单或取消。本示例是 SumWithPayload 正例的依赖方：`Event` 的每个变体都带载荷，订单号就在载荷里。根 README 从这里取 `Event` 与 `Parse`。

## public.viba

```bash public
import parse.types as parse
import parse.apis as parse_api

Event = parse.Event

Parse = parse_api.Parse
```

## types.viba

```bash types
Event =
  Oneof
  | $placed (Placed * { 下单 })
  | $cancelled (Cancelled * { 取消 })

Placed =
  Object
  * $order_no (str * { 下单的订单号 })
  * $placed_at (str * { 下单的时间 })

Cancelled =
  Object
  * $order_no (str * { 取消的订单号 })
  * $cancel_reason (str * { 取消的原因 })
```

## 基本操作

1. 从记录里读出事件名。
2. 从记录里读出订单号。
3. 下单时记下订单时间，取消时记下取消原因。

## apis.viba

```bash apis
import parse.types as parse


Parse =
     parse.Event
  <- $record (str * { 一条订单记录的文本 })
  <- {
    解析：从记录里读出事件名与订单号，交回一条事件
  }
```
