# 渲染缓存

## 需求背景

输入是一个缓存键 `$key` 与一段渲染好的提示文本；操作有两类：按键查已有的条目，把一条条目存进缓存。根 README 从这里取 `Entry`、`Lookup` 与 `Store`。

## public.viba

```viba public
import cache.types as cache
import cache.apis as cache_api

Entry = cache.Entry

Lookup = cache_api.Lookup

Store = cache_api.Store
```

## types.viba

```viba types
Entry =
  Object
  * $key (str * { 模板路径与变量表算出的键 })
  * $text (str * { 渲染好、可以直接使用的提示文本 })
```

## 基本操作

1. 按键在缓存里找条目。
2. 找到就交回那一条，没有就交回空列表。
3. 存的时候把键与文本记成一条 `Entry`，交回存好的条目。

## apis.viba

```viba apis
import cache.types as cache


Lookup =
     list[cache.Entry]
  <- $key (str * { 模板路径与变量表算出的键 })
  <- {
    查缓存：交回同一个键下的条目，没有就是空列表
  }

Store =
     cache.Entry
  <- $key (str * { 模板路径与变量表算出的键 })
  <- $text (str * { 渲染好、可以直接使用的提示文本 })
  <- {
    存缓存：把键与文本记成一条条目，交回存好的条目
  }
```
