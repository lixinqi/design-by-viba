# 缓存写入服务

## 需求背景

输入是上游给出的一条条目，由缓存键、值与有效期组成；操作是写入一条条目：把条目交给缓存，交回一份回执。本示例是 ExternalOnlyPublic 的正例：`Store` 的 `$entry` 与 `Receipt` 的 `$entry` 都从 `cache.public` 取 `Entry`，`cache.types` 与 `cache.apis` 只在缓存文档内部使用。

## public.viba

```bash public
import readme.types as readme
import readme.apis as readme_api

Receipt = readme.Receipt

Store = readme_api.Store
```

## types.viba

```bash types
import cache.public as cache

Receipt =
  Object
  * $entry (cache.Entry * { 写进缓存的条目 })
  * $written_at (int * { 写进去的时刻，单位秒 })
```

## 基本操作

1. 从上游收下一条条目。
2. 把条目交给 `Cache`。
3. 把写好的条目与写入时刻记成回执。

## apis.viba

```bash apis
import readme.types as readme
import cache.public as cache

Store =
     readme.Receipt
  <- $entry (cache.Entry * { 条目：要写进缓存的键、值与有效期 })
  <- {
    写入：把一条条目交给缓存，交回写好的回执
  }
  <- $cache (cache.Cache * { 写入：交回写好的条目，用它把条目记进缓存 })
```
