# 目录备份器

## 需求背景

输入是一个目录的路径 `$root` 和一份归档文件的路径 `$dest`；操作有两类：把单个文件写进归档，把整个目录备份成一份归档并交回备份清单。本示例是 RootApiIsRealOperation 的反例：根 public 只导出 `Read` 与 `List` 两个操作，一个读出文件内容，一个列出目录里的文件，没有任何操作能完成备份并交回备份清单。

## public.viba

```bash public
import readme.types as readme
import readme.apis as readme_api

Manifest = readme.Manifest

Read = readme_api.Read

List = readme_api.List
```

## types.viba

```bash types
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

```bash apis
Read =
     str
  <- $path (str * { 文件的路径 })
  <- {
    读取：读出文件的全部内容，交回这段内容
  }

List =
     list[str]
  <- $root (str * { 目录的路径 })
  <- {
    列举：列出目录里每个文件的路径，交回这些路径
  }
```
