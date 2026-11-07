# 模板解析

## 需求背景

输入是一个模板文件的路径 `$path`；操作只有一类：读出模板里的占位符与原文。根 README 从这里取 `Template` 与 `Parse`。

## public.viba

```viba public
import parse.types as parse
import parse.apis as parse_api

Template = parse.Template

Parse = parse_api.Parse
```

## types.viba

```viba types
Template =
  Object
  * $placeholders (list[str] * { 模板里出现的占位符名，按首次出现的顺序排列 })
  * $source (str * { 模板原文，占位符原样保留 })
```

## 基本操作

1. 读模板文件。
2. 按出现顺序记下每个占位符名。
3. 把原文原样保留，连同占位符名收进 `Template`。

## apis.viba

```viba apis
import parse.types as parse


Parse =
     parse.Template
  <- $path (str * { 模板文件的路径 })
  <- {
    解析：读出模板里的占位符名与原文，交回一个模板
  }
```
