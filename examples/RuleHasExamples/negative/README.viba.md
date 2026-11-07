# 规则集

## 需求背景

输入是一个 `.viba.md` 文档的路径 `$path`；操作是检查：用规则集逐条检查这份文档，交回违规清单。本示例是 RuleHasExamples 的反例：`Rule` 的 `$rule_has_examples` 变体对应 `RuleHasExamples`，这个规则类型只有规则原文与检查方法，没有示例提示。

## public.viba

```viba public
import readme.types as readme
import readme.apis as readme_api

RuleSet = readme.RuleSet

Check = readme_api.Check
```

## types.viba

```viba types
import rule.public as rule


RuleSet =
  Object
  * $rules (list[rule.Rule] * { 规则集里的全部规则，逐条带检查方法 })
```

## 基本操作

1. 从规则集里取出每一条规则。
2. 把文档路径与规则交给 `CheckRule`。
3. 把每条规则查出的违规收成一份清单，交回。

## apis.viba

```viba apis
import readme.types as readme
import rule.public as rule


Check =
     list[rule.Finding]
  <- $path (str * { 待检查文档的路径 })
  <- $rule_set (readme.RuleSet * { 规则集：里面的每条规则都要执行 })
  <- {
    检查：按规则集里的每条规则检查文档，交回全部违规
  }
  <- $check_rule (rule.CheckRule * { 查一条：交回这条规则查出的违规，用它逐条收成违规清单 })
```
