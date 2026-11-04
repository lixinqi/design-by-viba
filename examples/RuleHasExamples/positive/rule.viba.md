# 规则检查

## 需求背景

输入是一个 `.viba.md` 文档的路径 `$path`；操作是用一条规则检查这份文档，交回违规。根 README 从这里取 `Rule`、`RuleHasExamples`、`Finding` 与 `CheckRule`。

## public.viba

```bash public
import rule.types as rule
import rule.apis as rule_api

Rule = rule.Rule

RuleHasExamples = rule.RuleHasExamples

Finding = rule.Finding

CheckRule = rule_api.CheckRule
```

## types.viba

```bash types
Rule =
  Oneof
  | $rule_has_examples (RuleHasExamples * { 每条规则必须有正例与反例 })

RuleHasExamples =
  Object
  * $statement (str * { 规则原文：每条规则必须有正例与反例 })
  * $check (str * { 检查方法：检查每个规则类型是否带正例与反例的路径 })
  * { 正例见 examples/RuleHasExamples/positive }
  * { 反例见 examples/RuleHasExamples/negative }

Finding =
  Object
  * $rule (Rule * { 违反的是哪一条规则 })
  * $line (int * { 违规所在的行号 })
  * $evidence (str * { 查到的具体内容 })
```

## 基本操作

1. 读文档。
2. 按规则原文与检查方法核对文档。
3. 不符合时记一条违规，带上规则、行号与证据。

## apis.viba

```bash apis
import rule.types as rule_types


CheckRule =
     list[rule_types.Finding]
  <- $path (str * { 待检查文档的路径 })
  <- $rule (rule_types.Rule * { 待执行的规则：按它的检查方法检查文档 })
  <- {
    检查：按一条规则的检查方法读文档，交回这条规则查出的违规
  }
```
