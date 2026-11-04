# 概念要用类型连边

## 需求背景

说明里写出一个类型名，不等于依赖它：提示不是代码，闭包看不见它。概念之间的关系要用字段类型或参数类型表达，一段说明只是注脚；注脚里提到的名字，闭包会当成孤立物。

示例：`RunSpec.$config` 曾经写成 `str * { ...那份配置必须含 SampleConfigBase 的字段 }`。闭包检验时，`SampleConfigBase` 没有被任何字段或参数引用，连它的 `Topology`、`ObservationConfig` 一起被删掉。把字段改成 `$config (SampleConfigBase * { ... })` 之后，这条边才真正存在，三个类型都回来了。根 README 从这里取 `Reference` 与 `CheckEdges`，所以这篇有 public。

## public.viba

```bash public
import concept_edge.types as concept_edge
import concept_edge.apis as concept_edge_api

Reference = concept_edge.Reference
CheckEdges = concept_edge_api.CheckEdges
```

## types.viba

两条定义之间的关系只有两种情况：真边（闭包认）与只在说明里提到（闭包不认）。把两者分开记，才能一眼看出哪些边是虚的。

```bash types
Reference =
  Object
  * $from (str * { 引用方，写成模块.名字 })
  * $to (str * { 被引用的名字 })
  * $kind (EdgeKind * { 这条边是不是真边 })

EdgeKind =
  Oneof
  | "reference" * { 出现在字段类型或参数类型里；闭包认它 }
  | "mention" * { 只出现在说明文字里；闭包不认，等于没有这条边 }
```

## 基本操作

只有一个操作：查边。给出一批引用，逐条判它是真边还是只在说明里提到；虚边要么改成真边，要么把说明里的名字删掉。

## apis.viba

```bash apis
import concept_edge.types as concept_edge

CheckEdges =
     list[concept_edge.Reference]
  <- $references (list[concept_edge.Reference] * { 从文档里抽出来的候选引用 })
  <- {
    查边：kind 为 mention 的都是虚边——要么把它改成字段类型或参数类型里的引用，要么删掉说明里的名字；返回需要处理的引用
  }
```
