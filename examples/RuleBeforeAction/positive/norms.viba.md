# 规范库读写

## 需求背景

输入是规范库目录的路径 `$root` 与一篇规范的名字 `$name`；操作有两类：读出库里每篇规范，删掉一篇指定的规范。`Load` 与 `Delete` 只负责读写文件，不判断哪篇该删。根 README 从这里取 `Norm`、`Load` 与 `Delete`。

## public.viba

```viba public
import norms.types as norms
import norms.apis as norms_api

Norm = norms.Norm

Load = norms_api.Load

Delete = norms_api.Delete
```

## types.viba

```viba types
Norm =
  Object
  * $name (str * { 规范名，取文件名去掉 .md })
  * $retired (bool * { 规范自己标了作废时为 true })
  * $replaced_by (str * { 取代它的规范名；没有被取代时为空串 })
  * $referenced_by (list[str] * { 引用它的规范名；空列表表示没有引用者 })
```

## 基本操作

1. 读目录，每篇规范是一个 Markdown 文件，文件名去掉 `.md` 记成规范名。
2. 读每篇规范的头部字段：作废标记、取代它的规范名、引用它的规范名。
3. 按名字删一篇规范，交回剩下的规范清单。

## apis.viba

```viba apis
import norms.types as norms


Load =
     list[norms.Norm]
  <- $root (str * { 规范库目录的路径 })
  <- {
    读库：读出目录里的每篇规范，交回规范清单，顺序与文件名一致
  }

Delete =
     list[norms.Norm]
  <- $root (str * { 规范库目录的路径 })
  <- $name (str * { 要删的规范名 })
  <- {
    删文件：按名字删掉这篇规范，交回剩下的规范清单
  }
```
