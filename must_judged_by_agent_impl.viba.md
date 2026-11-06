# 规则的判定表

默认 true：没有列在这里的规则都由 agent 判。viba 只按结构判类型，规则的检查方法写成一句话时，程序判不了它；只有检查方法能落到结构上的规则才列在这里，答 false。

能不能由程序判，看这条规则的 `$check` 能不能只读文档的结构：文件、章节、import、类型与字段、tag、名字、行号。要读出语义的（一句话在说什么、名字像不像、改动有没有越界、这一步有没有发生），一律留给 agent。

文件按编号从小到大判，第一个命中的赢。`900.viba` 是兜底，答 true。

## `__generic__.viba`

```viba
# __generic__.viba
```

## `100.viba`

`ReadmeBackgroundFrozen`：README 的需求背景与冻结文本逐字比对。

```viba
import rules.types as rules

pattern rules.ReadmeBackgroundFrozen

value = false
```

## `110.viba`

`ExternalOnlyPublic`：跨文档 import 以 `.public` 结尾。

```viba
import rules.types as rules

pattern rules.ExternalOnlyPublic

value = false
```

## `120.viba`

`FiveSections`：抽 `##` 章节名比对。

```viba
import rules.types as rules

pattern rules.FiveSections

value = false
```

## `130.viba`

`DependenciesAfterHint`：看提示块之前的参数里有没有 `_api.`。

```viba
import rules.types as rules

pattern rules.DependenciesAfterHint

value = false
```

## `140.viba`

`DepTagAndApiType`：依赖参数带 tag，类型写被依赖的 api。

```viba
import rules.types as rules

pattern rules.DepTagAndApiType

value = false
```

## `150.viba`

`HintFolded`：看函数提示块是不是折行写法。

```viba
import rules.types as rules

pattern rules.HintFolded

value = false
```

## `160.viba`

`OrphanIsUnreachable`：从根 public 做可达性，差集就是孤立物。

```viba
import rules.types as rules

pattern rules.OrphanIsUnreachable

value = false
```

## `170.viba`

`DeleteAllFileKinds`：每类文件按同一条可达性判据查一遍。

```viba
import rules.types as rules

pattern rules.DeleteAllFileKinds

value = false
```

## `180.viba`

`GeneratedFollowsSource`：定义集合减去函数，与应有的 schema 文件比对。

```viba
import rules.types as rules

pattern rules.GeneratedFollowsSource

value = false
```

## `190.viba`

`SumWithPayload`：遍历 `Oneof`，看每个变体有没有载荷。

```viba
import rules.types as rules

pattern rules.SumWithPayload

value = false
```

## `200.viba`

`NoRecordPlusKind`：搜 `$kind` 与纯字符串枚举同时出现。

```viba
import rules.types as rules

pattern rules.NoRecordPlusKind

value = false
```

## `210.viba`

`VirtualEdgeBeforeDelete`：列出说明里的 mention 与代码里的 reference 比对。

```viba
import rules.types as rules

pattern rules.VirtualEdgeBeforeDelete

value = false
```

## `220.viba`

`ViolationAttribution`：看每条 `Finding` 有没有规则、位置与证据。

```viba
import rules.types as rules

pattern rules.ViolationAttribution

value = false
```

## `230.viba`

`FixedStructure`：抽章节与入口，看是不是固定结构、唯一根。

```viba
import rules.types as rules

pattern rules.FixedStructure

value = false
```

## `240.viba`

`DesignPhaseSpecOnly`：从 public 出发，看每类文件可达不可达。

```viba
import rules.types as rules

pattern rules.DesignPhaseSpecOnly

value = false
```

## `250.viba`

`PublicOnlyOwnNames`：看 public 每个导出行的来源模块是不是本文档的。

```viba
import rules.types as rules

pattern rules.PublicOnlyOwnNames

value = false
```

## `260.viba`

`NoChangeLog`：搜「本次」「改为」「新增」这类变更叙述。

```viba
import rules.types as rules

pattern rules.NoChangeLog

value = false
```

## `270.viba`

`NoTimeBoundContent`：搜时间词与对话指代。

```viba
import rules.types as rules

pattern rules.NoTimeBoundContent

value = false
```

## `280.viba`

`RuleHasExamples`：看每个规则类型有没有正例与反例的路径。

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
