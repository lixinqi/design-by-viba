# 拆环

## 需求背景

环是两张面孔：递归定义，和函数归属不明。类型递归是模型本来的样子，用泛型把自引用折起来；函数造成的环几乎都说明这个函数放错了模块，先问它到底服务于谁。

示例：sample 与 performance 互相依赖——sample 的 `Artifacts` 放 `CkptSli`，performance 的 `Measure` 参数是 `RunRecord`。这不是类型递归，是 `Measure` 的归属不清：它填的是 `Artifacts.metrics`，于是跟着记录走，移到 sample 之后环消失，performance 只剩指标类型与判定。

## public.viba

```bash public
import cycle.types as cycle
import cycle.apis as cycle_api

Cycle = cycle.Cycle
CycleKind = cycle.CycleKind
Diagnose = cycle_api.Diagnose
```

## types.viba

一个环先分种类，再决定拆法。递归定义靠泛型，函数造成的环靠重新组织模块；分不清种类时，先问「这个函数填的是谁的数据」。

```bash types
Cycle =
  Object
  * $nodes (list[str] * { 环上的模块或文档，按顺序 })
  * $kind (CycleKind * { 环的成因，决定拆法 })

CycleKind =
  Oneof
  | "recursive_definition" * { 类型引用自己形成环；用泛型把自引用折起来 }
  | "unclear_ownership" * { 函数用了别的模块的类型，而别的模块又用了它；把这个函数移到它服务的模块 }
  | "common_parent" * { 两边都缺同一块东西；抽出公共子模块，谁都不再指向对方 }
```

## 基本操作

只有一个操作：判环。给出一个环，判它是哪一类，并按那一类的拆法给出改动位置；判不出种类时，先回答「这个函数填的是谁的数据」。

## apis.viba

```bash apis
import cycle.types as cycle

Diagnose =
     cycle.CycleKind
  <- $nodes (list[str] * { 环上的模块或文档，按顺序 })
  <- {
    判环：类型自引用判 recursive_definition，函数与使用方互指判 unclear_ownership，两边同时缺一块判 common_parent；返回该用的拆法
  }
```
