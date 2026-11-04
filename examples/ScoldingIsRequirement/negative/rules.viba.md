# 规则记录

## 需求背景

输入是一句训斥的原话 `$scold`；操作只有一类：从原话反推一条规则，交回一条规则记录。根 README 从这里取 `Rule` 与 `Record`。

## public.viba

```bash public
import rules.types as rules
import rules.apis as rules_api

Rule = rules.Rule

Record = rules_api.Record
```

## types.viba

```bash types
Rule =
  Object
  * $statement (str * { 提示要写清楚 })
```

## 基本操作

1. 逐字记下训斥的原话。
2. 从原话反推说话人痛恨的做法，写成规则。
3. 把原话与规则收成一条 `Rule`，交回。

## apis.viba

```bash apis
import rules.types as rules


Record =
     rules.Rule
  <- $scold (str * { 训斥的原话，逐字抄录 })
  <- {
    记录：从训斥的原话反推一条规则，交回一条规则记录
  }
```
