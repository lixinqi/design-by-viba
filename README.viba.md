# design by viba

## 需求背景

设计最容易散成一个个点：每条都对，彼此没有边。viba 把一份文档变成可执行规范——文档是目录，代码块是模块，名字有唯一的家，引用就是边。这套方法是在一次真实的重构里磨出来的：先写需求，再由需求推出概念与操作，然后用闭包检验删掉够不到的东西，用图检查暴露缺的边和多余的环。

本篇是入口：九条经验各自回答一个问题，从 `Requirement` 读起，再顺着 public 往下。示例：本仓库自己就按这个方法组织——每篇文档都有需求背景、public、types、基本操作、apis，外部引用只走 public，全仓没有环。

## public.viba

```bash public
import readme.types as readme
import readme.apis as readme_api
import requirement.public as requirement
import surface.public as surface
import concept_edge.public as concept_edge
import closure.public as closure
import cycle.public as cycle
import naming.public as naming
import hint.public as hint
import design_phase.public as design_phase
import workflow.public as workflow

Lesson = readme.Lesson
Read = readme_api.Read
Requirement = requirement.Requirement
Surface = surface.Surface
Reference = concept_edge.Reference
Closure = closure.Closure
Cycle = cycle.Cycle
NameTriple = naming.NameTriple
Hint = hint.Hint
Artifact = design_phase.Artifact
CheckResult = workflow.CheckResult
State = requirement.State
Export = surface.Export
CheckEdges = concept_edge.CheckEdges
Reach = closure.Reach
Prune = closure.Prune
Diagnose = cycle.Diagnose
CheckName = naming.CheckName
Write = hint.Write
Judge = design_phase.Judge
Run = workflow.Run
```

## types.viba

九条经验回答九个问题，按依赖顺序排列：先有需求，才有 public；public 之间用类型连边，才谈得上闭包；闭包删东西之前，先看有没有环、名字对不对；最后才是改完之后怎么验证。

```bash types
Lesson =
  Oneof
  | "requirement" * { 先写需求：没有需求，public 只是一张清单 }
  | "surface" * { 外部只认 public：types 与 apis 是内部实现 }
  | "concept_edge" * { 概念要用类型连边：说明里提到不算依赖 }
  | "closure" * { 用闭包检验模型：从根 public 出发够不到的，删 }
  | "cycle" * { 拆环：递归定义用泛型，函数归属不明就换模块 }
  | "naming" * { 文件名、需求背景、public 三者信息量一致 }
  | "hint" * { 提示写清服务关系；依赖参数放在提示之后 }
  | "design_phase" * { 设计阶段只留规范：代码与生成物够不到就删 }
  | "workflow" * { 每步都要能被验证：加载、闭包、环、旧名 }

Reading =
  Object
  * $done (list[Lesson] * { 已经读过的经验，按顺序 })
  * $next ((Lesson | nil) * { 下一条要读的经验；全部读完时给 nil })
```

## 基本操作

1. 读一条：从需求背景开始，看这条经验解决什么问题，再看它的 public 给了谁。
2. 照着改：文件、需求背景、public 三处一起改，保持说的是同一件事。
3. 验证：重新加载文档，跑一次闭包，检查有没有环、有没有旧名字残留。

## apis.viba

```bash apis
import readme.types as readme

Read =
     readme.Reading
  <- $done (list[readme.Lesson] * { 已经读过的经验，按 Lesson 的顺序 })
  <- {
    读下一条：按 Lesson 的顺序交回还没读过的那一条；全部读完时 $next 给 nil，回到需求背景重新检查一遍
  }
```
