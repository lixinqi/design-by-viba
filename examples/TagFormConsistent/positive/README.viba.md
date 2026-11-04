# 缓存检查

## 需求背景

输入是一个键 `$key` 与检查的时刻 `$now`；操作有两类：从缓存里读这个键的记录；比较记录过期的时刻与检查的时刻，判断缓存能否直接服务。本示例是 TagFormConsistent 的正例：`Problem` 的三个变体都写成情况描述（`$cache_miss`、`$stale_entry`、`$read_failed`）。

## public.viba

```bash public
import readme.types as readme
import readme.apis as readme_api

Problem = readme.Problem

Inspection = readme.Inspection

Inspect = readme_api.Inspect
```

## types.viba

```bash types
import cache.public as cache


Problem =
  Oneof
  | $cache_miss ($key str * { 缓存里没有这个键的记录 })
  | $stale_entry (cache.Entry * { 缓存里那条已经过期的记录 })
  | $read_failed ($reason str * { 连不上缓存时给出的原因 })

Inspection =
  Object
  * $key (str * { 检查的键 })
  * $problems (list[Problem] * { 检查出的问题；空列表表示缓存里有一条未过期的记录 })
```

## 基本操作

1. 把键交给 `Read`。
2. 没有记录时，记一条未命中的 `Problem`。
3. 读到记录时，比较记录过期的时刻与检查的时刻：过期就记一条记录过期的 `Problem`。
4. 连不上缓存时，把原因记成一条读取失败的 `Problem`。
5. 把键与 `Problem` 清单收进 `Inspection`。

## apis.viba

```bash apis
import readme.types as readme
import cache.public as cache


Inspect =
     readme.Inspection
  <- $key (str * { 要检查的键 })
  <- $now (int * { 检查的时刻，Unix 秒 })
  <- {
    检查：读出这个键在缓存里的记录，按检查的时刻判断记录是否过期，交回这个键与缓存不能直接服务的问题清单
  }
  <- $read (cache.Read * { 读缓存：交回读到的记录、没有记录或连不上的原因，用它判断 })
```
