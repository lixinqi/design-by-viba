# 文档站构建器

## 需求背景

输入是一个 Markdown 目录的路径 `$root`；操作有两类：把目录构建成一份可以发布的文档，检查页面里的链接。本示例是 PublicOnlyOwnNames 的反例：根文档的 public 把 check 文档 public 里的 `Check` 转发成自己的导出，而不只导出本文档的 `Site` 与 `Build`。

## public.viba

```viba public
import readme.types as readme
import readme.apis as readme_api
import check.public as check

Site = readme.Site

Build = readme_api.Build

Check = check.Check
```

## types.viba

```viba types
Site =
  Object
  * $pages (list[str] * { 发布出来的页面路径，顺序与目录一致 })
  * $broken (list[str] * { 页面里无法打开的链接，按出现顺序 })
```

## 基本操作

1. 把目录里的每个 Markdown 文件排成一个页面。
2. 把页面路径交给 `Check`，取回无法打开的链接。
3. 按一级标题把页面排成目录树，拼成一份 HTML 文档，连同页面路径与无法打开的链接一起交回。

## apis.viba

```viba apis
import readme.types as readme
import check.public as check

Build =
     readme.Site
  <- $root (str * { Markdown 目录的路径 })
  <- {
    构建：把目录里的每个页面排成可以发布的文档，检查页面里的链接，交回页面路径与无法打开的链接
  }
  <- $check (check.Check * { 检查：交回无法打开的链接，用它一起记进构建结果 })
```
