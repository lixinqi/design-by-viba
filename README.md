# design by viba

一份设计文档最容易退化成一组互不相干的断言：每条单独看都对，却说不清谁依赖谁，也说不清哪一条被违反。这个仓库用 viba 把设计写成可执行规范：文档就是目录，代码块是模块，名字有唯一的定义处，引用就是边。规则集本身也按这套写法组织，并接受同一套检查。

## 依赖

本仓库依赖 [viba](https://github.com/lixinqi/viba)，主要是它的写法文档 [viba/wiki](https://github.com/lixinqi/viba/tree/main/viba/wiki)：`.viba.md` 怎么读、模块与 import 怎么解析、示例怎么加载，都以那里为准。本仓库只放设计规范与示例，不含解析器；示例仓库用 viba 的 markdown 读取器与 parser 校验，`tests/` 里的用例用 viba 的 interpreter 跑：`VIBA_ROOT=../viba python3 tests/test_must_judged_by_agent.py`。

## 入口

根文档是 [`README.viba.md`](README.viba.md)，对外只有两个操作：

- `Check`：输入仓库路径，逐条规则检查，返回 `Finding` 清单，每条带规则、位置与证据；
- `Ablate`：删除 public 够不到的定义，再验证需求要求的操作是否仍可解。

两份报告分别是 `CheckReport` 与 `AblationReport`。根文档的需求背景自定稿起冻结，新规则写入规则集，不改入口。

## 文档

| 文档 | 主题 |
|---|---|
| [`rules.viba.md`](rules.viba.md) | 规则集：55 条规则，每条一个类型与一对示例仓库 |
| [`requirement.viba.md`](requirement.viba.md) | 需求先行；根文档需求背景的冻结文本 |
| [`surface.viba.md`](surface.viba.md) | 外部只依赖 public |
| [`concept_edge.viba.md`](concept_edge.viba.md) | 概念用类型连边，说明里提到不算依赖 |
| [`closure.viba.md`](closure.viba.md) | 用闭包检验模型，孤立即删除 |
| [`cycle.viba.md`](cycle.viba.md) | 拆环：递归定义用泛型，函数归属不明就换模块 |
| [`naming.viba.md`](naming.viba.md) | 文件名、需求背景、public 三者一致；命名的正负与形态 |
| [`hint.viba.md`](hint.viba.md) | 提示写服务关系；依赖参数放在提示之后 |
| [`design_phase.viba.md`](design_phase.viba.md) | 设计阶段只留规范 |
| [`workflow.viba.md`](workflow.viba.md) | 每一步都要能被验证 |
| [`rule_tools.viba.md`](rule_tools.viba.md) | 规则工具：判定一条规则由谁判 |
| [`must_judged_by_agent_impl.viba.md`](must_judged_by_agent_impl.viba.md) | 判定表：程序能判的规则与交给 agent 的规则 |

表里前 10 份与根文档 [`README.viba.md`](README.viba.md) 是设计文档，共 11 份：每篇五段——需求背景、public、types、基本操作、apis；跨文档引用只经过目标文档的 public。表里最后 2 份是模块文档，没有五段，也没有 public：章就是模块的文件。

## 规则

规则来自一次真实重构：用户的原话、反复出现的纠错，以及由这些纠错归纳出的元规则。一条规则就是一个类型：

```viba
Rule =
  Oneof
  | $readme_background_frozen (ReadmeBackgroundFrozen * { ... })
  | ...
```

每个变体的载荷是这条规则自己的叶子类型，里面写规则原文、依据、检查方法与判定方式。规则被违反时交回 `Finding`（规则、位置、证据），不为每种违规另造一个类型。

## 示例

每条规则有两个示例仓库：`examples/<规则类型>/positive` 满足这条规则，`examples/<规则类型>/negative` 是同一个项目只在这一处违规。每个仓库有两到三篇文档，五段齐全，能被 viba 加载；正例与反例是同一个项目，差别就是这条规则管的那一处，可以直接对比。

`examples/` 是规则的用例，不是本仓库设计的一部分：每个示例有自己的 `README.viba.md`，是一个独立的仓库根；检查本仓库时按仓库根划分，不把示例算进本仓库的文档树。

## 检查什么

程序能判的规则覆盖：五段与唯一根、根需求背景逐字比对、外部只依赖 public、public 只导出本文档的名字、闭包的孤立物、虚边、设计阶段的可达性、生成物跟源头走、和类型带载荷、禁止记录+kind、依赖参数与提示的写法、违规归因、变更叙述与时间词扫描、每条规则带示例。其余规则要读出语义或过程（例如“点名一处要改完整类”“被骂后先复盘”），交给 agent 判；一条规则归哪一边，见规则工具与判定表。

检查结果必须能定位：`Finding` 的 `$where` 给出文件、行号与名字，`$evidence` 给出查到的内容。无法判定的情况不得当作通过。

## 当前规模

设计文档 11 份（117 个定义），模块文档 2 份；规则 55 条，每条一对示例仓库，共 110 个；程序能判的 19 条，其余 36 条交给 agent。从根 public 出发的闭包没有孤立定义，文档级依赖图无环。
