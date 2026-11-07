# 缓存存储

## 需求背景

输入是一个键 `$key`；操作是按键读缓存里的一条记录，交回读到的记录、没有记录或连不上缓存的原因。根 README 从这里取 `Entry` 与 `Read`。

## public.viba

```viba public
import cache.types as cache
import cache.apis as cache_api

Entry = cache.Entry

Reading = cache.Reading

Read = cache_api.Read
```

## types.viba

```viba types
Entry =
  Object
  * $key (str * { 记录的键 })
  * $value (str * { 记录的值 })
  * $expires_at (int * { 记录过期的时刻，Unix 秒 })

Reading =
  Oneof
  | $record_found (Entry * { 读到的记录 })
  | $no_record ($key str * { 没有记录的那个键 })
  | $cache_unreachable ($reason str * { 连不上缓存时给出的原因 })
```

## 基本操作

1. 按键在缓存里找记录。
2. 找到就交回记录。
3. 找不到就交回一条没有记录的结果。
4. 连不上缓存时，把原因交回。

## apis.viba

```viba apis
import cache.types as cache


Read =
     cache.Reading
  <- $key (str * { 要读的键 })
  <- {
    读：按键取一条记录，交回读到的记录、没有记录或连不上的原因
  }
```
