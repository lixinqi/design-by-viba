# 笔记检索

## 需求背景

输入是一个笔记目录的路径 `$notes_dir` 与一个查询串 `$query`；操作有两类：把查询串解析成要匹配与要排除的词项，按相关程度给目录里的笔记排序。本示例是 ExplainHardParts 的正例：`Search` 的基本操作先把排序要处理的难点讲清，再列步骤。

## public.viba

```viba public
import readme.types as readme
import readme.apis as readme_api

Result = readme.Result

Search = readme_api.Search
```

## types.viba

```viba types
import parse.public as parse


Hit =
  Object
  * $path (str * { 笔记文件的路径 })
  * $title (str * { 笔记的标题 })
  * $keyword (float * { 关键词分：按命中词出现的次数累加 })
  * $title_match (float * { 标题匹配分：标题含查询词为 1，不含为 0 })
  * $rank (int * { 在结果里的名次，从 1 开始，越小越靠前 })

Result =
  Object
  * $query (parse.Query * { 解析出来的词项 })
  * $hits (list[Hit] * { 排好序的笔记 })
```

## 基本操作

排序前要先处理一个难点：`$keyword` 与 `$title_match` 的取值范围不同。`$keyword` 按命中词出现的次数累加，不会小于 0，一篇笔记常见在 0 到 20 之间；`$title_match` 只有 0 与 1。两个分直接相加，关键词分会盖过标题匹配分。先把关键词分除以本批结果里最高的关键词分，把标题匹配分除以本批结果里最高的标题匹配分，两者都压到 0 到 1，这一步叫归一；再按 0.6 与 0.4 加权求和，得到总分，按总分排序的整套做法叫排序归一。例如本批结果里最高的关键词分是 12，一篇笔记的关键词分是 6，归一后是 0.5；它的标题含查询词，标题匹配分归一后是 1；总分是 0.6 × 0.5 + 0.4 × 1 = 0.7。某一字段的最高分为 0 时，该字段一律记 0。

1. 把 `$query` 交给 `Parse`，读出要匹配的词项与要排除的词项。
2. 按要匹配的词项找出目录里的候选笔记，去掉含要排除词项的笔记。
3. 给每篇候选笔记算出 `$keyword` 与 `$title_match`。
4. 按上面排序归一的规则把关键词分与标题匹配分都压到 0 到 1，加权成总分，从高到低排列，名次从 1 记起。
5. 把词项与排好的笔记装进 `Result`。

## apis.viba

```viba apis
import readme.types as readme
import parse.public as parse


Search =
     readme.Result
  <- $notes_dir (str * { 笔记目录的路径 })
  <- $query (str * { 查询串 })
  <- {
    检索：解析查询串，给目录里的笔记算出关键词分与标题匹配分，排好序交回结果
  }
  <- $parse (parse.Parse * { 解析：交回查询串里的词项与要排除的词项，用它挑出候选笔记 })
```
