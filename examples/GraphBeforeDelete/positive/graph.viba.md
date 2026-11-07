# 概念图

## 需求背景

输入是一个文档仓库的根目录 `$root`；操作有两类：扫出概念图里的引用边，从根 public 出发算可达。根 README 从这里取 `Reference`、`Scan` 与 `Reach`。

## public.viba

```viba public
import graph.types as graph
import graph.apis as graph_api

Reference = graph.Reference

Closure = graph.Closure

Scan = graph_api.Scan

Reach = graph_api.Reach
```

## types.viba

```viba types
Edge =
  Object
  * $from (str * { 引用方，写成模块.名字 })
  * $to (str * { 被引用的名字 })

Reference =
  Oneof
  | $real (Edge * { 出现在字段类型或参数类型里：闭包走这条边 })
  | $mention (Edge * { 只出现在说明文字里：闭包不认这条边，删前要查 })

Closure =
  Object
  * $root (str * { 入口：根文档的 public })
  * $reached (list[str] * { 走到的名字，按模块分组 })
  * $unreachable (list[str] * { 没走到的名字：只是可疑，删前还要对照引用边 })
```

## 基本操作

1. 读仓库里的每篇文档。
2. 按字段类型、参数类型与 public 的转发找出引用，记成 `$real` 边；只在说明文字里出现的引用记成 `$mention` 边。
3. 从根 public 出发只走 `$real` 边，记下走到的名字与够不到的名字。
4. 把引用与可达结果分别交回。

## apis.viba

```viba apis
import graph.types as graph


Scan =
     list[graph.Reference]
  <- $root (str * { 文档仓库的根目录 })
  <- {
    列边：读出文档之间的引用，交回全部边；字段类型或参数类型里的记成 $real，只在说明里提到的记成 $mention
  }

Reach =
     graph.Closure
  <- $root (str * { 文档仓库的根目录 })
  <- {
    算可达：从根 public 出发只走 $real 边，交回走到的名字与够不到的名字
  }
```
