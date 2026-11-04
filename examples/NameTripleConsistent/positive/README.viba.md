# 文档站构建器

## 需求背景

输入是一个 Markdown 目录的路径 `$root`；操作类别是构建：把目录里的页面按标题层级排成一份可以发布的文档站，交回文档站的页面清单与 HTML。本示例是 NameTripleConsistent 的正例：parse.viba.md 的文件名是 parse，需求背景讲页面解析，public 导出 `Parse`，三处一致。

## public.viba

```bash public
import readme.types as readme
import readme.apis as readme_api

Site = readme.Site

Build = readme_api.Build
```

## types.viba

```bash types
import parse.public as parse


Site =
  Object
  * $pages (list[parse.Page] * { 文档站的页面，按标题层级排好 })
  * $html (str * { 按目录树拼好的 HTML，可以直接发布 })
```

## 基本操作

1. 收下 Markdown 目录的路径。
2. 把目录里的每个文件交给 `Parse`，收下它交回的页面。
3. 按一级标题把页面排成目录树。
4. 按目录树拼成 HTML，交回文档站的页面清单与 HTML。

## apis.viba

```bash apis
import readme.types as readme
import parse.public as parse


Build =
     readme.Site
  <- $root (str * { Markdown 目录的路径 })
  <- {
    构建：把目录里的页面按标题层级排出目录树并拼成 HTML，交回文档站的页面清单与 HTML
  }
  <- $parse (parse.Parse * { 解析：交回一个页面的标题与正文，用它排目录树 })
```
