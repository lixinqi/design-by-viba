# 文档站装配

## 需求背景

输入是一个文档目录的路径 `$root`；操作有两类：解析单个页面，把目录里的页面装配成一份站点。本示例是 SectionMatchesHeading 的反例：根 README 的“基本操作”写成了 `Site` 的字段表与限制说明，没有列出装配的步骤。

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
  * $title (str * { 站点标题，取文档目录的名字 })
  * $pages (list[parse.Page] * { 解析出来的页面，按文件名的升序排列；没有一级标题的页面不进清单 })
```

## 基本操作

`Site` 只有两个字段：`$title` 与 `$pages`。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `$title` | `str` | 站点标题，取文档目录的名字 |
| `$pages` | `list[parse.Page]` | 解析出来的页面，按文件名的升序排列；没有一级标题的页面不进清单 |

限制说明：目录里只收 `.viba.md` 文档；页面标题只取第一个一级标题；没有一级标题的页面跳过，不进清单。

## apis.viba

```bash apis
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
