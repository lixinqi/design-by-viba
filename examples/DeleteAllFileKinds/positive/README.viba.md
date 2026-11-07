# 文档站清理

## 需求背景

输入是文档站目录的路径 `$root` 与入口页的路径 `$entry`；操作有两类：扫描目录里的文件，删掉从入口页走不到的文件。本示例是 DeleteAllFileKinds 的正例：删除不分文件类型：页面、图片、草稿都回答谁依赖它，按同一条可达性判据保留或删掉。

## public.viba

```viba public
import readme.types as readme
import readme.apis as readme_api

PruneReport = readme.PruneReport

Prune = readme_api.Prune
```

## types.viba

```viba types
import scan.public as scan


PruneReport =
  Object
  * $kept (list[scan.File] * { 从入口页走得到的文件，页面、图片、草稿都算 })
  * $removed (list[scan.File] * { 删掉的文件：从入口页走不到，页面、图片、草稿都可能出现 })
```

## 基本操作

1. 扫描目录里的每个文件，不看扩展名。
2. 回答每个文件被谁依赖：把引用它的文件路径记进 `$referenced_by`。
3. 从入口页出发，走得到的文件留下、走不到的文件删掉；页面、图片、草稿用同一条判据，交回保留与删除的清单。

## apis.viba

```viba apis
import readme.types as readme
import scan.public as scan


Prune =
     readme.PruneReport
  <- $root (str * { 文档站目录的路径 })
  <- $entry (str * { 入口页的相对路径 })
  <- {
    清理：从入口页出发，页面、图片、草稿用同一条可达性判据，走得到的文件留下、走不到的删掉，交回保留与删除的清单
  }
  <- $scan (scan.Scan * { 扫描：交回目录里的每个文件，带上引用它的文件路径，用它从入口页算可达性 })
```
