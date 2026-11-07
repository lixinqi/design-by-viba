# 缓存加载

## 需求背景

输入是一个仓库目录的路径 `$root`；操作有两类：把目录里的文档装进缓存，数出装进缓存的篇数与加载失败的篇数。根 README 从这里取 `Loaded` 与 `Load`。

## public.viba

```viba public
import cache.types as cache
import cache.apis as cache_api

Loaded = cache.Loaded

Load = cache_api.Load
```

## types.viba

```viba types
Loaded =
  Object
  * $loaded (int * { 本轮装进缓存的文档数 })
  * $failed (int * { 本轮加载失败的文档数 })
  * $evidence (str * { 失败文档的路径与错误，全部加载时为空串 })
```

## 基本操作

1. 枚举仓库目录里的每篇文档。
2. 逐篇装进缓存。
3. 数出装进缓存的篇数，把失败文档的路径与错误记成证据。

## apis.viba

```viba apis
import cache.types as cache


Load =
     cache.Loaded
  <- $root (str * { 待检查仓库的目录路径 })
  <- {
    加载：把目录里的文档逐篇装进缓存，交回装进缓存与加载失败的篇数，以及失败文档的位置
  }
```
