# 收款请求解析

## 需求背景

输入是一条收款请求的文本 `$request`；操作是把请求解析成这次收款用的支付方式：银行卡、钱包或银行转账。`Parse` 只负责解析请求，不知道扣款如何完成。本示例是 PayloadFormConsistent 正例的依赖方：`PaymentMethod` 的三个变体都带载荷，标签是支付方式的术语，载荷类型名也是同一个术语。根 README 从这里取 `PaymentMethod` 与 `Parse`。

## public.viba

```bash public
import parse.types as parse
import parse.apis as parse_api

PaymentMethod = parse.PaymentMethod

Card = parse.Card

Wallet = parse.Wallet

BankTransfer = parse.BankTransfer

Parse = parse_api.Parse
```

## types.viba

```bash types
PaymentMethod =
  Oneof
  | $card (Card * { 银行卡 })
  | $wallet (Wallet * { 钱包 })
  | $bank_transfer (BankTransfer * { 银行转账 })

Card =
  Object
  * $card_no (str * { 卡号 })
  * $holder (str * { 持卡人 })

Wallet =
  Object
  * $account (str * { 钱包账户 })
  * $provider (str * { 钱包服务商 })

BankTransfer =
  Object
  * $bank (str * { 开户行 })
  * $account_no (str * { 收款账号 })
```

## 基本操作

1. 从请求里读出支付方式。
2. 支付方式是银行卡时读出卡号与持卡人，是钱包时读出账户与服务商，是银行转账时读出开户行与收款账号。
3. 把读到的支付方式与这些字段记成一个 `PaymentMethod`。

## apis.viba

```bash apis
import parse.types as parse


Parse =
     parse.PaymentMethod
  <- $request (str * { 一条收款请求的文本 })
  <- {
    解析：从请求里读出支付方式与它带的字段，交回这次收款用的支付方式
  }
```
