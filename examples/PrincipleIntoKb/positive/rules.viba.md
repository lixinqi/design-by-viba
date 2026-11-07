# 知识库规则集

## 需求背景

输入是一篇文档的全文 `$text`；操作只有一类：按规则集检查这篇文档，交回不合规的条目。本示例是 PrincipleIntoKb 的正例：知识库把用户讲清的“提示要折行”写成规则类型，叶子类型带规则原文、依据、检查方法与判定，并附示例路径。根 README 从这里取 `Finding` 与 `Check`。

## public.viba

```viba public
import rules.types as rules
import rules.apis as rules_api

Finding = rules.Finding

Check = rules_api.Check
```

## types.viba

```viba types
Rule =
  Oneof
  | $hints_folded (HintsFolded * { 函数提示块一律折行 })

HintsFolded =
  Object
  * $statement (str * { 函数提示块一律折行 })
  * $evidence (str * { 原话：提示要折行 })
  * $check (str * { 读每一个函数提示块，看它是否折成多行 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
  * { 正例见 examples/PrincipleIntoKb/positive }
  * { 反例见 examples/PrincipleIntoKb/negative }

Finding =
  Object
  * $rule (Rule * { 违反的是哪一条规则 })
  * $where (str * { 在哪个文件的哪一行 })
  * $evidence (str * { 查到的具体内容 })
```

## 基本操作

1. 读一篇文档的全文。
2. 按规则集里的每个变体检查文档，每个变体用自己的检查方法检查一遍。
3. 把违规的位置、证据与对应的规则记成 `Finding`，按出现顺序交回。

## apis.viba

```viba apis
import rules.types as rules


Check =
     list[rules.Finding]
  <- $text (str * { 一篇文档的全文 })
  <- {
    检查：按规则集逐条检查这篇文档，交回不合规的条目
  }
```
