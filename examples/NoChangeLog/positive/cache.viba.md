# 配置缓存

## 需求背景

输入是一个配置文件的路径 `$path`；操作只有一类：按这个路径交回缓存里保存的默认值。`Restore` 只负责取默认值，缺了哪些项由根 README 判断。根 README 从这里取 `Entry` 与 `Restore`。

## public.viba

```viba public
import cache.types as cache
import cache.apis as cache_api

Entry = cache.Entry

Restore = cache_api.Restore
```

## types.viba

```viba types
Entry =
  Object
  * $name (str * { 配置项名 })
  * $value (str * { 配置项的值，也就是它的默认值 })
```

## 基本操作

1. 按配置文件的路径找这份配置的默认值记录。
2. 把记录里的每一项记成一个配置项。
3. 按记录里的先后把默认值交回。

## apis.viba

```viba apis
import cache.types as cache


Restore =
     list[cache.Entry]
  <- $path (str * { 配置文件的路径 })
  <- {
    恢复：按配置文件的路径交回缓存里保存的默认值，按记录里的先后排列
  }
```
