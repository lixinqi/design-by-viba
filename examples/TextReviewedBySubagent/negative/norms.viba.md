# 规范解析

## 需求背景

输入是一个规范文件的路径 `$path`；操作只有一类：读出这篇规范的名字与正文。`Parse` 只负责解析，不知道交付前如何审查。根 README 从这里取 `Norm` 与 `Parse`。

## public.viba

```viba public
import norms.types as norms
import norms.apis as norms_api

Norm = norms.Norm

Parse = norms_api.Parse
```

## types.viba

```viba types
Norm =
  Object
  * $name (str * { 规范名：文件名去掉 .md })
  * $text (str * { 规范的正文，原样保留 })
```

## 基本操作

1. 读规范文件。
2. 文件名去掉 `.md`，记成规范名。
3. 全文原样记成正文，连同规范名交回。

## apis.viba

```viba apis
import norms.types as norms


Parse =
     norms.Norm
  <- $path (str * { 规范文件的路径 })
  <- {
    解析：读出一篇规范的名字与正文，交回一条规范
  }
```
