# 交付检查

## 需求背景

输入是一个仓库目录的路径 `$root`；操作有三类：逐篇解析目录里的文档，把文档装进缓存，把这一轮的检查结果汇成 `Round`。本示例是 SixChecksPerRound 的正例：`Round` 的六个字段分别记下解析、加载、闭包、环、旧名、三者一致的结论与证据。

## public.viba

```viba public
import readme.types as readme
import readme.apis as readme_api

Round = readme.Round

Review = readme_api.Review
```

## types.viba

```viba types
import parse.public as parse
import cache.public as cache


Check =
  Object
  * $count (int * { 这一项检查发现的问题数 })
  * $evidence (str * { 问题所在的路径与原文，没有问题时为空串 })

Round =
  Object
  * $parsed (parse.Parsed * { 解析检查：通过与失败的篇数，以及失败文档的位置 })
  * $loaded (cache.Loaded * { 加载检查：装进缓存与加载失败的篇数，以及失败文档的位置 })
  * $closure (Check * { 闭包检查：悬空引用的问题数与位置 })
  * $cycle (Check * { 环检查：文档互相引用成环的问题数与路径 })
  * $old_name (Check * { 旧名检查：改名后残留旧名的问题数与位置 })
  * $name_triple (Check * { 三者一致检查：文件名、需求背景与 public 对不上的问题数与位置 })
```

## 基本操作

1. 收下这一轮要检查的仓库目录路径。
2. 把目录交给 `Parse`，取回解析检查的结论；交给 `Load`，取回加载检查的结论。
3. 其余检查逐项跑一遍，每项记下问题数与证据。
4. 把各项结论汇成这一轮的 `Round`。

## apis.viba

```viba apis
import readme.types as readme
import parse.public as parse
import cache.public as cache


Review =
     readme.Round
  <- $root (str * { 待检查仓库的目录路径 })
  <- {
    检查：把这一轮的各项检查跑一遍，交回每一项的结论与证据
  }
  <- $parse (parse.Parse * { 解析：交回通过与失败的篇数，以及失败文档的位置，用它填解析那一项 })
  <- $load (cache.Load * { 加载：交回装进缓存与加载失败的篇数，以及失败文档的位置，用它填加载那一项 })
```
