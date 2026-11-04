# 设计阶段只留规范

## 需求背景

设计阶段产出的是规范，不是实现。代码、生成的 schema、样例数据、配方配置，只要从根 public 出发没有一条边能到它，就是负担：读的人要判断它是否还有效，写的人要维护两套真相。判据始终是同一条——有没有从 public 出发的边。

示例：一天里删掉 12 个 python、79 份生成的 schema、7 份手写 schema、配方 yaml、指标登记表与样例数据，共 102 个文件；文档里指向它们的说明同步改成按内容描述。真正需要保留的只有被 public 依赖的文档：11 份，1142 行。根 README 从这里取 `Artifact` 与 `Judge`，所以这篇有 public。

## public.viba

```bash public
import design_phase.types as design_phase
import design_phase.apis as design_phase_api

Artifact = design_phase.Artifact
Judge = design_phase_api.Judge
```

## types.viba

仓库里的文件分四类：规范、生成物、工具、样例数据。只有规范可能被 public 依赖；其余三类一旦没有边，就该删。

```bash types
Artifact =
  Oneof
  | $spec (str * { 文档路径：类型与操作的出处，可能被 public 依赖 })
  | $generated (str * { 生成物路径：例如 JSON Schema；规范删了它就是陈旧数据 })
  | $tooling (str * { 脚本与依赖清单的路径；设计阶段没有实现可跑，只在验证时临时出现 })
  | $sample_data (str * { 样例数据与配方配置的路径；没有文档引用就是死数据 })

Verdict =
  Object
  * $artifact (Artifact * { 被判断的文件 })
  * $keep (bool * { 是否保留；只有规范且从 public 可达时为真 })
  * $why (str * { 保留或删除的理由，写清是从哪条边判的 })
```

## 基本操作

只有一个操作：判一份文件。看它是不是规范、有没有从 public 出发的边，答保留或删除，并写清理由。

## apis.viba

```bash apis
import design_phase.types as design_phase

Judge =
     design_phase.Verdict
  <- $artifact (design_phase.Artifact * { 要判断的文件 })
  <- $reachable (bool * { 从根 public 出发能不能走到它 })
  <- {
    判一份文件：spec 且可达才保留；generated、tooling、sample_data 一律删，可达的规范被删时先补边再删
  }
```
