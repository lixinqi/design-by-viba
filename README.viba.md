# design by viba

## 需求背景

设计要能被机器检查，才谈得上被机器建设。总输入是一个仓库路径 `repo_path`，里面是一组 `.viba.md` 文档；操作分两类。

第一类是合规性检查：像编译一样，逐条原则检查仓库，清楚指出违反了哪一条、在哪个文件、违反了什么。

第二类是消融实验：删掉 public 够不到的死概念之后，README 需求要求的操作还能不能被解决；还能解决说明模型自洽，不能解决说明断的是哪条边。

示例：本仓库就是被检查的仓库——根 public 导出 `Check` 与 `Ablate` 两个操作，输入都是 `repo_path`；九条经验各提供一条原则，检查结果按原则归类。

## public.viba

```bash public
import readme.types as readme
import readme.apis as readme_api
import sum_type.public as sum_type
import requirement.public as requirement
import surface.public as surface
import concept_edge.public as concept_edge
import closure.public as closure
import cycle.public as cycle
import naming.public as naming
import hint.public as hint
import design_phase.public as design_phase
import workflow.public as workflow

Violation = readme.Violation
CheckReport = readme.CheckReport
AblationReport = readme.AblationReport
Check = readme_api.Check
Sum = sum_type.Sum
Variant = sum_type.Variant
Split = sum_type.Split
Ablate = readme_api.Ablate
Requirement = requirement.Requirement
Gap = requirement.Gap
Surface = surface.Surface
Leak = surface.Leak
Reference = concept_edge.Reference
Closure = closure.Closure
Cycle = cycle.Cycle
NameTriple = naming.NameTriple
Polarity = naming.Polarity
Hint = hint.Hint
Inline = hint.Inline
Artifact = design_phase.Artifact
CheckResult = workflow.CheckResult
CheckEdges = concept_edge.CheckEdges
Reach = closure.Reach
Prune = closure.Prune
Diagnose = cycle.Diagnose
CheckName = naming.CheckName
Judge = design_phase.Judge
Run = workflow.Run
```

## types.viba

两类操作共用一套词汇：一条违规就是一条规则的变体，载荷就是那条规则查出来的东西；一次检查是违规的清单；一次消融记下删掉了哪些定义、需求还解不解决得了、缺的是哪一个。

```bash types
import requirement.public as requirement
import surface.public as surface
import concept_edge.public as concept_edge
import closure.public as closure
import cycle.public as cycle
import naming.public as naming
import hint.public as hint
import design_phase.public as design_phase
import workflow.public as workflow

Violation =
  Oneof
  | $missing_requirement (requirement.Gap * { 先写需求：public 名字讲不出由来时，载荷是这个缺口 })
  | $public_leak (surface.Leak * { 外部只认 public：import 绕过 public 时，载荷是这条泄漏 })
  | $virtual_reference (concept_edge.Reference * { 概念要用类型连边：说明里提到不算依赖，载荷是这条虚引用 })
  | $unreachable (closure.Orphan * { 用闭包检验模型：从根 public 出发够不到时，载荷是这个孤立物 })
  | $cyclic_dependency (cycle.Cycle * { 拆环：递归定义或函数归属不清时，载荷是带节点的环 })
  | $name_mismatch (naming.Mismatch * { 文件名、需求背景、public 对不上时，载荷是这处差异 })
  | $malformed_hint (hint.Inline * { 提示写清服务关系、依赖参数放在提示之后；不合时，载荷是这条提示 })
  | $dead_artifact (design_phase.Verdict * { 设计阶段只留规范：该删的文件，载荷是这个判断 })
  | $failed_step (workflow.CheckResult * { 每步都要能被验证：某一步没通过时，载荷是这一步的结果 })
  | $root_background_changed (requirement.Background * { 铁律：根文档的需求背景不得随意更改；被改动时，载荷是冻结时与现在的两句 })

CheckReport =
  Object
  * $violations (list[Violation] * { 查出来的全部违规；每个变体就是一种违规和它带的证据；空列表表示合规 })
  * $passed (bool * { 是否为真：没有违规即合规 })

AblationReport =
  Object
  * $removed (list[str] * { 消融删掉的定义，按模块分组 })
  * $still_solves (bool * { 删完之后，需求要求的操作是否还能被解决 })
  * $missing (list[str] * { 解决不了的缺口；$still_solves 为 true 时为空 })
```

## 基本操作

两类操作，输入都是 `repo_path`。

1. 合规检查：对仓库里每篇文档逐条原则检查——需求、public 边界、概念边、闭包、环、命名、提示、设计阶段、流程，把发现按原则归类，返回违规清单。
2. 消融实验：从根 public 出发删掉够不到的定义，再看需求要求的操作是否还能被解决；能解决返回删掉的清单，不能解决写清缺的是哪一个。

## apis.viba

```bash apis
import readme.types as readme
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
    合规检查：对仓库里每篇文档逐条原则检查，把各原则的发现收成违规清单；$violations 为空时 $passed 为 true，否则逐条写清原则、位置与违反的内容
  }
  <- $run (workflow.Run * { 跑流程：它按 edit、load、closure、cycle、stale_name 的顺序检查，交回每一步的结果 })
  <- $reach (closure.Reach * { 算闭包：它交回走到的名字与没走到的名字，够不到的名字记成一条 unreachable })
  <- $diagnose (cycle.Diagnose * { 判环：它交回环的种类，文档级依赖图有环时记成一条 cyclic_dependency })
  <- $names (naming.CheckName * { 查命名：它交回的差异写成一条 name_mismatch })
  <- $judge (design_phase.Judge * { 判文件：它交回的保留或删除理由写成一条 dead_artifact })
  <- $requirement_check (requirement.Check * { 查需求：它交回的 Gap 写成一条 missing_requirement })
  <- $surface_check (surface.Check * { 查边界：它交回的 Leak 写成一条 public_leak })
  <- $edge_check (concept_edge.CheckEdges * { 查概念边：它交回的虚边写成一条 virtual_reference })
  <- $hint_check (hint.Check * { 查提示：它交回的 Inline 写成一条 malformed_hint })
  <- $frozen_check (requirement.CheckFrozen * { 查冻结：它交回的 Background 写成一条 root_background_changed })

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
