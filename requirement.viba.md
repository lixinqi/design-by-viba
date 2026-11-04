# 需求先行

## 需求背景

没有需求，public 会变成一张清单：名字都在，却说不出为什么是这些。需求背景要回答两件事——这篇文档替谁解决什么问题，别的文档为什么必须从它的 public 取名字。写不出这句需求的名字，就不该出现在 public 里。

示例：checkpoint bench 的根文档写「在一批真实的模型代码上，测量 checkpoint 写入与读取对存储的要求」，于是 public 只导出 `Bench` 与收代码、挑样本、跑一次、判阈值、比版本、补缺口六个操作；后来凡是讲不出由来的名字，都在闭包检验里被删掉了。根 README 从这里取 `Requirement` 与 `State`，所以这篇有 public。

## public.viba

```bash public
import requirement.types as requirement
import requirement.apis as requirement_api

Requirement = requirement.Requirement
State = requirement_api.State
```

## types.viba

一条需求要能被别人复核：说清问题、谁在等、需要哪些名字。三个字段缺一个，public 就没有依据。

```bash types
Requirement =
  Object
  * $statement (str * { 一句话说清问题：替谁、测什么、为什么现在做 })
  * $why (str * { 不做会怎样，谁在等这个结果 })
  * $surface (list[str] * { 这个问题需要对外可见的名字；多一个或少一个都要说清 })
```

## 基本操作

只有一个操作：写需求。给出问题、理由与需要对外可见的名字，返回一条需求；写不出 `$surface` 的需求不算需求。

## apis.viba

```bash apis
import requirement.types as requirement

State =
     requirement.Requirement
  <- $statement (str * { 一句话说清问题：替谁、测什么、为什么现在做 })
  <- $why (str * { 不做会怎样，谁在等这个结果 })
  <- $surface (list[str] * { 这个问题需要对外可见的名字 })
  <- {
    写需求：把问题、理由与名字清单收成一条需求；$surface 为空时直接答不可写，先回去想清楚替谁解决什么问题
  }
```
