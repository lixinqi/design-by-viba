# 解析检查

## 需求背景

输入是一个仓库目录的路径 `$root`；操作有两类：逐篇解析目录里的文档，把通过与失败的篇数记成检查结果。根 README 从这里取 `Parsed` 与 `Parse`。

## public.viba

```viba public
import parse.types as parse
import parse.apis as parse_api

Parsed = parse.Parsed

Parse = parse_api.Parse
```

## types.viba

```viba types
Parsed =
  Object
  * $passed (int * { 本轮解析通过的文档数 })
  * $failed (int * { 本轮解析失败的文档数 })
  * $evidence (str * { 失败文档的路径与错误，全部通过时为空串 })
```

## 基本操作

1. 枚举仓库目录里的每篇文档。
2. 逐篇送进解析器。
3. 数出通过的篇数，把失败文档的路径与错误记成证据。

## apis.viba

```viba apis
import parse.types as parse


Parse =
     parse.Parsed
  <- $root (str * { 待检查仓库的目录路径 })
  <- {
    解析：逐篇读目录里的文档，交回通过与失败的篇数，以及失败文档的位置
  }
```
