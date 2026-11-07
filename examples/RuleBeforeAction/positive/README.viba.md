# 团队规范库维护

## 需求背景

输入是规范库目录的路径 `$root`；操作有两类：读出规范库里的规范，按淘汰规则删掉可以删的规范。本示例是 RuleBeforeAction 的正例：三条淘汰判据先写在 rules 文档里，`Retire` 把 `Judge` 写成依赖参数，先逐条核对判据，三条全部成立才删。

## public.viba

```viba public
import readme.types as readme
import readme.apis as readme_api

RetireReport = readme.RetireReport

Retire = readme_api.Retire
```

## types.viba

```viba types
import norms.public as norms


RetireReport =
  Object
  * $removed (list[norms.Norm] * { 已经删掉的规范，按文件名排列 })
  * $kept (list[norms.Norm] * { 留在库里的规范，按文件名排列 })
```

## 基本操作

1. 读规范库，拿到目录里的每篇规范。
2. 对每篇规范先让 `Judge` 逐条核对三条判据，收下每条的结论与依据。
3. 判据全部成立的规范交给 `Delete` 删掉，其余留在库里，交回删掉的规范与保留的规范。

## apis.viba

```viba apis
import readme.types as readme
import norms.public as norms
import rules.public as rules


Retire =
     readme.RetireReport
  <- $root (str * { 规范库目录的路径 })
  <- {
    淘汰：先逐篇核对三条判据，判据全部成立的规范才删掉，交回删掉的规范与保留的规范
  }
  <- $load (norms.Load * { 读库：交回目录里的每篇规范，用它取出要判定的规范 })
  <- $judge (rules.Judge * { 判定：交回一篇规范三条判据的核对结果与能否删除的结论，用它筛出判据全部成立的规范 })
  <- $delete (norms.Delete * { 删文件：交回删掉这篇规范之后剩下的规范清单，用它得到库里的剩余规范 })
```
