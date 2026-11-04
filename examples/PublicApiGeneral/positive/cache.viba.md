# 缓存写入

## 需求背景

输入是一个缓存键 `$key`、一个页面的路径 `$page` 与页面正文 `$body`；操作只有一类：把这一页的正文按键写进缓存，交回写下的记录。`Cache` 只负责写一页，目录如何遍历由根 README 决定。根 README 从这里取 `Entry` 与 `Cache`。

## public.viba

```bash public
import cache.types as cache
import cache.apis as cache_api

Entry = cache.Entry

Cache = cache_api.Cache
```

## types.viba

```bash types
Entry =
  Object
  * $key (str * { 缓存里这条记录用的键 })
  * $page (str * { 这条记录存放的页面路径 })
```

## 基本操作

1. 按缓存键在缓存里找记录。
2. 没有记录就新建一条。
3. 把页面正文写进缓存里这条记录。
4. 交回这条记录的键与页面路径。

## apis.viba

```bash apis
import cache.types as cache


Cache =
     cache.Entry
  <- $key (str * { 要写的缓存键 })
  <- $page (str * { 页面路径 })
  <- $body (str * { 要缓存的页面正文 })
  <- {
    缓存：把页面正文按键写进缓存，交回写下的键与页面路径
  }
```
