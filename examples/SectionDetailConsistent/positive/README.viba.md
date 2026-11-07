# 文档站装配

## 需求背景

输入是一个文档目录的路径 `$root`；操作有两类：解析单个页面，把目录里的页面装配成一份站点。本示例是 SectionDetailConsistent 的正例：README 与 parse 两篇的各节都停在操作与数据这一层，没有哪一节单独落进实现细节。

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
  * $title (str * { 站点标题，取文档目录的名字 })
  * $pages (list[parse.Page] * { 解析出来的页面，按文件名的升序排列；没有一级标题的页面不进清单 })
```

## 基本操作

1. 读文档目录，取出每篇 `.viba.md` 文档的路径。
2. 逐篇交给 `Parse`，取回页面的标题与正文。
3. 用文档目录的名字作站点标题，把全部页面按文件名的升序排进清单。
4. 交回装好的 `Site`。

## apis.viba

```viba apis
import readme.types as readme
import parse.public as parse


Build =
     readme.Site
  <- $root (str * { 文档目录的路径 })
  <- {
    装配：把文档目录里的页面排成一份站点，交回站点标题与排好的页面清单
  }
  <- $parse (parse.Parse * { 解析：交回一个页面的标题与正文，用它逐个装配目录里的页面 })
```
