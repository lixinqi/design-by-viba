# 配置装载器

## 需求背景

输入是一份 JSON 配置文件的路径 `$path`；操作类别有两类：按生成的 `schema.json` 校验配置，把缓存设置写进缓存服务。`schema.json` 由 `Config` 与 `cache.Settings` 这两个对象定义生成。本示例是 GeneratedFollowsSource 的反例：`schema.json` 缺少 `cache.Settings` 的 `max_entries` 字段，没有跟着源头走。

## public.viba

```viba public
import readme.types as readme
import readme.apis as readme_api

Config = readme.Config

Load = readme_api.Load
```

## types.viba

```viba types
import cache.public as cache


Config =
  Object
  * $cache (cache.Settings * { 缓存设置，写进缓存服务后生效 })
  * $log_level (str * { 日志级别：debug、info、warn、error })
  * $workers (int * { 工作线程数，至少为 1 })
```

## 基本操作

1. 读入 JSON 配置文件。
2. 从 `Config` 与 `cache.Settings` 这两个对象定义生成 `schema.json`：每个字段对应一条属性，操作定义不进 schema；对象定义改动后重新生成。
3. 按 `schema.json` 校验配置。
4. 把 `cache` 字段交给 `cache.Apply`，写进缓存服务。
5. 交回生效的配置。

生成物是本仓库根目录的 `schema.json`，字段与上面的对象定义逐项对应。

## apis.viba

```viba apis
import readme.types as readme
import cache.public as cache


Load =
     readme.Config
  <- $path (str * { JSON 配置文件的路径 })
  <- {
    装载：按生成的 schema 校验配置文件，把缓存设置写进缓存服务，交回生效的配置
  }
  <- $apply (cache.Apply * { 应用：把一份缓存设置写进缓存服务并交回生效的设置，用它确认缓存已经就绪 })
```
