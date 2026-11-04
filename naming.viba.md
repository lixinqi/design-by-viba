# 文件名、需求背景、public 三者一致

## 需求背景

三处说的是同一件事：文件名叫什么，需求背景就该讲什么，public 就该导出什么。不一致说明概念还没理清，而且会一路传染到 import 与讨论里。

示例：`checkpoint.viba.md` 与目录同名、和 `README.viba.md` 争入口，改成 `ckpt_bypass_plan.viba.md`，内容是旁路方案；`scaling.viba.md` 的内容只剩档位，改成 `level.viba.md`；`measures` 的 public 还挂着已删文档的 `Methodology` 前缀，改成 `Metric`、`Tolerance`。三处对齐之后，读文件名就能猜到 import 长什么样。每次删掉一个死概念之后，都要回头再查这三样，删东西最容易让名字与内容脱节。根 README 从这里取 `NameTriple`、`Mismatch` 与 `CheckName`，所以这篇有 public。

## public.viba

```bash public
import naming.types as naming
import naming.apis as naming_api

NameTriple = naming.NameTriple
Mismatch = naming.Mismatch
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

Mismatch =
  Object
  * $triple (NameTriple * { 被检查的那一组 })
  * $why (str * { 哪里对不上：文件名说 A，背景说 B，public 导出 C })
```

## 基本操作

只有一个操作：查一致。给出一组文件名、一句话与 public 清单，判它们是否说同一件事；不一致时写清哪里对不上。

## apis.viba

```bash apis
import naming.types as naming

CheckName =
     (naming.Mismatch | nil)
  <- $triple (naming.NameTriple * { 文件名、一句话与 public 清单 })
  <- {
    查一致：文件名里的关键词要能从 $statement 里找到，$surface 的每个名字要能用 $statement 解释；对不上时返回差异，全部对得上时给 nil
  }
```
