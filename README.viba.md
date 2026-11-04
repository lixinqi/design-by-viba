# design by viba

## 需求背景

设计要能被机器检查，才谈得上被机器建设。总输入是一个仓库路径 `repo_path`，里面是一组 `.viba.md` 文档；操作分两类。

第一类是合规性检查：像编译一样，逐条规则检查仓库，清楚指出违反了哪一条、在哪个文件、违反了什么。

第二类是消融实验：删掉 public 够不到的死概念之后，README 需求要求的操作还能不能被解决；还能解决说明模型自洽，不能解决说明断的是哪条边。

示例：本仓库就是被检查的仓库——根 public 导出 `Check` 与 `Ablate` 两个操作，输入都是 `repo_path`；九条经验各提供一条原则，检查结果按原则归类。

## public.viba

```bash public
import readme.types as readme
import readme.apis as readme_api


CheckReport = readme.CheckReport

AblationReport = readme.AblationReport

Check = readme_api.Check

Ablate = readme_api.Ablate
```

## types.viba

两类操作共用一套词汇：一条违规就是一条规则的变体，变体自带那条规则查出来的证据；一次检查是违规的清单；一次消融记下删掉了哪些定义、需求还解不解决得了、缺的是哪一个。

```bash types
import rules.public as rules


CheckReport =
  Object
  * $violations (list[rules.Finding] * { 查出来的全部违规；每条带规则、位置与证据；空列表表示合规 })
  * $passed (bool * { 是否为真：没有违规即合规 })

AblationReport =
  Object
  * $removed (list[str] * { 消融删掉的定义，按模块分组 })
  * $still_solves (bool * { 删完之后，需求要求的操作是否还能被解决 })
  * $missing (list[str] * { 解决不了的缺口；$still_solves 为 true 时为空 })
```

## 基本操作

两类操作，输入都是 `repo_path`。

1. 合规检查：对仓库里每篇文档逐条规则检查——需求、public 边界、概念边、闭包、环、命名、提示、设计阶段、流程，把发现按原则归类，返回违规清单。
2. 消融实验：从根 public 出发删掉够不到的定义，再看需求要求的操作是否还能被解决；能解决返回删掉的清单，不能解决写清缺的是哪一个。

## apis.viba

```bash apis
import readme.types as readme
import rules.public as rules
import closure.public as closure
import concept_edge.public as concept_edge
import cycle.public as cycle
import design_phase.public as design_phase
import hint.public as hint
import naming.public as naming
import requirement.public as requirement
import surface.public as surface
import workflow.public as workflow

Check =
     readme.CheckReport
  <- $repo (str * { 仓库路径：里面是一组 .viba.md 文档 })
  <- {
    合规检查：对仓库里每篇文档逐条规则检查，把各原则的发现收成违规清单；$violations 为空时 $passed 为 true，否则逐条写清原则、位置与违反的内容
  }
  <- $rules (rules.CheckViolations * { 按规则检查：交回违规清单，这里按规则变体归类 })
  <- $run (workflow.Run * { 执行流程：它按 edit、load、closure、cycle、stale_name 的顺序检查，交回每一步的结果 })
  <- $reach (closure.Reach * { 算闭包：它交回走到的名字与没走到的名字，够不到的名字记成一条 unreachable })
  <- $diagnose (cycle.Diagnose * { 判环：它交回环的种类，文档级依赖图有环时记成一条 cyclic_dependency })
  <- $names (naming.CheckName * { 查命名：它交回的差异写成一条 name_mismatch })
  <- $judge (design_phase.Judge * { 判文件：它交回的保留或删除理由写成一条 dead_artifact })
  <- $requirement_check (requirement.Check * { 查需求：交回的缺口按规则变体归类 })
  <- $surface_check (surface.Check * { 查边界：交回的泄漏按规则变体归类 })
  <- $edge_check (concept_edge.CheckEdges * { 查概念边：交回的虚边按规则变体归类 })
  <- $hint_check (hint.Check * { 查提示：交回的不合规提示按规则变体归类 })
  <- $frozen_check (requirement.CheckFrozen * { 查冻结：交回的不一致记录按规则归类 })

Ablate =
     readme.AblationReport
  <- $repo (str * { 仓库路径：里面是一组 .viba.md 文档 })
  <- $required (list[str] * { 需求要求的操作名；README 需求背景里列的就是这些 })
  <- {
    消融实验：从根 public 出发删掉够不到的定义，再看 $required 里的操作是否还能被解决；能解决返回删掉的清单，不能解决时 $missing 写清缺的是哪一个
  }
  <- $reach (closure.Reach * { 算可达：它交回走到的名字，没走到的就是这次要消融掉的 })
  <- $prune (closure.Prune * { 删孤立：它按种类删除够不到的定义，交回这一轮删掉的条目 })
```
