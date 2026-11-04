# 上传处理

## 需求背景

输入是一次上传请求 `$upload`，含文件名、声明的校验和与内容；操作有两类：校验内容，把内容存进缓存并交回上传结果。本示例是 InnerSumForFailures 的反例：`UploadResult` 没有把失败收进内层和类型，而是把 `$ok`、`$too_large`、`$checksum_mismatch` 平铺在同一个和类型里；同一语义位置的失败每增加一种，外层就多一个变体。

## public.viba

```bash public
import readme.types as readme
import readme.apis as readme_api

UploadRequest = readme.UploadRequest

Stored = readme.Stored

UploadResult = readme.UploadResult

Upload = readme_api.Upload
```

## types.viba

```bash types
import check.public as check


UploadRequest =
  Object
  * $name (str * { 文件名，含扩展名 })
  * $checksum (str * { 声明的校验和 })
  * $content (str * { 上传的内容 })

Stored =
  Object
  * $key (str * { 内容在缓存里的键 })
  * $size (int * { 内容的字节数 })

UploadResult =
  Oneof
  | $ok (Stored * { 内容已经存进缓存 })
  | $too_large (check.TooLarge * { 内容超过允许的大小 })
  | $checksum_mismatch (check.ChecksumMismatch * { 内容与声明的校验和不一致 })
```

## 基本操作

1. 从请求里取出文件名、声明的校验和与内容。
2. 把声明的校验和与内容交给 `Check`，取回这次上传的失败原因。
3. 没有失败原因就把内容存进缓存；有失败原因就把原因记进结果。
4. 交回 `UploadResult`。

## apis.viba

```bash apis
import readme.types as readme
import check.public as check


Upload =
     readme.UploadResult
  <- $upload (readme.UploadRequest * { 一次上传请求：文件名、声明的校验和与内容 })
  <- {
    上传：把内容交给校验，通过就存进缓存，交回一次上传的结果
  }
  <- $check (check.Check * { 校验：交回这次上传的失败原因，用它决定结果记成 `$ok` 还是失败变体 })
```
