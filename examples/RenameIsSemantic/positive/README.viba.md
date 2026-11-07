# 文档检索

## 需求背景

输入是一个 Markdown 目录的路径 `$root`，以及一个关键词 `$query`；操作有两类：解析单个页面，按关键词检索整个目录。本示例是 RenameIsSemantic 的正例：操作从 `Read` 改名为 `Search` 后，结果类型改成 `SearchResult`，提示改成“检索”。

## public.viba

```viba public
import readme.types as readme
import readme.apis as readme_api

SearchResult = readme.SearchResult

Search = readme_api.Search
```

## types.viba

```viba types
import parse.public as parse


SearchResult =
  Object
  * $pages (list[parse.Page] * { 命中的页面，按命中次数从高到低 })
  * $total (int * { 命中的页面总数 })
```

## 基本操作

1. 收下目录的路径与关键词。
2. 把目录里的每个 Markdown 文件交给 `Parse`。
3. 在页面的标题与正文里数关键词出现的次数，按次数把命中的页面排好。
4. 把命中的页面与总数交回。

## apis.viba

```viba apis
import readme.types as readme
import parse.public as parse


Search =
     readme.SearchResult
  <- $root (str * { Markdown 目录的路径 })
  <- $query (str * { 关键词 })
  <- {
    检索：把目录里的每个页面交给 Parse 解析出来，按关键词匹配标题与正文，交回命中的页面与总数
  }
  <- $parse (parse.Parse * { 解析：交回一个页面的标题与正文，用它匹配关键词 })
```
