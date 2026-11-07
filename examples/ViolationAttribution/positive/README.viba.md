# 规则检查器

## 需求背景

输入是一个规则目录的路径 `$rules` 与待检查仓库的根目录 `$root`；操作有两类：把规则目录里的每个文件解析成一条规则，按这些规则检查仓库里的文件并交回违规报告。本示例是 ViolationAttribution 的正例：`Finding` 把每条违规归因到 `$principle`、`$position`、`$evidence` 三个字段，分别写违反的原则、文件路径与行号、证据原文。

## public.viba

```viba public
import readme.types as readme
import readme.apis as readme_api

Report = readme.Report

Check = readme_api.Check
```

## types.viba

```viba types
Finding =
  Object
  * $principle (str * { 被违反的原则，取规则文件里的原则 })
  * $position (str * { 违规所在位置，写成文件路径与行号 })
  * $evidence (str * { 违规那几行的原文 })

Report =
  Object
  * $findings (list[Finding] * { 这次检查发现的违规，按在仓库里遇到的先后排列 })
```

## 基本操作

1. 逐个读规则目录里的规则文件，把每个路径交给 `Parse`，读出原则与正文。
2. 逐个读仓库里的文本文件，按每条规则的原则与正文找出违规。
3. 每发现一条违规，记成一条 `Finding`，收进 `Report` 交回。

## apis.viba

```viba apis
import readme.types as readme
import parse.public as parse


Check =
     readme.Report
  <- $rules (str * { 规则目录的路径，每个文件是一条规则 })
  <- $root (str * { 待检查仓库的根目录 })
  <- {
    检查：解析规则目录，按每条规则检查仓库里的文件，交回这次检查的报告
  }
  <- $parse (parse.Parse * { 解析：交回一条规则的原则与正文，用它比对仓库里的文件 })
```
