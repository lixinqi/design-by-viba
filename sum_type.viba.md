# 带载荷的和类型

## 需求背景

和类型不是标签集合。一个变体就是一种情况，变体自己带这种情况的数据；读的人按变体分支，不需要先读一个 kind 字段再猜剩下的字段是什么。它替代的是「记录 + 标签枚举」和继承层次：父类那套 is-a 的写法，在这里是一个和类型加若干个带载荷的变体。

示例：`Unreachable` 原先写成 `{ $name, $kind }` 加一个 `OrphanKind` 枚举，删一个孤立物要先读 kind 再决定怎么删；改成四个变体之后，`$definition(str)`、`$document(str)`、`$file(str)`、`$reference(str)` 各自带自己的载荷，枚举消失。同样的改法还落在 `CyclicDependency`、`Artifact`、`Hint`、`Reference` 上，`Violation` 的十个变体也各带自己那条违规的证据类型，`Violation` 的 `$principle`、`$where`、`$what` 三个字段随之删掉。根 README 的 `Check` 依赖本篇的检查，`Violation` 用本篇的发现类型作载荷，所以这篇有 public。

## public.viba

```bash public
import sum_type.types as sum_type
import sum_type.apis as sum_type_api

Sum = sum_type.Sum
Variant = sum_type.Variant
Split = sum_type_api.Split
```

## types.viba

一个和类型由若干个变体组成；每个变体有标签和载荷类型两样东西。变体没有数据时，载荷写 `nil`：它表示这个变体没有数据，而不是没有这个变体。

```bash types
Sum =
  Object
  * $name (str * { 和类型的名字，例如 Unreachable })
  * $variants (list[Variant] * { 全部变体；一个变体就是一种情况 })

Variant =
  Object
  * $tag (str * { 变体的标签，例如 definition })
  * $payload (str * { 这个变体带的类型；没有数据时写 nil })
```

## 基本操作

只有一个操作：拆分。给出一个「记录 + 标签枚举」的写法，说清它该拆成哪几个变体、每个变体带什么载荷；拆不出来时说明它本来就是同一种情况，不需要和类型。

## apis.viba

```bash apis
import sum_type.types as sum_type

Split =
     sum_type.Sum
  <- $record (str * { 现在的写法：一条记录加一个标签枚举 })
  <- {
    拆分：按标签枚举的每个取值造一个变体，把记录里只属于这个取值的字段挪进它的载荷；所有变体共用、且与情况无关的字段留在和类型外面
  }
```
