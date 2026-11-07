# 目录备份器

## 需求背景

输入是一个目录的路径 `$root` 和一份归档文件的路径 `$dest`；操作有两类：把单个文件写进归档，把整个目录备份成一份归档并交回备份清单。本示例是 RootApiIsRealOperation 的正例：根 public 导出 `Backup`，它独立执行就完成一次备份并交回备份清单。

## public.viba

```viba public
import readme.types as readme
import readme.apis as readme_api

Manifest = readme.Manifest

Backup = readme_api.Backup
```

## types.viba

```viba types
import archive.public as archive


Manifest =
  Object
  * $members (list[archive.Member] * { 写进归档的文件，顺序与写入顺序一致 })
  * $total_bytes (int * { 全部文件写进归档的字节数之和 })
```

## 基本操作

1. 走一遍目录，拿到每个文件的路径。
2. 把每个文件交给 `Pack`，追加进归档。
3. 把每个成员的路径与字节数记成备份清单，连同总字节数一起交回。

## apis.viba

```viba apis
import readme.types as readme
import archive.public as archive


Backup =
     readme.Manifest
  <- $root (str * { 要备份的目录路径 })
  <- $dest (str * { 归档写到的路径 })
  <- {
    备份：把目录里的每个文件写进归档，交回这份归档的备份清单
  }
  <- $pack (archive.Pack * { 打包：把一个文件写进归档并交回成员，用它记备份清单 })
```
