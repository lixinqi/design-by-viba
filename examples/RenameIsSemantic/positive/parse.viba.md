# 页面解析

## 需求背景

输入是一个 Markdown 文件的路径 `$path`；操作是解析单个页面：把第一个一级标题读成标题，其余内容读成正文。本示例是 RenameIsSemantic 正例的依赖方：`Parse` 只解析页面，改名时检索操作的类型与提示也一起更新。根 README 从这里取 `Page` 与 `Parse`。

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
  * $body (str * { 标题以下的正文 })
```

## 基本操作

1. 读文件。
2. 把第一个一级标题记成标题。
3. 其余内容记成正文。

## apis.viba

```viba apis
import parse.types as parse


Parse =
     parse.Page
  <- $path (str * { Markdown 文件的路径 })
  <- {
    解析：读出一个页面的标题与正文
  }
```
