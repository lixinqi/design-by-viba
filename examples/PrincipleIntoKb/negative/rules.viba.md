# 知识库规则集

## 需求背景

输入是一篇文档的全文 `$text`；操作只有一类：按规则集检查这篇文档，交回不合规的条目。本示例是 PrincipleIntoKb 的反例：知识库只在基本操作里写了一句“提示要折行”，没有把它写成规则类型，也没有附示例。根 README 从这里取 `Finding` 与 `Check`。

## public.viba

```bash public
import rules.types as rules
import rules.apis as rules_api

Finding = rules.Finding

Check = rules_api.Check
```

## types.viba

```bash types
Finding =
  Object
  * $rule (str * { 违反的规则原文 })
  * $where (str * { 在哪个文件的哪一行 })
  * $evidence (str * { 查到的具体内容 })
```

## 基本操作

1. 读一篇文档的全文。
2. 提示要折行。
3. 把违规的位置、证据与对应的规则记成 `Finding`，按出现顺序交回。

## apis.viba

```bash apis
import rules.types as rules


Check =
     list[rules.Finding]
  <- $text (str * { 一篇文档的全文 })
  <- {
    检查：按规则集逐条检查这篇文档，交回不合规的条目
  }
```
