# 概念图删除计划

## 需求背景

输入是一个文档仓库的根目录 `$root`；操作类别是删除：从根 public 出发走引用边，得到够不到的名字，整理成一份删除计划，交回这份计划。本示例是 GraphBeforeDelete 的正例：`Plan` 交回的 `DeletePlan` 先列出概念图里的引用边，够不到但被 `$mention` 边指着的名字保留下来，只有没有任何边指着的名字才写进删除名单。

## public.viba

```bash public
import readme.types as readme
import readme.apis as readme_api

DeletePlan = readme.DeletePlan

Plan = readme_api.Plan
```

## types.viba

```bash types
import graph.public as graph


DeletePlan =
  Object
  * $references (list[graph.Reference] * { 删前扫出来的全部引用：真边与只在说明里提到的边都收在这里 })
  * $kept (list[str] * { 够不到但有 $mention 边指着的名字：不删，把这条边补成真边 })
  * $unreachable (list[str] * { 够不到也没有任何边指着的名字：这些才写进删除名单 })
```

## 基本操作

1. 让 `Scan` 扫出文档之间的全部引用。
2. 让 `Reach` 从根 public 出发，得到够不到的名字。
3. 对照引用边逐条查够不到的名字：有边指着的保留，没有边指着的写进删除名单。
4. 整理成删除计划，交回这份计划。

## apis.viba

```bash apis
import readme.types as readme
import graph.public as graph


Plan =
     readme.DeletePlan
  <- $root (str * { 文档仓库的根目录 })
  <- {
    整理删除计划：先扫出全部引用，再得到闭包够不到的名字，逐条对照引用边之后交回删除计划
  }
  <- $scan (graph.Scan * { 列边：交回文档之间的全部引用，只在说明里提到的边也在里面，用它查够不到的名字有没有被提到 })
  <- $reach (graph.Reach * { 算可达：从根 public 出发交回走到的名字与够不到的名字，用它列出待查的候选 })
```
