# 指标序列

## 需求背景

输入是指标名 `$metric` 与一批采样值 `$values`；操作有两类：把采样值追加到序列，按指标名读出序列里的采样值。根 README 从这里取 `Read`。

## public.viba

```bash public
import series.types as series
import series.apis as series_api

Series = series.Series

Append = series_api.Append

Read = series_api.Read
```

## types.viba

```bash types
Series =
  Object
  * $metric (str * { 指标名 })
  * $samples (list[float] * { 采样值，按追加顺序排好 })
```

## 基本操作

1. 按指标名找到序列；没有就新建一条。
2. 把每个采样值记进 `$samples`，保持追加顺序。
3. 交回更新后的序列。

## apis.viba

```bash apis
import series.types as series

Append =
     series.Series
  <- $metric (str * { 指标名 })
  <- $values (list[float] * { 采样值，按追加顺序 })
  <- {
    追加：把采样值并进序列末尾，交回更新后的序列
  }

Read =
     list[float]
  <- $metric (str * { 指标名 })
  <- {
    读取：按指标名取出序列里的全部采样值，交回这一串值
  }
```
