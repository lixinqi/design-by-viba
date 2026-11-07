# 归档写入

## 需求背景

输入是一个文件的路径 `$path` 和一份归档文件的路径 `$dest`；操作只有一类：把一个文件追加进归档，交回这个成员。根 README 从这里取 `Pack`。

## public.viba

```viba public
import archive.types as archive
import archive.apis as archive_api

Member = archive.Member

Pack = archive_api.Pack
```

## types.viba

```viba types
Member =
  Object
  * $path (str * { 写进归档的文件的路径 })
  * $bytes (int * { 这个文件写进归档的字节数 })
```

## 基本操作

1. 读出文件的全部内容。
2. 把内容追加到归档文件的末尾。
3. 记下文件路径与字节数，交回这个成员。

## apis.viba

```viba apis
import archive.types as archive


Pack =
     archive.Member
  <- $path (str * { 要写进归档的文件路径 })
  <- $dest (str * { 归档文件的路径 })
  <- {
    打包：把一个文件追加进归档，交回这个文件的路径与字节数
  }
```
