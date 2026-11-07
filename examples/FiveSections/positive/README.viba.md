# 收银台下单

## 需求背景

输入是购物车 `$cart`，里面有顾客编号与商品行；操作类别是下单：把购物车写成一张订单，交给订单簿，交回带编号的订单。本示例是 FiveSections 的正例：README 与 orders 两篇都写全 需求背景、public、types、基本操作、apis 五节，顺序一致。

## public.viba

```viba public
import readme.types as readme
import readme.apis as readme_api

Cart = readme.Cart

Checkout = readme_api.Checkout
```

## types.viba

```viba types
import orders.public as orders


Cart =
  Object
  * $customer (str * { 顾客编号 })
  * $lines (list[orders.Line] * { 购物车里的商品行，每行是商品编号与数量 })
```

## 基本操作

1. 把顾客编号与购物车里的商品行组成一张 `Cart`。
2. 从 `Cart` 写出一张订单草稿。
3. 把订单草稿交给 `Place`。
4. 取回带编号的订单，作为下单结果。

## apis.viba

```viba apis
import readme.types as readme
import orders.public as orders


Checkout =
     orders.Order
  <- $cart (readme.Cart * { 顾客编号与购物车里的商品行 })
  <- {
    下单：把购物车写成订单草稿，交给订单簿，交回带编号的订单
  }
  <- $place (orders.Place * { 下单：把订单草稿写进订单簿并分配编号，交回带编号的订单，用它作为下单结果 })
```
