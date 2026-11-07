# 团队规范交付

## 需求背景

输入是团队规范目录的路径 `$root` 与独立审查者的名字 `$reviewer`；操作有三类：解析目录里的每篇规范，把正文的措辞搞一下，把整批规范与审查记录交成一份规范集。本示例是 TextReviewedBySubagent 的反例：交付前没有起独立 subagent 审查，也没有留下审查记录，README 直接用了口语。

## public.viba

```viba public
import readme.types as readme
import readme.apis as readme_api

Delivery = readme.Delivery

Deliver = readme_api.Deliver
```

## types.viba

```viba types
import norms.public as norms
import review.public as review


Delivery =
  Object
  * $norms (list[norms.Norm] * { 交付的规范，顺序与目录里的文件名一致 })
  * $review (review.ReviewRecord * { 交付前的独立审查记录：审查者、发现清单与判定 })
```

## 基本操作

1. 走一遍 `$root`，把每篇规范交给 `Parse`，收下名字与正文。
2. 把规范的正文按文件名顺序拼成交付文本这玩意儿，连同审查者交给 `Review`，收下审查记录。
3. 审查记录里 `$passed` 为 false 就退回；为 true 就把规范与审查记录收成 `Delivery`。

## apis.viba

```viba apis
import readme.types as readme
import norms.public as norms
import review.public as review


Deliver =
     readme.Delivery
  <- $root (str * { 团队规范目录的路径 })
  <- $reviewer (str * { 独立审查者的名字，记进审查记录 })
  <- {
    交付：解析目录里的每篇规范，收下交付前的独立审查记录，交回一份规范集
  }
  <- $parse (norms.Parse * { 解析：交回一篇规范的名字与正文，用它收成交付文本 })
  <- $review (review.Review * { 审查：交回审查者、发现清单与判定，用它决定是否交付 })
```
