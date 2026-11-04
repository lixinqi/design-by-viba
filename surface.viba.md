# 外部只认 public

## 需求背景

一份文档内部可以随意拆模块，对外只能有一个门：public。外部要的名字集中在 public 里发布，types 与 apis 是实现，改了不影响别人。没有这条规矩，删一个内部类型之前得先读遍全仓，改名更不敢动。

示例：sample 文档的 public 只导出 `RunSpec`、`RunRecord`、`Execute`、`Measure` 等名字，performance 文档写 `import sample.public as sample`，从不直接拿 `sample.types`。一天里改了三次名字（`sample`、`level`、`ckpt_bypass_plan`），18 处跨文档引用一次改完、全仓搜旧名为 0，依据的就是这条规则。import 一律写项目根目录的绝对路径并带别名，读一行 import 就知道名字从哪个文档来。public 漏项和写错名字同样严重：构建样本的 `Collect` 与 `PickSamples` 一度不在根 public 里，整条链被闭包删掉。根 README 的 `Check` 依赖本篇的检查，`Violation` 用本篇的发现类型作载荷，所以这篇有 public。

## public.viba

```bash public
import surface.types as surface
import surface.apis as surface_api

Check = surface_api.Check
```

## types.viba

一个 public 槽位只做一件事：把内部模块里的一个名字，按外部要用的名字重新绑定一次。`$home` 记它定义在哪，外部不该知道也不需要知道。

```bash types
Surface =
  Object
  * $entries (list[SurfaceEntry] * { 这个 public 对外发布的全部名字 })
  * $owner (str * { 这份文档的文件名；public 里的名字必须能在本文档找到定义 })

SurfaceEntry =
  Object
  * $name (str * { 对外可见的名字 })
  * $home (str * { 这个名字定义在哪个内部模块，例如 sample.types })
  * $visibility (Visibility * { 这条名字对外发布，还是只给本文档内部用 })

Visibility =
  Oneof
  | "public" * { 对外可见；别的文档只能从这里取 }
  | "internal" * { 只在本文档内部使用；改名、删除都不影响别人 }

PublicLeak =
  Object
  * $surface (Surface * { 被引用的那篇文档的 public })
  * $import (str * { 落在 public 之外的 import，例如直接取 `sample.types` 而不是 `sample.public` })
```

## 基本操作

只有一个操作：查边界。看每篇文档的 import 落在目标文档的哪个模块上；落在 types 或 apis 上的记成一条泄漏。

## apis.viba

```bash apis
import surface.types as surface

Check =
     list[surface.PublicLeak]
  <- $repo (str * { 仓库路径：里面是一组 .viba.md 文档 })
  <- {
    查边界：逐条看 import 落在目标文档的哪个模块；落在 types 或 apis 上的记成 PublicLeak，落在 public 上的通过
  }
```
