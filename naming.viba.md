# 文件名、需求背景、public 三者一致

## 需求背景

三处说的是同一件事：文件名叫什么，需求背景就该讲什么，public 就该导出什么。不一致说明概念还没理清，而且会一路传染到 import 与讨论里。

示例：`checkpoint.viba.md` 与目录同名、和 `README.viba.md` 争入口，改成 `ckpt_bypass_plan.viba.md`，内容是旁路方案；`scaling.viba.md` 的内容只剩档位，改成 `level.viba.md`；`measures` 的 public 还挂着已删文档的 `Methodology` 前缀，改成 `Metric`、`Tolerance`。三处对齐之后，读文件名就能猜到 import 长什么样。变体的形态也要一致：和类型的标签要么全是对问题的描述，要么全是术语名词，要么全是动作动词，不能混。示例：装违规的类型 `Violation`，它的变体全是问题描述（`missing_requirement`、`public_leak`、`malformed_hint` 等）；如果其中一个叫 `cycle` 或 `inline_hint`，它只是名词，读起来就不像同一类变体。载荷类型也一样：`Violation` 各变体的载荷类型是 `MissingRequirement`、`PublicLeak`、`MalformedHint` 这类问题名，不能一个叫 `Gap`、另一个叫 `Mismatch`。名字的正负也要一致：类型名是正面的，变体标签也得是正面的；否则类型与标签一起用负面名。示例：`Violation` 的变体全是负面名（`missing_requirement`、`public_leak` 等），若类型名与标签的正负相反，读起来就前后矛盾。每次删掉一个死概念之后，都要回头再查这三样，删东西最容易让名字与内容脱节。根 README 的 `Check` 依赖本篇的 `CheckName`，所以这篇有 public。

## public.viba

```bash public
import naming.types as naming
import naming.apis as naming_api

CheckName = naming_api.CheckName
```

## types.viba

一致性检查只需要三样东西：文件名、需求背景里的一句话、public 里的名字清单。三样放在一起，对不上的地方会自己跳出来。

```bash types
NameTriple =
  Object
  * $file (str * { 文件名，去掉 .viba.md })
  * $statement (str * { 需求背景里的一句话，说这篇解决什么问题 })
  * $surface (list[str] * { public 里导出的名字 })

NameMismatch =
  Oneof
  | $name_mismatch (NameTriple * { 文件名、需求背景、public 三处对不上 })
  | $polarity_clash (PolarityClash * { 类型名与变体标签的正负性对不上 })
  | $inconsistent_tag_form (TagFormMix * { 变体标签的形态混用：有的描述问题，有的只是名词 })

Polarity =
  Oneof
  | "positive" * { 正面名：说这个东西是什么，例如“某份文档的 public” }
  | "negative" * { 负面名：说哪里出了问题，例如 Violation 与 missing_requirement }

TagForm =
  Oneof
  | "problem" * { 对问题的描述，例如 missing_requirement }
  | "term" * { 术语名词，例如 cycle }
  | "verb" * { 动作动词，例如 check }

TagFormMix =
  Object
  * $type_name (str * { 类型名，例如 Violation })
  * $forms (list[TagForm] * { 各变体标签的形态；不止一种就是混用 })

PolarityClash =
  Object
  * $type_name (str * { 类型名，例如 Violation })
  * $type_polarity (Polarity * { 类型名的正负 })
  * $tags (list[str] * { 变体标签，例如 missing_requirement、public_leak })
  * $payload_types (list[str] * { 各变体带的载荷类型名，例如“缺了什么”“哪里泄漏” })
  * $tag_polarity (Polarity * { 标签的正负；与 $type_polarity 不同就是冲突 })
```

## 基本操作

只有一个操作：查一致。给出一组文件名、一句话与 public 清单，判它们是否说同一件事；不一致时写清哪里对不上。

## apis.viba

```bash apis
import naming.types as naming

CheckName =
     (naming.NameMismatch | nil)
  <- $triple (naming.NameTriple * { 文件名、一句话与 public 清单 })
  <- {
    查一致：变体标签的形态要统一、正负要一致；文件名里的关键词要能从 $statement 里找到，$surface 的每个名字要能用 $statement 解释，类型名与变体标签的正负要一致；对不上时返回差异，全部对得上时给 nil
  }
```
