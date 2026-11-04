# 目录扫描

## 需求背景

输入是文档站目录的路径 `$root`；操作是读出目录里的每个文件，记下路径与引用它的文件路径。本示例是 DeleteAllFileKinds 正例的依赖方：`Scan` 不看扩展名，页面、图片、草稿都读出来，每个文件都回答谁依赖它。根 README 从这里取 `File` 与 `Scan`。

## public.viba

```bash public
import scan.types as scan
import scan.apis as scan_api

File = scan.File

Scan = scan_api.Scan
```

## types.viba

```bash types
File =
  Object
  * $path (str * { 站点目录里的相对路径 })
  * $referenced_by (list[str] * { 引用这个文件的文件路径；空列表表示没人依赖 })
```

## 基本操作

1. 读目录，列出每个文件的相对路径，不看扩展名。
2. 读每个文件的内容，找出它引用的其他文件路径。
3. 把引用它的文件路径记成 `$referenced_by`，交回文件清单。

## apis.viba

```bash apis
import scan.types as scan


Scan =
     list[scan.File]
  <- $root (str * { 文档站目录的路径 })
  <- {
    扫描：读出目录里的每个文件与引用它的文件路径，交回文件清单
  }
```
