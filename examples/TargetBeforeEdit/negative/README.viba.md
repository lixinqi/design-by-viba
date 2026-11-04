# 团队规范修订

## 需求背景

输入是规范库目录的路径 `$root` 与一条改动请求 `$change`；操作类别是修订：按改动清单改目标文件，交回改的变更与逐文件的 diff。本示例是 TargetBeforeEdit 的反例：`$target` 写成文件名 `parse.viba.md`，规范库里的两个同名文件都算它，diff 里还多了 `drafts/cache.viba.md`。

## public.viba

```bash public
import readme.types as readme
import readme.apis as readme_api

Revision = readme.Revision

Revise = readme_api.Revise
```

## types.viba

```bash types
import change.public as change


Revision =
  Object
  * $change (change.Change * { 改的那条变更请求：目标文件与改动清单 })
  * $diff (list[change.DiffFile] * { 改后的逐文件 diff })
```

## 基本操作

1. 从改动请求里取出 `$target` 与改动清单。
2. 把规范库目录与改动请求交给 `Apply`。
3. 收下改的变更与逐文件的 diff，记成修订。

## apis.viba

```bash apis
import readme.types as readme
import change.public as change


Revise =
     readme.Revision
  <- $root (str * { 规范库目录的路径 })
  <- $change (change.Change * { 要改的目标与改动清单 })
  <- {
    修订：按改动清单改 `$target` 指向的文件，交回改的变更与逐文件的 diff
  }
  <- $apply (change.Apply * { 改：按改动清单改目标文件，交回改的变更与逐文件的 diff，用它记成修订 })
```
