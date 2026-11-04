# 规范淘汰规则

## 需求背景

输入是一篇规范 `$norm`；操作只有一类：按淘汰规则逐条核对三条判据，交回结论与依据。本示例是 RuleBeforeAction 正例的规则方：三条判据先写成 `Criterion` 的核对结果，`Judge` 先交回每条的结论与依据，再交回能否删除的结论。根 README 从这里取 `Criterion`、`Verdict` 与 `Judge`。

## public.viba

```bash public
import rules.types as rules
import rules.apis as rules_api

Criterion = rules.Criterion

Verdict = rules.Verdict

Judge = rules_api.Judge
```

## types.viba

```bash types
Criterion =
  Object
  * $name (str * { 判据名：作废、取代、引用 })
  * $passed (bool * { 这条判据成立时为 true })
  * $evidence (str * { 核对到的内容：作废标记的值、取代它的规范名、引用它的规范名 })

Verdict =
  Object
  * $deletable (bool * { 三条判据全部成立时为 true })
  * $criteria (list[Criterion] * { 三条判据各一条核对结果，顺序固定为作废、取代、引用 })
```

## 基本操作

1. 作废：`$retired` 为 true 时判据成立，依据写作废标记的值。
2. 取代：`$replaced_by` 非空时判据成立，依据写取代它的规范名。
3. 引用：`$referenced_by` 为空列表时判据成立，依据写引用它的规范名。
4. 三条判据全部成立时 `$deletable` 记为 true，把三条核对结果按作废、取代、引用的顺序交回。

## apis.viba

```bash apis
import rules.types as rules
import norms.public as norms


Judge =
     rules.Verdict
  <- $norm (norms.Norm * { 要判定的一篇规范 })
  <- {
    判定：逐条核对三条淘汰判据并记下依据，三条全部成立才交回可删的结论
  }
```
