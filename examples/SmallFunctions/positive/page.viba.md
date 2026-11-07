# 页面解析、排版与渲染

## 需求背景

输入是一份草稿 `$draft` 与一份页面清单 `$pages`；操作有三类：把草稿解析成一个页面，把页面按标题排成目录顺序，把排好的页面拼成整站 HTML。根 README 从这里取 `Parse`、`Arrange` 与 `Render`。

## public.viba

```viba public
import page.types as page
import page.apis as page_api

Page = page.Page

Parse = page_api.Parse

Arrange = page_api.Arrange

Render = page_api.Render
```

## types.viba

```viba types
Page =
  Object
  * $title (str * { 页面的一级标题；文件没有一级标题时取文件名 })
  * $body (str * { 标题以下的正文 })
```

## 基本操作

1. 解析：把草稿的第一个一级标题记成标题，其余内容记成正文；没有一级标题时用文件名去掉扩展名顶上。
2. 排版：把页面按标题排成目录顺序；标题重复时保留读到的先后。
3. 渲染：把排好的页面依次拼成整站 HTML；正文为空时留一个占位。

## apis.viba

```viba apis
import page.types as page
import read.public as read


Parse =
     page.Page
  <- $draft (read.Draft * { 要解析的文件：路径与原文 })
  <- {
    解析：读出一级标题与其余正文，没有一级标题时用文件名顶上，交回一个页面
  }

Arrange =
     list[page.Page]
  <- $pages (list[page.Page] * { 解析出来的页面 })
  <- {
    排版：把页面按标题排成目录顺序，标题重复时保留读到的先后，交回排好的页面清单
  }

Render =
     str
  <- $pages (list[page.Page] * { 排好顺序的页面 })
  <- {
    渲染：把页面依次拼成整站 HTML，正文为空时留一个占位，交回可以直接发布的文本
  }
```
