# 每步都要能被验证

## 需求背景

删改之后不能只读一遍就提交：要重新加载文档、跑一次闭包、检查环、搜旧名字。每一步都要有能被重复执行的判据，否则下一次改动又会把已经理清的关系打乱。

示例：每次改名后全仓搜旧名（`ckpt_sample`、`checkpoint.`、`Methodology`）确认为 0；每次删改后临时恢复生成器再执行一遍，79 份 schema 生成无误再删掉；提交信息里写清这一步用哪条规则判的，例如「Rename the sample and bypass-plan docs」。根 README 的 `Check` 依赖本篇的 `Run`，所以这篇有 public。

## public.viba

```bash public
import workflow.types as workflow
import workflow.apis as workflow_api

Run = workflow_api.Run
```

## types.viba

一次改动由六步组成，前五步都有输出，最后一步才提交。任何一步不通过，都回到改动本身，而不是在提交信息里解释。

```bash types
Step =
  Oneof
  | $edit (CheckResult * { 改文档这一步：文件、需求背景、public 三处一起改 })
  | $load (CheckResult * { 重新加载这一步：所有代码块能解析，模块树能加载 })
  | $closure (CheckResult * { 闭包这一步：从根 public 出发，孤立列表为空 })
  | $cycle (CheckResult * { 环这一步：文档级依赖图无环 })
  | $stale_name (CheckResult * { 旧名字这一步：全仓搜索为 0 })
  | $commit (CheckResult * { 提交这一步：写清用哪条规则判的 })

CheckName =
  Oneof
  | "edit" * { 改文档 }
  | "load" * { 重新加载 }
  | "closure" * { 闭包 }
  | "cycle" * { 环 }
  | "stale_name" * { 旧名字 }
  | "commit" * { 提交 }

CheckResult =
  Object
  * $passed (bool * { 这一步是否通过 })
  * $detail (str * { 通过或失败的具体证据，例如生成条数、环上的模块名 })
```

## 基本操作

只有一个操作：执行一遍。按 `$steps` 里 `CheckName` 的顺序逐条检查，任何一步不通过就停在那一步，并把证据写清。

## apis.viba

```bash apis
import closure.public as closure
import workflow.types as workflow

Run =
     list[workflow.Step]
  <- $steps (list[workflow.CheckName] * { 这次要跑的检查，按顺序 })
  <- {
    执行一遍：逐步执行 edit、load、closure、cycle、stale_name 五项检查，全部通过才提交；返回每一步的结果，失败时停在该步并写清证据
  }
  <- $reach (closure.Reach * { 算可达：它交回走到的名字与没走到的名字，闭包这一步按它判过不过 })
```
