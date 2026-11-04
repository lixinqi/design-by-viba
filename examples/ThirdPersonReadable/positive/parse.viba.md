# 笔记解析

## 需求背景

输入是一篇 Markdown 笔记的路径 `$path`；操作是把第一个一级标题读成标题，其余内容读成正文，交回一个页面。根 README 从这里取 `Parse`。

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
  * $body (str * { 标题以下的正文 })
```

## 基本操作

1. 读文件。
2. 把第一个一级标题记成标题。
3. 其余内容记成正文。

## apis.viba

```bash apis
import parse.types as parse


Parse =
     parse.Page
  <- $path (str * { Markdown 笔记的路径 })
  <- {
    解析：读出一篇笔记的标题与正文，交回一个页面
  }
```
