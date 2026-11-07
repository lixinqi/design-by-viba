# 告警分派

## 需求背景

输入是一条告警的来源 `$source` 与原文 `$text`；操作有两类：按原文判出告警级别，把告警发给值班人并交回分派结果。分派成功时只交回成功，失败时要交回没送达的原因。本示例是 PureEnumAllowed 的正例：`Severity` 的三个级别本来就没有数据，纯枚举是允许的；`AlertResult` 的失败变体带 `$reason`，失败原因随结果交回。

## public.viba

```viba public
import readme.types as readme
import readme.apis as readme_api

Alert = readme.Alert

AlertResult = readme.AlertResult

DispatchReport = readme.DispatchReport

Dispatch = readme_api.Dispatch
```

## types.viba

```viba types
import classify.public as classify


Alert =
  Object
  * $source (str * { 告警的来源，例如一台机器的名字 })
  * $text (str * { 告警的原文 })
  * $severity (classify.Severity * { 按原文判出的告警级别 })

AlertResult =
  Oneof
  | $ok ()
  | $failed ($reason str * { 没有分派出去的原因，值班人据此判断是否需要重发 })

DispatchReport =
  Object
  * $alert (Alert * { 已定级的告警 })
  * $result (AlertResult * { 这次分派的结果 })
```

## 基本操作

1. 把原文交给 `Classify` 判出级别，连同来源与原文记成一条 `Alert`。
2. 按级别选择一个值班通道，把告警发出去。
3. 发出去就在结果里记 `$ok`；没发出去就把原因记进 `$failed`，连同告警交回一条 `DispatchReport`。

## apis.viba

```viba apis
import readme.types as readme
import classify.public as classify


Dispatch =
     readme.DispatchReport
  <- $source (str * { 告警的来源，例如一台机器的名字 })
  <- $text (str * { 告警的原文 })
  <- {
    分派：按原文判出级别，把告警发给值班人，交回已定级的告警与这次分派的结果；失败时带没送达的原因
  }
  <- $classify (classify.Classify * { 分级：交回告警的级别，用它决定发给哪个值班通道 })
```
