# 收款服务

## 需求背景

输入是一条收款请求的文本 `$request` 与这次收款的金额 `$amount`；操作有两类：把请求解析成这次收款用的支付方式，按支付方式扣款并交回一张收款回执。本示例是 VariantTypeFormConsistent 的反例：`PaymentMethod` 的三个变体的标签 `card`、`wallet`、`bank_transfer` 仍是支付方式的术语，`card` 后面的类型名却是问题描述 `CardDeclined`，与标签不是同一个术语。

## public.viba

```viba public
import readme.types as readme
import readme.apis as readme_api

Receipt = readme.Receipt

Charge = readme_api.Charge
```

## types.viba

```viba types
import parse.public as parse


Receipt =
  Object
  * $method (parse.PaymentMethod * { 这次收款用的支付方式 })
  * $amount (int * { 这次收款的金额，以分为单位 })
  * $paid (bool * { 是否扣款成功 })
```

## 基本操作

1. 收下一条收款请求的文本与这次收款的金额。
2. 把请求交给 `Parse`，取回这次收款用的支付方式。
3. 按支付方式扣款，把支付方式、金额与扣款结果记成一张收款回执。

## apis.viba

```viba apis
import readme.types as readme
import parse.public as parse


Charge =
     readme.Receipt
  <- $request (str * { 一条收款请求的文本 })
  <- $amount (int * { 这次收款的金额，以分为单位 })
  <- {
    扣款：把请求解析成这次收款用的支付方式，按支付方式从付款方扣款，交回一张收款回执
  }
  <- $parse (parse.Parse * { 解析：交回这次收款用的支付方式，用它扣款并填回执 })
```
