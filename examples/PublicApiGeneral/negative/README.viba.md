# 缓存站点构建

## 需求背景

输入是一个 Markdown 目录的路径 `$root`；操作有两类：把目录里的页面构建成一份站点，把一个页面的正文写进缓存。本示例是 PublicApiGeneral 的反例：`Build` 收一个 `dict[str, str]`，把缓存内部的存储布局暴露给调用方。

## public.viba

```viba public
import readme.types as readme
import readme.apis as readme_api

Site = readme.Site

Build = readme_api.Build
```

## types.viba

```viba types
import cache.public as cache


Site =
  Object
  * $pages (list[str] * { 构建出来的页面路径，顺序与目录一致 })
  * $entries (list[cache.Entry] * { 写进缓存的页面记录，顺序与页面一致 })
```

## 基本操作

1. 读目录里的每个 Markdown 文件，按文件路径排好。
2. 按文件路径算出每个页面的缓存键。
3. 把页面正文按键写进缓存。
4. 把页面路径与写下的缓存记录收进 `Site`，交回。

## apis.viba

```viba apis
import readme.types as readme


Build =
     readme.Site
  <- $root (str * { Markdown 目录的路径 })
  <- $store (dict[str, str] * { 缓存内部的存储内容，键是缓存键，值是页面正文，用它把正文写进去 })
  <- {
    构建：把目录里的每个页面正文写进缓存，交回页面路径与缓存记录
  }
```
