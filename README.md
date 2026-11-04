# design by viba

一份设计文档最容易退化成一组互不相干的断言：每条单独看都对，却说不清谁依赖谁，也说不清哪一条被违反。这个仓库用 viba 把设计写成可执行规范：文档就是目录，代码块是模块，名字有唯一的定义处，引用就是边。规则集本身也按这套写法组织，并接受同一套检查。

## 入口

根文档是 [`README.viba.md`](README.viba.md)，对外只有两个操作：

- `Check`：输入仓库路径，逐条规则检查，返回 `Finding` 清单，每条带规则、位置与证据；
- `Ablate`：删除 public 够不到的定义，再验证需求要求的操作是否仍可解。

两份报告分别是 `CheckReport` 与 `AblationReport`。根文档的需求背景自定稿起冻结，新规则写入规则集，不改入口。

## 文档

| 文档 | 主题 |
|---|---|
| [`rules.viba.md`](rules.viba.md) | 规则集：42 条规则，每条一个类型 |
| [`requirement.viba.md`](requirement.viba.md) | 需求先行；根文档需求背景的冻结文本 |
| [`surface.viba.md`](surface.viba.md) | 外部只依赖 public |
| [`concept_edge.viba.md`](concept_edge.viba.md) | 概念用类型连边，说明里提到不算依赖 |
| [`closure.viba.md`](closure.viba.md) | 用闭包检验模型，孤立即删除 |
| [`cycle.viba.md`](cycle.viba.md) | 拆环：递归定义用泛型，函数归属不明就换模块 |
| [`naming.viba.md`](naming.viba.md) | 文件名、需求背景、public 三者一致；命名的正负与形态 |
| [`hint.viba.md`](hint.viba.md) | 提示写服务关系；依赖参数放在提示之后 |
| [`design_phase.viba.md`](design_phase.viba.md) | 设计阶段只留规范 |
| [`workflow.viba.md`](workflow.viba.md) | 每一步都要能被验证 |

每篇文档五段：需求背景、public、types、基本操作、apis。跨文档引用只经过目标文档的 public。

## 规则

规则来自一次真实重构：用户的原话、反复出现的纠错，以及由这些纠错归纳出的元规则。一条规则就是一个类型：

```viba
Rule =
  Oneof
  | $readme_background_frozen (ReadmeBackgroundFrozen * { ... })
  | ...

ReadmeBackgroundFrozen =
  Object
  * $statement (str * { 规则原文 })
  * $evidence (str * { 依据 })
  * $check (str * { 检查方法 })
  * $verdict (str * { 不满足 $check 时，报这一条并写出位置与证据 })
```

规则被违反时交回 `Finding`（规则、位置、证据），不为每种违规另造一个类型。

## 检查什么

可机检的规则覆盖：固定结构与需求背景、外部只依赖 public、闭包无孤立、依赖图无环、命名与正负、提示与依赖参数的写法、和类型必须带载荷、生成物与手写件互斥、以及根文档需求背景与冻结文本逐字一致。

检查结果必须能定位：`Finding` 的 `$where` 给出文件、行号与名字，`$evidence` 给出查到的内容。无法判定的情况不得当作通过。

过程类规则（例如“点名一处要改完整类”“被骂后先复盘”）只能人工执行，规则集保留它们，但不宣称有机器检查。

## 当前规模

文档 11 份，定义 104 个；从根 public 出发的闭包没有孤立定义，文档级依赖图无环。
