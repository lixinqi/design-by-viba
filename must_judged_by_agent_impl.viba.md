# 规则的判定表

默认 true：没有列在这里的规则都由 agent 判。viba 只按结构判类型，规则的检查方法写成一句话时，程序判不了它；只有检查方法能落到结构上的规则才列在这里，答 false。

能不能由程序判，看这条规则的 `$check` 能不能只读文档的结构：文件、章节、import、类型与字段、tag、名字、行号。要读出语义的（一句话在说什么、名字像不像、改动有没有越界、这一步有没有发生），一律留给 agent。

文件按编号从小到大判，第一个命中的赢。`900.viba` 是兜底，答 true。

## `__generic__.viba`

```viba
# __generic__.viba
```

## `100.viba`

`ReadmeBackgroundFrozen`：读 `README.viba.md` 需求背景的正文，与 `requirement.viba.md` 里 `FrozenRootBackground` 的冻结文本逐字比对；不一致即违规。

```viba
import rules.types as rules

pattern rules.ReadmeBackgroundFrozen

value = false
```

## `110.viba`

`ExternalOnlyPublic`：读每篇设计文档代码块里的 `import` 行；目标模块不属于本文档时，模块名必须以 `.public` 结尾，否则违规；模块文档与泛型目录不查。

```viba
import rules.types as rules

pattern rules.ExternalOnlyPublic

value = false
```

## `120.viba`

`FiveSections`：读每篇设计文档的 `##` 章节名，按 需求背景、public.viba、types.viba、基本操作、apis.viba 的顺序逐项比对；少一节或顺序不同即违规；多出来的节只许放在末尾；模块文档不查。

```viba
import rules.types as rules

pattern rules.FiveSections

value = false
```

## `130.viba`

`DependenciesAfterHint`：读每个函数定义的参数顺序：提示块 `<- { ... }` 之前只能是输入参数，之后才允许依赖参数（类型来自另一篇文档的操作）；提示块之前出现依赖参数即违规。

```viba
import rules.types as rules

pattern rules.DependenciesAfterHint

value = false
```

## `140.viba`

`DepTagAndApiType`：读每个依赖参数：必须写成 `<- $tag (X.Op * { 提示 })`，`X` 是另一篇文档的 public 别名，`Op` 是它导出的操作；类型写成 `str` 或内部类型即违规。

```viba
import rules.types as rules

pattern rules.DepTagAndApiType

value = false
```

## `150.viba`

`HintFolded`：每个函数提示块必须折行：`<- {` 独占一行开始，提示内容另起，`}` 独占一行结束；整块写成一行即违规。

```viba
import rules.types as rules

pattern rules.HintFolded

value = false
```

## `160.viba`

`OrphanIsUnreachable`：从根文档 public 导出的名字出发，沿字段类型、参数类型与 public 转发逐层走；走不到的定义记为孤立；只在说明文字里出现不算走到。

```viba
import rules.types as rules

pattern rules.OrphanIsUnreachable

value = false
```

## `170.viba`

`DeleteAllFileKinds`：对仓库里每种文件（`.viba.md`、生成物、脚本、数据）都按同一条判据回答“谁依赖它”：从根 public 出发的可达性；只对其中一类文件做判断即违规。

```viba
import rules.types as rules

pattern rules.DeleteAllFileKinds

value = false
```

## `180.viba`

`GeneratedFollowsSource`：从对象定义生成 schema：属性集合取对象定义的字段、去掉函数定义；与仓库里的 `schema.json` 比对，属性多一个或少一个即违规。

```viba
import rules.types as rules

pattern rules.GeneratedFollowsSource

value = false
```

## `190.viba`

`VariantCarriesType`：遍历每个 `Oneof`：每个变体必须写成 `| $tag (Type * { 提示 })`；变体只有 `()` 或字符串字面量即违规。

```viba
import rules.types as rules

pattern rules.VariantCarriesType

value = false
```

## `200.viba`

`NoRecordPlusKind`：同一个对象里同时出现 `$kind` 字段与纯字符串枚举类型即违规；状态要写成和类型，每个变体带着自己的类型。

```viba
import rules.types as rules

pattern rules.NoRecordPlusKind

value = false
```

## `210.viba`

`VirtualEdgeBeforeDelete`：对每个待删名字，列出两类边：真引用（出现在字段类型或参数类型里）与提及（只出现在说明文字里）；删除记录里缺这两类边即违规。

```viba
import rules.types as rules

pattern rules.VirtualEdgeBeforeDelete

value = false
```

## `220.viba`

`ViolationAttribution`：读每条 `Finding`：必须能读出规则、位置（文件与行号）与证据原文三样；缺一样即违规。

```viba
import rules.types as rules

pattern rules.ViolationAttribution

value = false
```

## `230.viba`

`FixedStructure`：仓库只有一个入口（根 `README.viba.md`）；每篇设计文档的 `##` 章节按固定顺序排列；多一个入口或章节不合顺序即违规。

```viba
import rules.types as rules

pattern rules.FixedStructure

value = false
```

## `240.viba`

`DesignPhaseSpecOnly`：对仓库里的每个文件回答：从根 public 出发有没有边到它；代码、生成物、样例数据与文档都一样，没有边即违规。

```viba
import rules.types as rules

pattern rules.DesignPhaseSpecOnly

value = false
```

## `250.viba`

`PublicOnlyOwnNames`：读每篇文档 `public.viba` 的每个导出行 `X = alias.Y`；`alias` 指向的模块必须属于本文档（模块名前缀与文档名相同）；转发别的文档的名字即违规。

```viba
import rules.types as rules

pattern rules.PublicOnlyOwnNames

value = false
```

## `260.viba`

`NoChangeLog`：搜索正文里的变更叙述（“本次”“今天”“改为”“新增”等）；命中即违规，变更写进提交信息。

```viba
import rules.types as rules

pattern rules.NoChangeLog

value = false
```

## `270.viba`

`NoTimeBoundContent`：搜索正文里的时间词（今天、本次、当前）与对话指代（上一轮、刚才）；命中即违规，应改写成适用条件。

```viba
import rules.types as rules

pattern rules.NoTimeBoundContent

value = false
```

## `280.viba`

`RuleHasExamples`：读每个规则叶子类型：必须有两行提示，分别给出正例与反例的路径，且路径指向的仓库存在；缺一行或路径不存在即违规。

```viba
import rules.types as rules

pattern rules.RuleHasExamples

value = false
```

## `900.viba`

```viba
pattern T

value = true
```
