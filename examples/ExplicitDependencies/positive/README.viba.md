# 文档站构建器

## 需求背景

输入是一个 Markdown 目录的路径 `$root`；操作有两类：解析单个页面，把整个目录构建成一份可以发布的文档。本示例是 ExplicitDependencies 的正例：`Build` 依赖 `Parse`，依赖在签名里写成参数，不藏在提示块里。

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
  * $pages (list[parse.Page] * { 解析出来的页面，顺序与目录一致 })
```

## 基本操作

1. 把目录里的每个 Markdown 文件交给 `Parse`。
2. 按一级标题把页面排成目录树。
3. 拼成一份 HTML 文档。

## apis.viba

```bash apis
import readme.types as readme
import parse.public as parse


Build =
     readme.Site
  <- $root (str * { Markdown 目录的路径 })
  <- {
    构建：把目录里的每个页面解析出来，按标题层级排成一份可以发布的文档
  }
  <- $parse (parse.Parse * { 解析：交回一个页面的标题与正文，用它排目录树 })
```
