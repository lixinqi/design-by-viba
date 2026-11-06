# 规则工具

规则集之外、检查规则时用的小工具。`trait.viba` 一章是判定规则由谁判的 trait：一行泛型定义，把问题转给 `must_judged_by_agent_impl` 的判定表；规则新增或改判时只动那张表。

## `trait.viba`

```viba
import must_judged_by_agent_impl as must_judged_by_agent_impl

must_judged_by_agent[T] = must_judged_by_agent_impl[T].value
```
