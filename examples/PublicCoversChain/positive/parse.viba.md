# 页面解析

## 需求背景

输入是一个 Markdown 文件的路径 `$path`；操作类别是解析：把第一个一级标题读成标题，其余内容读成正文，连同文件路径记成一个页面。根 README 从这里取 `Page` 与 `Parse`。

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
  * $source (str * { 这个页面来自的 Markdown 文件路径 })
  * $title (str * { 第一个一级标题 })
  * $body (str * { 标题以下的正文 })
```

## 基本操作

1. 读文件。
2. 把第一个一级标题记成标题。
3. 其余内容记成正文，连同文件路径记成 `Page`，交回这个页面。

## apis.viba

```bash apis
import parse.types as parse


Parse =
     parse.Page
  <- $path (str * { Markdown 文件的路径 })
  <- {
    解析：把第一个一级标题读成标题、其余内容读成正文，连同文件路径，交回这个页面
  }
```
