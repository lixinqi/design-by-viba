# 目录读取

## 需求背景

输入是一个 Markdown 目录的路径 `$root`；操作只有一类：读出目录里每个 Markdown 文件的路径与原文。根 README 从这里取 `Read`。

## public.viba

```viba public
import read.types as read
import read.apis as read_api

Draft = read.Draft

Read = read_api.Read
```

## types.viba

```viba types
Draft =
  Object
  * $path (str * { 文件在目录里的路径 })
  * $text (str * { 文件的原文，标题与正文原样保留 })
```

## 基本操作

1. 读目录，拿到目录里的每个 Markdown 文件。
2. 逐个读出文件的路径与原文。
3. 把每份原文记成一条 `Draft`，交回草稿清单。

## apis.viba

```viba apis
import read.types as read


Read =
     list[read.Draft]
  <- $root (str * { Markdown 目录的路径 })
  <- {
    读取：读出目录里每个 Markdown 文件的路径与原文，交回草稿清单
  }
```
