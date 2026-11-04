# 文档站清理

## 需求背景

输入是文档站目录的路径 `$root` 与入口页的路径 `$entry`；操作有两类：扫描目录里的页面，删掉从入口页走不到的页面。本示例是 DeleteAllFileKinds 的反例：删除只按 `.viba.md` 页面一种文件做，没人引用的草稿 `draft.md` 留在目录里，图片也没有进遍历。

## public.viba

```bash public
import readme.types as readme
import readme.apis as readme_api

PruneReport = readme.PruneReport

Prune = readme_api.Prune
```

## types.viba

```bash types
import scan.public as scan


PruneReport =
  Object
  * $kept (list[scan.Page] * { 从入口页走得到的页面 })
  * $removed (list[scan.Page] * { 删掉的页面：从入口页走不到 })
```

## 基本操作

1. 扫描目录里的每个 `.viba.md` 页面。
2. 回答每个页面被谁引用：把引用它的页面路径记进 `$referenced_by`。
3. 从入口页出发，只算页面之间的引用，走得到的页面留下、走不到的页面删掉，交回保留与删除的页面清单；`draft.md` 与图片不在遍历里，留在目录里。

## apis.viba

```bash apis
import readme.types as readme
import scan.public as scan


Prune =
     readme.PruneReport
  <- $root (str * { 文档站目录的路径 })
  <- $entry (str * { 入口页的相对路径 })
  <- {
    清理：从入口页出发，只算页面之间的引用，走得到的页面留下、走不到的删掉，交回保留与删除的页面清单
  }
  <- $scan (scan.Scan * { 扫描：交回目录里的每个页面，带上引用它的页面路径，用它从入口页算可达性 })
```
