# 告警分级

## 需求背景

输入是一条告警的原文 `$text`；操作只有一类：按原文里的关键词判出告警级别。根 README 从这里取 `Severity` 与 `Classify`。

## public.viba

```bash public
import classify.types as classify
import classify.apis as classify_api

Severity = classify.Severity

Classify = classify_api.Classify
```

## types.viba

```bash types
Severity =
  Oneof
  | $info ()
  | $warning ()
  | $critical ()
```

## 基本操作

1. 读原文。
2. 按关键词判出级别：出现“宕机”一类词记成严重，出现“变慢”一类词记成警告，其余记成提示。
3. 交回这个级别。

## apis.viba

```bash apis
import classify.types as classify


Classify =
     classify.Severity
  <- $text (str * { 告警的原文 })
  <- {
    分级：按原文里的关键词判出告警级别，交回提示、警告或严重
  }
```
