# 概念图删除计划

## 需求背景

输入是一个文档仓库的根目录 `$root`；操作类别是删除：从根 public 出发走引用边，得到够不到的名字，整理成一份删除计划，交回这份计划。本示例是 GraphBeforeDelete 的反例：`Plan` 交回的 `DeletePlan` 只有 `$unreachable`，签名里没有列边的依赖参数，说明里提到过的名字也会被删掉。

## public.viba

```viba public
import readme.types as readme
import readme.apis as readme_api

DeletePlan = readme.DeletePlan

Plan = readme_api.Plan
```

## types.viba

```viba types
DeletePlan =
  Object
  * $unreachable (list[str] * { 闭包算出来够不到的名字：照这份名单删 })
```

## 基本操作

1. 让 `Scan` 扫出文档之间的全部引用。
2. 让 `Reach` 从根 public 出发，得到够不到的名字。
3. 对照引用边逐条查够不到的名字：有边指着的保留，没有边指着的写进删除名单。
4. 整理成删除计划，交回这份计划。

## apis.viba

```viba apis
import readme.types as readme
import graph.public as graph


Plan =
     readme.DeletePlan
  <- $root (str * { 文档仓库的根目录 })
  <- {
    整理删除计划：从根 public 出发得到闭包够不到的名字，交回删除计划
  }
  <- $reach (graph.Reach * { 算可达：从根 public 出发交回走到的名字与够不到的名字，用它列出要删的名字 })
```
