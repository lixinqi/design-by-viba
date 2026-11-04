# design by viba

用 viba 把设计写成可执行规范：文档就是目录，代码块是模块，名字有唯一的定义处，引用就是边。规则集自己也按这套写法组织，并且用自己审查自己。

## 从哪读起

[`README.viba.md`](README.viba.md) 是根文档，对外只有两个操作：

- `Check`：输入仓库路径，逐条规则检查，交回违规清单；
- `Ablate`：删掉 public 够不到的定义，再验证需求要求的操作是否仍可解。

读完根文档，按 public 顺着看主题文档：`requirement`、`surface`、`concept_edge`、`closure`、`cycle`、`naming`、`hint`、`design_phase`、`workflow`。

## 文件

| 文件 | 内容 |
|---|---|
| [`README.viba.md`](README.viba.md) | 根文档：检查与消融两类操作，报告类型 |
| [`rules.viba.md`](rules.viba.md) | 规则集：42 条规则，每条规则一个变体，载荷是该规则自己的类型（规则原文、依据、检查方法、判定方式） |
| [`requirement.viba.md`](requirement.viba.md) | 需求先行；根文档需求背景的冻结文本 |
| [`surface.viba.md`](surface.viba.md) | 外部只依赖 public |
| [`concept_edge.viba.md`](concept_edge.viba.md) | 概念要用类型连边，说明里提到不算依赖 |
| [`closure.viba.md`](closure.viba.md) | 用闭包检验模型，孤立即删除 |
| [`cycle.viba.md`](cycle.viba.md) | 拆环：递归定义用泛型，函数归属不明就换模块 |
| [`naming.viba.md`](naming.viba.md) | 文件名、需求背景、public 三者一致；命名正负与形态 |
| [`hint.viba.md`](hint.viba.md) | 提示写服务关系；依赖参数放在提示之后 |
| [`design_phase.viba.md`](design_phase.viba.md) | 设计阶段只留规范 |
| [`workflow.viba.md`](workflow.viba.md) | 每步都要能被验证 |

每篇文档都是五段：需求背景 → public → types → 基本操作 → apis；外部引用只走目标文档的 public。

## 规则集

42 条规则来自一次真实重构的执行记录：用户的原话、反复出现的纠错、以及由此归纳出的元规则。每条规则在 [`rules.viba.md`](rules.viba.md) 里是一个和类型的变体，带一个独立类型：

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

规则被违反时不是另造一个类型，而是交回 `Finding`（规则、位置、证据）。

## 自审记录

规则集建立之后，项目按自己的规则审了四轮，每轮跑五项检查（解析、模块加载、public 闭包、文档级环、旧名字搜索），通过后提交推送。审出并修掉的违规：

| 规则 | 违规 | 修复 |
|---|---|---|
| A33 | 检查只返回规则，没有位置与证据 | 新增 `Finding` |
| A16/A18/A19 | 负面类型名配正面规则名 | 类型改为 `Rule`，违规由 `Finding` 表示 |
| A15 | `Step` 是记录 + 标签枚举 | 改为和类型，变体各自带结果 |
| A23 | 提示提到类型名但代码没引用 | 改为描述情形 |
| A01 | 冻结没有可比基线 | 冻结文本存进 `FrozenRootBackground`，脚本比对 |

当前状态：文档 11 份、定义 104 个、孤儿 0、文档级环 0、旧名字 0 命中、解析失败 0。

## 说明

- 过程类规则（如“点名一处要改完整类”“被骂后先复盘”）只能人工执行，规则集里仍保留，但没有对应的机器检查；
- 根文档的需求背景自定稿起冻结，任何新规则写进 `rules.viba.md`，不改入口那句话。
