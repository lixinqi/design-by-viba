# 规则检查器

## 需求背景

输入是一个示例仓库的路径 `$root`，以及一份规则清单；操作有两类：检查单篇文档，把整个仓库检查成一份报告。本示例是 TypeNameSaysContent 的正例：装规则、位置与证据的类型叫 `Violation`，名字与内容是一类。

## public.viba

```bash public
import readme.types as readme
import readme.apis as readme_api

Report = readme.Report

Audit = readme_api.Audit
```

## types.viba

```bash types
import check.public as check

Report =
  Object
  * $violations (list[check.Violation] * { 全部违规，按文档路径排好 })
```

## 基本操作

1. 收下示例仓库的路径与规则清单。
2. 把每篇文档的路径与规则清单交给 `Check`。
3. 把交回的违规按文档路径排好，收集成一份报告。

## apis.viba

```bash apis
import readme.types as readme
import check.public as check

Audit =
     readme.Report
  <- $root (str * { 示例仓库的路径 })
  <- $rules (list[check.Rule] * { 要执行的规则清单 })
  <- {
    审计：把仓库里的每篇文档交给检查，收集违规，交回一份报告
  }
  <- $check (check.Check * { 检查：交回一篇文档的违规，用它查完整个仓库 })
```
