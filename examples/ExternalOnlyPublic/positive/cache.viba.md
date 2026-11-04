# 缓存存储

## 需求背景

输入是一条条目，由缓存键、值与有效期组成；操作是写入一条条目：把条目记进缓存，交回写好的条目。根 README 从这里取 `Entry` 与 `Cache`。

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
  * $key (str * { 缓存键，全局唯一 })
  * $value (str * { 缓存里的值 })
  * $ttl (int * { 有效期，单位秒 })
```

## 基本操作

1. 读入缓存键、值与有效期。
2. 把三者记进缓存。
3. 交回写好的条目。

## apis.viba

```bash apis
import cache.types as cache

Cache =
     cache.Entry
  <- $entry (cache.Entry * { 条目：键、值与有效期 })
  <- {
    写入：把条目记进缓存，交回写好的条目
  }
```
