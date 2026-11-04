# 文档站页面构建

## 需求背景

输入是一个 Markdown 文件的路径 `$path`；操作类别是构建文档站：把文件构建成站点里的一页，交回这一页的标题与正文。根 README 从这里取 `Page` 与 `Build`。

## public.viba

```bash public
import parse.types as parse
import parse.apis as parse_api

Page = parse.Page

Build = parse_api.Build
```

## types.viba

```bash types
Page =
  Object
  * $title (str * { 页面的一级标题 })
  * $body (str * { 标题以下的正文 })
```

## 基本操作

1. 读入 Markdown 文件。
2. 把第一个一级标题记成标题。
3. 其余内容记成正文。
4. 交回这一页的标题与正文。

## apis.viba

```bash apis
import parse.types as parse


Build =
     parse.Page
  <- $path (str * { Markdown 文件的路径 })
  <- {
    构建：把文件构建成文档站里的一页，交回这一页的标题与正文
  }
```
