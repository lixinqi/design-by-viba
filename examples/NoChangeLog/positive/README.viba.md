# 服务配置加载

## 需求背景

输入是一个配置文件的路径 `$path`；操作有两类：把配置文件读成配置项，用缓存里的默认值补上配置文件里缺的项。缓存按配置文件的路径保存每个配置项的默认值。本示例是 NoChangeLog 的正例：需求背景只写现在是什么，变更写进提交信息。

## public.viba

```viba public
import readme.types as readme
import readme.apis as readme_api

Settings = readme.Settings

Load = readme_api.Load
```

## types.viba

```viba types
import cache.public as cache


Settings =
  Object
  * $entries (list[cache.Entry] * { 配置项，按配置文件里的先后排列 })
```

## 基本操作

1. 读配置文件，把每一项记成一个配置项。
2. 把配置文件的路径交给 `Restore`，收下缓存里保存的默认值。
3. 配置文件里缺的项，用收下的默认值补上。
4. 按配置文件里的先后把配置项排好，交回。

## apis.viba

```viba apis
import readme.types as readme
import cache.public as cache


Load =
     readme.Settings
  <- $path (str * { 配置文件的路径 })
  <- {
    加载：读出配置文件里的配置项，用缓存里的默认值补上缺的项，交回补全的配置
  }
  <- $cache (cache.Restore * { 恢复：交回缓存里保存的默认值，用它补上配置文件里缺的项 })
```
