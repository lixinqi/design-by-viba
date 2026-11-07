# 指标汇总

## 需求背景

输入是指标名 `$metric`；操作类别是汇总：按指标名读取序列里的采样值，相加并计数，交回报告。本示例是 VirtualEdgeBeforeDelete 的正例：`Sample` 只在提示里被提到，但 `Series` 有 `$samples (list[Sample])`，是真引用，所以保留。

## public.viba

```viba public
import readme.types as readme
import readme.apis as readme_api

Report = readme.Report

Rollup = readme_api.Rollup
```

## types.viba

```viba types
Report =
  Object
  * $metric (str * { 指标名 })
  * $total (float * { 采样值之和 })
  * $count (int * { 采样值的条数 })
```

## 基本操作

1. 按指标名让 `Read` 交回序列里的采样值。
2. 把采样值相加，记下条数。
3. 把指标名、总和与条数记成报告。

## apis.viba

```viba apis
import readme.types as readme
import series.public as series

Rollup =
     readme.Report
  <- $metric (str * { 指标名 })
  <- {
    汇总：按指标名读取序列里的采样值，相加并计数，交回报告
  }
  <- $read (series.Read * { 读取：交回这个指标的全部采样值，用它累计总和与条数 })
```
