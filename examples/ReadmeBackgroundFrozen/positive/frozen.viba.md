# 冻结的需求背景

## 需求背景

输入是 README 需求背景的当前文本 `$text`；操作是核对：把这段文本与冻结文本逐字比较，不一致时给出冻结文本与当前文本。本示例是 ReadmeBackgroundFrozen 正例的冻结方：冻结文本就是 README 需求背景定稿时的那一份。根 README 从这里取 `FrozenBackground` 与 `CheckFrozen`。

## public.viba

```viba public
import frozen.types as frozen
import frozen.apis as frozen_api

FrozenBackground = frozen.FrozenBackground

CheckFrozen = frozen_api.CheckFrozen
```

## types.viba

```viba types
FrozenBackground = str * { 冻结文本，逐字保留：输入是 README 文件的路径 `$readme`；操作是构建首页：读出 README 的大标题、需求背景与各级标题，核对需求背景与冻结文本，排出站点首页。本示例是 ReadmeBackgroundFrozen 的正例：README 需求背景的全文与冻结文本逐字一致。 }

Background =
  Object
  * $frozen (FrozenBackground * { 冻结时的文本，逐字保留 })
  * $current (str * { 核对时给出的文本 })
```

## 基本操作

1. 保留 README 需求背景定稿时的那一份文本。
2. 把待核对的文本与冻结文本逐字比较。
3. 不一致时给出冻结文本与当前文本。

## apis.viba

```viba apis
import frozen.types as frozen


CheckFrozen =
     list[frozen.Background]
  <- $text (str * { 待核对的需求背景 })
  <- {
    核对：把 $text 与冻结文本逐字比较，不一致时交回一条记录，带上冻结文本与当前文本
  }
```
