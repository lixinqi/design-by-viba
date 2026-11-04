# 页面解析

## 需求背景

输入是一个 Markdown 文件的路径 `$path`；操作是把第一个一级标题记成标题，其余内容记成正文。根 README 从这里取 `Page` 与 `Parse`。

## public.viba

```bash public
import parse.types as parse
import parse.apis as parse_api

Page = parse.Page

Parse = parse_api.Parse
```

## types.viba

```bash types
Page =
  Object
  * $title (str * { 第一个一级标题 })
  * $body (str * { 标题之后的正文 })
```

## 基本操作

1. 读入 `$path` 指向的 Markdown 文件。
2. 找到第一个一级标题，把它的文本记成标题。
3. 把标题之后的内容记成正文。

## apis.viba

```bash apis
import parse.types as parse


Parse =
     parse.Page
  <- $path (str * { Markdown 文件的路径 })
  <- {
    解析：把第一个一级标题记成标题、其余内容记成正文，交回这个页面
  }
```
