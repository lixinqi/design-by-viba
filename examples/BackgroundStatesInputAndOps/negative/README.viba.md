# 指标采集与汇总

## 需求背景

本示例是 BackgroundStatesInputAndOps 的反例：需求背景写成了阅读顺序，既没有写输入，也没有写操作类别。阅读顺序是先看 types.viba，再看 apis.viba，最后看基本操作。

## public.viba

```viba public
import readme.types as readme
import readme.apis as readme_api

Metric = readme.Metric

Collect = readme_api.Collect

Rollup = readme_api.Rollup
```

## types.viba

```viba types
Sample =
  Object
  * $at (int * { 时间窗的起点，Unix 秒 })
  * $value (float * { 同一个时间窗里事件数值的和 })

Metric =
  Object
  * $name (str * { 指标名 })
  * $samples (list[Sample] * { 采样点，按时间窗的起点先后排好 })
```

## 基本操作

1. 把事件目录里的每个文件交给 `Parse`，收下它交回的事件。
2. 按指标名把事件分组，每一组按时间窗求和，得到采样点。
3. 每个指标交回一条 `Metric`，采样点按时间先后排好。

## apis.viba

```viba apis
import readme.types as readme
import parse.public as parse


Collect =
     list[parse.Event]
  <- $events_dir (str * { 事件目录的路径 })
  <- {
    采集：读出目录里每个事件文件的内容，交回全部事件，按读入顺序排好
  }
  <- $parse (parse.Parse * { 解析：交回一个事件文件里的全部事件，用它逐个读取目录里的文件 })

Rollup =
     list[readme.Metric]
  <- $events (list[parse.Event] * { 已采集的事件 })
  <- $window (int * { 时间窗的长度，单位秒 })
  <- {
    汇总：把同一个指标的事件按时间窗分段求和，交回每个指标按时间先后排好的采样点
  }
```
