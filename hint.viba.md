# 提示与依赖参数

## 需求背景

函数依赖另一个 api 时，有三条写法约定：依赖写成带 tag 的参数，放在提示块之后；说明写清它交回什么、大 api 拿它做什么，不要复述名字；提示块无论长短都折行。约定成文，读签名就知道这一步会调用谁、拿结果做什么。

示例：`Execute` 的依赖参数 `<- $measure (sample.Measure * { 跑完把这条记录交给它，它把 trace 折算成六项 SLI，填进 Artifacts.metrics })`——交回什么、拿去做什么都在一句话里；与之相对的反例是 `* { 依赖 performance.apis：测量 SLI }`，它只是把名字又说了一遍。根 README 从这里取 `Hint`、`Inline` 与 `Check`，所以这篇有 public。

## public.viba

```bash public
import hint.types as hint
import hint.apis as hint_api

Hint = hint.Hint
Inline = hint.Inline
Check = hint_api.Check
```

## types.viba

提示有两种形态：折行的块，和更短的内联说明；依赖参数只有一个形态——放在提示块之后、带 tag、类型直接写被依赖的 api。

```bash types
Hint =
  Object
  * $form (HintForm * { 提示的写法 })
  * $text (str * { 这一步做什么；依赖参数的提示还要写它交回什么、拿它做什么 })

HintForm =
  Oneof
  | "folded" * { 函数的提示块：`<- {` 单独一行，文字缩进一层，`}` 回到 `<-` 的缩进 }
  | "inline" * { 字段或参数上的提示：`* { ... }` 写在同一行 }

Inline =
  Object
  * $where (str * { 哪个函数的哪个参数 })
  * $hint (Hint * { 那条不合规的提示；形态或位置不对都在这里记下 })
```

## 基本操作

只有一个操作：查提示。看每个函数的提示块是不是折行、依赖参数是不是放在提示块之后；不合的记成一条 Inline。

## apis.viba

```bash apis
import hint.types as hint

Check =
     list[hint.Inline]
  <- $repo (str * { 仓库路径：里面是一组 .viba.md 文档 })
  <- {
    查提示：提示块要折行，依赖参数要带 tag 并放在提示块之后，说明要写交回什么与拿去做什么；不合的记成 Inline
  }
```
