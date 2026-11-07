# 页面解析

## 需求背景

输入是一个 Markdown 文件的路径 `$path`；操作是把第一个一级标题记成标题，其余内容记成正文。根 README 从这里取 `Page` 与 `Parse`。

## public.viba

```viba public
import parse.types as parse
import parse.apis as parse_api

Page = parse.Page

Parse = parse_api.Parse
```

## types.viba

```viba types
Page =
  Object
  * $title (str * { 第一个一级标题 })
  * $body (str * { 标题之后的正文 })
```

## 基本操作

1. 读入 `$path` 的文件内容，按换行切成行，用 `$line_no` 从 1 数起。
2. 遇到第一个以 `# ` 开头的行，把 `# ` 之后的文字记成 `$title`，把 `$line_no` 记成 `$title_line`，把 `$in_body` 置成 true。
3. `$in_body` 为 true 之后，每行原样追加到 `$body`，行与行之间补一个换行；不要先 join 再 strip，空行要留着。
4. 没有 `# ` 行时，把文件名去掉 `.viba.md` 的部分记成 `$title`，`$body` 取全文，`$title_line` 记成 0，`$in_body` 一直是 true。

## apis.viba

```viba apis
import parse.types as parse


Parse =
     parse.Page
  <- $path (str * { Markdown 文件的路径 })
  <- {
    解析：把第一个一级标题记成标题、其余内容记成正文，交回这个页面
  }
```
