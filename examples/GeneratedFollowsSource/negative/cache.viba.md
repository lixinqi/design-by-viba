# 缓存设置

## 需求背景

输入是一份缓存设置，由有效期、条目上限与命名空间组成；操作类别是应用设置：把缓存设置写进缓存服务，交回生效的设置。根 README 从这里取 `Settings` 与 `Apply`。

## public.viba

```viba public
import cache.types as cache
import cache.apis as cache_api

Settings = cache.Settings

Apply = cache_api.Apply
```

## types.viba

```viba types
Settings =
  Object
  * $ttl_seconds (int * { 每条缓存条目的有效期，单位秒 })
  * $max_entries (int * { 缓存最多保留的条目数 })
  * $namespace (str * { 缓存键的命名空间，同一命名空间内键唯一 })
```

## 基本操作

1. 读入一份缓存设置，里面是有效期、条目上限与命名空间。
2. 把缓存设置写进缓存服务。
3. 交回生效的设置。

## apis.viba

```viba apis
import cache.types as cache


Apply =
     cache.Settings
  <- $settings (cache.Settings * { 缓存设置：有效期、条目上限与命名空间 })
  <- {
    应用：把一份缓存设置写进缓存服务，交回生效的设置
  }
```
