# 配置校验

## 需求背景

输入是配置文件的文本 `$text`；操作只有一类：把文本逐项按规则检查，交回不合规的配置项。根 README 从这里取 `Violation` 与 `Validate`。

## public.viba

```viba public
import validate.types as validate
import validate.apis as validate_api

Violation = validate.Violation

Validate = validate_api.Validate
```

## types.viba

```viba types
Violation =
  Object
  * $key (str * { 配置项的名字 })
  * $reason (str * { 这一项不合规的原因 })
```

## 基本操作

1. 把配置文本的每一行按等号拆开，得到配置项的名字与值。
2. 按规则检查每一个名字与值。
3. 把不合规的项记成 `Violation`，按配置项在文件里的先后交回。

## apis.viba

```viba apis
import validate.types as validate


Validate =
     list[validate.Violation]
  <- $text (str * { 配置文件的文本，一项占一行，名字与值用等号分开 })
  <- {
    校验：逐项检查配置文本，交回不合规的配置项与原因
  }
```
