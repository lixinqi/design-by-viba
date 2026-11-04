# 规范改动

## 需求背景

输入是规范库目录的路径 `$root` 与一条改动请求 `$change`；操作类别是改：按改动清单改目标文件，交回改的变更与逐文件的 diff。根 README 从这里取 `Change`、`DiffFile` 与 `Apply`。

## public.viba

```bash public
import change.types as change
import change.apis as change_api

Edit = change.Edit

Change = change.Change

DiffFile = change.DiffFile

AppliedChange = change.AppliedChange

Apply = change_api.Apply
```

## types.viba

```bash types
Edit =
  Object
  * $old (str * { 改动前的那段文字 })
  * $new (str * { 改动后替换成的文字 })

Change =
  Object
  * $target (str * { 要改的文件路径：`norms/parse.viba.md`；改前按文件名列出 `parse.viba.md` 的全部路径，规范库里还有 `drafts/parse.viba.md`，目标写全路径，只指 `norms/parse.viba.md` 这一个 })
  * $edits (list[Edit] * { 改动清单，每一项都只改 `$target` 这一个文件 })

DiffFile =
  Object
  * $path (str * { 改动落到哪个文件 })
  * $lines (int * { 这个文件改动的行数 })

AppliedChange =
  Object
  * $change (Change * { 改的那条变更请求：目标文件与改动清单 })
  * $diff (list[DiffFile] * { 逐文件核对之后的 diff：只有 `norms/parse.viba.md` 一个文件 })
```

## 基本操作

1. 收下规范库目录与改动请求。
2. 按改动清单改 `$target` 指向的文件。
3. 把改的变更与逐文件的 diff 记成 `AppliedChange`，交回它。

## apis.viba

```bash apis
import change.types as change


Apply =
     change.AppliedChange
  <- $root (str * { 规范库目录的路径 })
  <- $change (change.Change * { 要改的目标与改动清单 })
  <- {
    改：按改动清单改 `$target` 指向的文件，交回改的变更与逐文件的 diff
  }
```
