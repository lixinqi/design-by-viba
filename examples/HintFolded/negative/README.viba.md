# 配置加载

## 需求背景

输入是一个配置文件的路径 `$path`；操作有两类：校验一份配置文本，把一个配置文件读成配置并交回校验发现的违规条目。本示例是 HintFolded 的反例：`Validate` 的提示只有一句，却写成一行，没有折行。

## public.viba

```viba public
import readme.types as readme
import readme.apis as readme_api

Loaded = readme.Loaded

Load = readme_api.Load
```

## types.viba

```viba types
import validate.public as validate


Config =
  Object
  * $entries (dict[str, str] * { 每个配置项的名字与值 })

Loaded =
  Object
  * $config (Config * { 配置文件读成的配置 })
  * $violations (list[validate.Violation] * { 校验发现的违规条目，按配置项在文件里的先后排列 })
```

## 基本操作

1. 读配置文件。
2. 把文本交给 `Validate`，收下违规条目。
3. 把文本读成 `Config`，与违规条目一起交回。

## apis.viba

```viba apis
import readme.types as readme
import validate.public as validate


Load =
     readme.Loaded
  <- $path (str * { 配置文件的路径 })
  <- {
    加载：读出配置文件，交给校验，交回读成的配置与校验发现的违规条目
  }
  <- $validate (validate.Validate * { 校验：交回配置文本里的违规条目，用它决定配置是否可用 })
```
