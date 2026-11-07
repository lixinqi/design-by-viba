# 文档解析

## 需求背景

输入是一篇文档文件的路径 `$path`；操作只有一类：读出文档的标题与词项。根 README 从这里取 `Document` 与 `Parse`。

## public.viba

```viba public
import parse.types as parse
import parse.apis as parse_api

Document = parse.Document

Parse = parse_api.Parse
```

## types.viba

```viba types
Document =
  Object
  * $title (str * { 文档的一级标题 })
  * $terms (list[str] * { 正文切出来的词项，按第一次出现的顺序 })
```

## 基本操作

1. 读文件。
2. 把第一个一级标题记成标题。
3. 把其余正文按空白切开，去掉重复的词，按第一次出现的顺序记成词项。

## apis.viba

```viba apis
import parse.types as parse


Parse =
     parse.Document
  <- $path (str * { 文档文件的路径 })
  <- {
    解析：读出一篇文档的标题与词项
  }
```
