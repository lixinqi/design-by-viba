# 页面解析

## 需求背景

输入是一个 Markdown 文件的路径 `$path`；操作是把第一个一级标题读成标题，其余内容读成正文。本示例是 ExplicitDependencies 反例的依赖方：`Parse` 存在，构建器却没有把它写成参数。根 README 从这里取 `Parse`。

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
