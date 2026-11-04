# 备份演练

## 需求背景

输入是一个源目录的路径 `$source`、一个归档目录的路径 `$archive` 与一个恢复目标目录的路径 `$target`；操作有两类：把源目录备份成一份快照，把快照恢复到目标目录并核对恢复出来的文件。本示例是 BackgroundNamesPublic 的正例：backup.viba.md 的需求背景收尾写出根 README 从这里取 `Snapshot`、`Backup` 与 `Restore`，与它的 public 导出行逐条对得上。

## public.viba

```bash public
import readme.types as readme
import readme.apis as readme_api

DrillReport = readme.DrillReport

RunDrill = readme_api.RunDrill
```

## types.viba

```bash types
import backup.public as backup


DrillReport =
  Object
  * $snapshot (backup.Snapshot * { 这次演练建出的快照 })
  * $files (list[str] * { 从快照恢复出来的文件，按目标目录里的相对路径排列 })
  * $checked (bool * { 恢复出来的文件与快照里记下的文件一致 })
```

## 基本操作

1. 把源目录与归档目录交给 `Backup`，收下它交回的快照。
2. 把快照与目标目录交给 `Restore`，收下它交回的文件清单。
3. 对照快照里记下的文件核对这份清单，交回演练报告。

## apis.viba

```bash apis
import readme.types as readme
import backup.public as backup


RunDrill =
     readme.DrillReport
  <- $source (str * { 源目录的路径 })
  <- $archive (str * { 归档目录的路径 })
  <- $target (str * { 恢复目标目录的路径 })
  <- {
    演练：把源目录备份成一份快照，再把它恢复到目标目录并核对文件，交回这次演练的报告
  }
  <- $backup (backup.Backup * { 备份：把源目录存成一份快照，用它作为恢复的来源 })
  <- $restore (backup.Restore * { 恢复：把一份快照恢复到目标目录，交回恢复出来的文件清单 })
```
