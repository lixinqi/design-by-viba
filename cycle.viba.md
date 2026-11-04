# 拆环

## 需求背景

环分两类：递归定义，和函数归属不明。类型递归是模型本来的样子，用泛型用泛型消解自引用；函数造成的环几乎都说明这个函数放错了模块，先问它实际服务于谁。

示例：sample 与 performance 互相依赖——sample 的 `Artifacts` 放 `CkptSli`，performance 的 `Measure` 参数是 `RunRecord`。这不是类型递归，是 `Measure` 的归属不清：它填的是 `Artifacts.metrics`，于是跟着记录走，移到 sample 之后环消失，performance 只剩指标类型与判定。根 README 的 `Check` 依赖本篇的检查，`Violation` 用本篇的发现类型作载荷，所以这篇有 public。

## public.viba

```bash public
import cycle.types as cycle
import cycle.apis as cycle_api

CyclicDependency = cycle.CyclicDependency
Diagnose = cycle_api.Diagnose
```

## types.viba

一个环先分种类，再决定拆法。递归定义靠泛型，函数造成的环靠重新组织模块；分不清种类时，先问「这个函数填的是谁的数据」。

```bash types
CyclicDependency =
  Oneof
  | $recursive_definition (list[str] * { 环上的模块或文档，按顺序；类型引用自己，用泛型用泛型消解自引用 })
  | $unclear_ownership (list[str] * { 环上的模块或文档，按顺序；函数用了别的模块的类型，把它移到它服务的模块 })
  | $common_parent (list[str] * { 环上的模块或文档，按顺序；两边都缺同一块东西，抽出公共子模块 })
```

## 基本操作

只有一个操作：判环。给出一个环，判它是哪一类，并按那一类的拆法给出改动位置；判不出种类时，先回答「这个函数填的是谁的数据」。

## apis.viba

```bash apis
import cycle.types as cycle

Diagnose =
     cycle.CyclicDependency
  <- $nodes (list[str] * { 环上的模块或文档，按顺序 })
  <- {
    判环：类型自引用判 recursive_definition，函数与使用方互指判 unclear_ownership，两边同时缺一块判 common_parent；返回带节点的环
  }
```
