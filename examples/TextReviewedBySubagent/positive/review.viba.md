# 交付前审查

## 需求背景

输入是一份待交付文本 `$text` 与独立审查者的名字 `$reviewer`；操作只有一类：逐句检查文本的口语、术语与拗口，交回审查记录。仓库里三篇文档在交付前由独立 subagent `text-reviewer` 审查，发现清单有三条：口语一条，“把正文的措辞搞一下”改为“逐句审查正文的措辞”；术语一条，“交付文本这玩意儿”改为“交付文本”；拗口一条，README 需求背景的第一句按输入与操作拆成两句。修改后判定为通过。根 README 从这里取 `ReviewRecord` 与 `Review`。

## public.viba

```viba public
import review.types as review
import review.apis as review_api

ReviewRecord = review.ReviewRecord

Review = review_api.Review
```

## types.viba

```viba types
Finding =
  Object
  * $aspect (str * { 检查方面：口语、术语或拗口 })
  * $evidence (str * { 命中的原文，逐字抄录 })
  * $advice (str * { 修改建议 })

ReviewRecord =
  Object
  * $reviewer (str * { 审查者的名字：由独立 subagent 担任 })
  * $findings (list[Finding] * { 发现清单，按文本顺序排列；空列表表示没有发现 })
  * $passed (bool * { 发现全部改完后重新审查通过时为 true })
```

## 基本操作

1. 读一遍待交付文本。
2. 逐句查口语，把过分口语的说法记成一条 `Finding`：`$evidence` 抄原文，`$advice` 写改成哪种说法。
3. 逐个查术语，把不标准的说法记成一条 `Finding`：`$evidence` 抄原文，`$advice` 写标准术语。
4. 查拗口，把读不顺的句子记成一条 `Finding`：`$evidence` 抄原句，`$advice` 写改写。
5. 没有发现时 `$passed` 记为 true；有发现时为 false，把审查者、发现清单与判定交回。

## apis.viba

```viba apis
import review.types as review


Review =
     review.ReviewRecord
  <- $text (str * { 待审查的交付文本 })
  <- $reviewer (str * { 独立审查者的名字，记进记录 })
  <- {
    审查：逐句检查文本的口语、术语与拗口，交回发现清单与判定
  }
```
