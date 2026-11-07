# 需求先行

## 需求背景

没有需求，public 会变成一张清单：名字都在，却说不出为什么是这些。需求背景要回答两件事——这篇文档替谁解决什么问题，别的文档为什么必须从它的 public 取名字。写不出这句需求的名字，就不该出现在 public 里。

示例：checkpoint bench 的根文档写「在一批真实的模型代码上，测量 checkpoint 写入与读取对存储的要求」，于是 public 只导出 `Bench` 与收集代码、挑选样本、执行一次、判定阈值、比较版本、补充缺口六个操作；后来凡是讲不出由来的名字，都在闭包检验里被删掉了。根文档的需求背景一旦写定就冻结：新的经验写进别的文档，入口那句话不跟着改。根 README 的 `Check` 依赖本篇的 `Check` 与 `CheckFrozen`，所以这篇有 public。

## public.viba

```viba public
import requirement.types as requirement
import requirement.apis as requirement_api

Check = requirement_api.Check

CheckFrozen = requirement_api.CheckFrozen
```

## types.viba

一条需求要能被别人复核：说清问题、谁在等、需要哪些名字。三个字段缺一个，public 就没有依据。

```viba types
Requirement =
  Object
  * $statement (str * { 一句话说清问题：替谁、测什么、为什么现在做 })
  * $why (str * { 不做会怎样，谁在等这个结果 })
  * $surface (list[str] * { 这个问题需要对外可见的名字；多一个或少一个都要说清 })

FrozenRootBackground = str * { 冻结文本，逐字保留：设计要能被机器检查，才谈得上被机器建设。总输入是一个仓库路径 `repo_path`，里面是一组 `.viba.md` 文档；操作分两类。

第一类是合规性检查：像编译一样，逐条规则检查仓库，清楚指出违反了哪一条、在哪个文件、违反了什么。

第二类是消融实验：删掉 public 够不到的死概念之后，README 需求要求的操作还能不能被解决；还能解决说明模型自洽，不能解决说明断的是哪条边。

示例：本仓库就是被检查的仓库——根 public 导出 `Check` 与 `Ablate` 两个操作，输入都是 `repo_path`；九条经验各提供一条原则，检查结果按原则归类。 }

Background =
  Object
  * $doc (str * { 哪份文档的需求背景 })
  * $frozen (FrozenRootBackground * { 冻结时的文本；铁律要求它与当前文本一致 })
  * $current (str * { 当前文件里的文本 })

MissingRequirement =
  Object
  * $where (str * { 哪个文件的哪个 public 名字 })
  * $requirement ((Requirement | nil) * { 它对应的需求；nil 表示讲不出由来 })
```

## 基本操作

只有一个操作：查需求。对仓库里每个 public 名字，找到它对应的需求；找不到的记成一条缺口。

## apis.viba

```viba apis
import requirement.types as requirement

Check =
     list[requirement.MissingRequirement]
  <- $repo (str * { 仓库路径：里面是一组 .viba.md 文档 })
  <- {
    查需求：对每篇文档的每个 public 名字，找到它对应的需求；讲不出来由的记成 MissingRequirement，$requirement 给 nil
  }

CheckFrozen =
     list[requirement.Background]
  <- $repo (str * { 仓库路径：里面是一组 .viba.md 文档 })
  <- {
    查冻结：根文档的需求背景必须与冻结文本逐字一致；不一致的记成 Background，带上冻结文本与当前文本
  }
```
