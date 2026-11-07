# 目录扫描

## 需求背景

输入是文档站目录的路径 `$root`；操作是读出目录里的每个 `.viba.md` 页面，记下路径与引用它的页面路径。本示例是 DeleteAllFileKinds 反例的依赖方：`Scan` 只读页面，`draft.md` 与图片不进清单，删除只覆盖页面一种文件。根 README 从这里取 `Page` 与 `Scan`。

## public.viba

```viba public
import scan.types as scan
import scan.apis as scan_api

Page = scan.Page

Scan = scan_api.Scan
```

## types.viba

```viba types
Page =
  Object
  * $path (str * { 页面的相对路径，以 .viba.md 结尾 })
  * $referenced_by (list[str] * { 引用这个页面的页面路径；空列表表示没人依赖 })
```

## 基本操作

1. 读目录，列出每个 `.viba.md` 页面的相对路径。
2. 读每个页面的内容，找出它引用的其他页面路径。
3. 把引用它的页面路径记成 `$referenced_by`，交回页面清单。

## apis.viba

```viba apis
import scan.types as scan


Scan =
     list[scan.Page]
  <- $root (str * { 文档站目录的路径 })
  <- {
    扫描：读出目录里的每个页面与引用它的页面路径，交回页面清单
  }
```
