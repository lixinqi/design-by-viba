# 文档站构建

## 需求背景

输入是一个 Markdown 目录的路径 `$root`；操作只有一类：把整个目录构建成一份可以发布的站点。本示例是 SmallFunctions 的正例：`Build` 只负责串联，解析、排版、渲染分别由 `Parse`、`Arrange`、`Render` 三个短操作完成。

## public.viba

```viba public
import readme.types as readme
import readme.apis as readme_api

Site = readme.Site

Build = readme_api.Build
```

## types.viba

```viba types
Site =
  Object
  * $html (str * { 整站拼好的 HTML，可以直接发布 })
```

## 基本操作

1. 把目录路径交给 `Read`，收下每个文件的路径与原文。
2. 把每份草稿交给 `Parse`，收下它交回的页面。
3. 把页面清单交给 `Arrange`，按标题排成目录顺序。
4. 把排好的页面交给 `Render`，拼成整站 HTML。
5. 把 HTML 记成 `Site` 交回。

## apis.viba

```viba apis
import readme.types as readme
import read.public as read
import page.public as page


Build =
     readme.Site
  <- $root (str * { Markdown 目录的路径 })
  <- {
    构建：把目录里的文件依次读取、解析、排版、渲染，交回一份可以发布的站点
  }
  <- $read (read.Read * { 读取：交回目录里每个文件的路径与原文，用它逐个解析 })
  <- $parse (page.Parse * { 解析：交回一个页面的标题与正文，用它排好页面顺序 })
  <- $arrange (page.Arrange * { 排版：交回按标题排好的页面，用它决定渲染顺序 })
  <- $render (page.Render * { 渲染：交回整站拼好的 HTML，用它填进站点 })
```
