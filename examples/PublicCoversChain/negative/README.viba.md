# 文档站构建与预览

## 需求背景

输入是一个 Markdown 目录的路径 `$root` 与要预览的页面路径 `$path`；操作有两类：`Build` 负责把整个目录构建成一份可以发布的站点，`Preview` 负责预览单个页面。本示例是 PublicCoversChain 的反例：需求里的两个操作只有 `Build` 从根 public 导出，`Preview` 留在 `readme.apis` 里，从根 public 出发预览这一路走不到。

## public.viba

```viba public
import readme.types as readme
import readme.apis as readme_api

Site = readme.Site

Build = readme_api.Build
```

## types.viba

```viba types
import parse.public as parse


Site =
  Object
  * $pages (list[parse.Page] * { 解析出来的页面，顺序与目录一致 })
  * $html (str * { 排好目录树后拼成的 HTML，可以直接发布 })
```

## 基本操作

1. 构建时，把目录里的每个 Markdown 文件交给 `Parse`，收下它交回的页面。
2. 按一级标题把页面排成目录树，拼成整站的 HTML，交回页面清单与 HTML。
3. 预览单个页面时，把这一页交给 `Parse`，按站点的排版渲染成 HTML。

## apis.viba

```viba apis
import readme.types as readme
import parse.public as parse


Build =
     readme.Site
  <- $root (str * { Markdown 目录的路径 })
  <- {
    构建：把目录里的每个页面解析出来，按标题层级排成目录树，交回页面清单与拼好的 HTML
  }
  <- $parse (parse.Parse * { 解析：交回一个页面的来源、标题与正文，用它排目录树 })

Preview =
     str
  <- $path (str * { 要预览的 Markdown 文件路径 })
  <- {
    预览：把这一页解析出来，按站点的排版渲染，交回这一页的 HTML
  }
  <- $parse (parse.Parse * { 解析：交回一个页面的来源、标题与正文，用它渲染这一页 })
```
