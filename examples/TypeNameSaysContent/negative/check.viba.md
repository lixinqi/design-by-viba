# 文档检查

## 需求背景

输入是一篇文档的路径 `$path`，以及一份规则清单；操作是按规则清单检查这篇文档，交回命中的违规。本示例是 TypeNameSaysContent 反例的依赖方：装规则、位置与证据的类型叫 `Lesson`，名字与内容不是一类。根 README 从这里取 `Rule`、`Lesson` 与 `Check`。

## public.viba

```viba public
import check.types as check
import check.apis as check_api

Rule = check.Rule

Position = check.Position

Lesson = check.Lesson

Check = check_api.Check
```

## types.viba

```viba types
Rule =
  Object
  * $name (str * { 规则名，例如 TypeNameSaysContent })
  * $statement (str * { 规则原文：什么算违反 })
  * $check (str * { 检查方法：怎么查 })

Position =
  Object
  * $doc (str * { 文档的路径 })
  * $section (str * { 节标题 })

Lesson =
  Object
  * $rule (Rule * { 命中的规则，带规则名、原文与检查方法 })
  * $where (Position * { 违规出在哪个文档的哪一节 })
  * $evidence (str * { 违规处的原文 })
```

## 基本操作

1. 读文档。
2. 对每一条规则，按它的检查方法比对文档。
3. 每命中一条，记下规则、位置与证据，交回违规清单。

## apis.viba

```viba apis
import check.types as check

Check =
     list[check.Lesson]
  <- $path (str * { 文档的路径 })
  <- $rules (list[check.Rule] * { 要执行的规则清单 })
  <- {
    检查：对一篇文档逐条执行规则清单，交回命中的违规，每条带规则、位置与证据
  }
```
