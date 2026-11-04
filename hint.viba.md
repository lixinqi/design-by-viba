# 提示与依赖参数

## 需求背景

函数依赖另一个 api 时，有三条写法约定：依赖写成带 tag 的参数，放在提示块之后；说明写清它交回什么、大 api 拿它做什么，不要复述名字；提示块无论长短都折行。约定成文，读签名就知道这一步会调用谁、拿结果做什么。

示例：`Execute` 的依赖参数 `<- $measure (sample.Measure * { 跑完把这条记录交给它，它把 trace 折算成六项 SLI，填进 Artifacts.metrics })`——交回什么、拿去做什么都在一句话里；与之相对的反例是 `* { 依赖 performance.apis：测量 SLI }`，它只是把名字又说了一遍。

## public.viba

```bash public
import hint.types as hint
import hint.apis as hint_api

Hint = hint.Hint
HintForm = hint.HintForm
DependencySlot = hint.DependencySlot
Write = hint_api.Write
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

DependencySlot =
  Object
  * $tag (str * { 依赖参数的 tag，例如 $measure })
  * $api (str * { 被依赖的 api，例如 sample.Measure })
  * $hint (Hint * { 它交回什么、大 api 拿它做什么 })
```

## 基本操作

1. 写提示：说明这一步做什么，不写实现细节。
2. 挂依赖：把依赖写成带 tag 的参数，类型写被依赖的 api，位置放在提示块之后。
3. 折行：函数的提示块改写成折行形态，不论长短。

## apis.viba

```bash apis
import hint.types as hint

Write =
     hint.DependencySlot
  <- $tag (str * { 依赖参数的 tag })
  <- $api (str * { 被依赖的 api })
  <- $returns (str * { 它交回什么 })
  <- $use (str * { 大 api 拿它做什么 })
  <- {
    写依赖：把交回什么与拿去做什么合成一句提示，挂到提示块之后的参数上；只复述名字的说明不算
  }
```
