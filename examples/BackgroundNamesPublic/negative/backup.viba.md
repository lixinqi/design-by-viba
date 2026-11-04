# 快照备份与恢复

## 需求背景

输入是一个源目录的路径 `$source`、一个归档目录的路径 `$archive` 与一个恢复目标目录的路径 `$target`；操作有两类：把源目录存成一份快照，把一份快照恢复到目标目录。

## public.viba

```bash public
import backup.types as backup
import backup.apis as backup_api

Snapshot = backup.Snapshot

Backup = backup_api.Backup

Restore = backup_api.Restore
```

## types.viba

```bash types
Snapshot =
  Object
  * $name (str * { 快照的名字，按归档目录里的建立次序编号 })
  * $source (str * { 建这份快照时读的源目录路径 })
  * $archive (str * { 存放这份快照的归档目录路径 })
  * $files (list[str] * { 快照里记下的文件，按相对源目录的路径排列 })
```

## 基本操作

1. 按归档目录里已有的快照给新快照编号。
2. 把源目录里的文件按相对路径记进快照，放进归档目录。
3. 恢复时按快照记下的路径把文件写进目标目录，交回文件清单。

## apis.viba

```bash apis
import backup.types as backup


Backup =
     backup.Snapshot
  <- $source (str * { 源目录的路径 })
  <- $archive (str * { 归档目录的路径 })
  <- {
    备份：把源目录里的文件记成一份快照放进归档目录，交回这份快照
  }

Restore =
     list[str]
  <- $snapshot (backup.Snapshot * { 要恢复的快照 })
  <- $target (str * { 恢复目标目录的路径 })
  <- {
    恢复：把快照里记下的文件写进目标目录，交回恢复出来的文件清单
  }
```
