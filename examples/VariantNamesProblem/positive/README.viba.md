# 上传检查

## 需求背景

输入是一次上传请求 `$upload`，含文件名、上传内容与声明的 SHA-256 校验和；操作是检查一次上传：算出内容的校验和与字节数，核对字节数是否超过上限、校验和是否与声明一致，交回这次上传查出的问题清单。本示例是 VariantNamesProblem 的正例：把 `UploadFailure` 的变体代入“这条报的是___”，得到的是“文件太大”“校验和不一致”——都是这次上传遇到的问题，不是检查项的名字。

## public.viba

```bash public
import readme.types as readme
import readme.apis as readme_api

UploadRequest = readme.UploadRequest

UploadFailure = readme.UploadFailure

Inspection = readme.Inspection

Inspect = readme_api.Inspect
```

## types.viba

```bash types
import checksum.public as checksum


UploadRequest =
  Object
  * $name (str * { 文件名，含扩展名 })
  * $checksum (str * { 声明的 SHA-256 校验和，十六进制串 })
  * $content (str * { 上传的内容 })

TooLarge =
  Object
  * $limit (int * { 允许的最大字节数 })
  * $actual (int * { 内容的字节数 })

ChecksumMismatch =
  Object
  * $expected (str * { 请求里声明的校验和 })
  * $actual (checksum.Digest * { 从内容算出来的校验和 })

UploadFailure =
  Oneof
  | $too_large (TooLarge * { 内容超过允许的大小 })
  | $checksum_mismatch (ChecksumMismatch * { 内容与声明的校验和不一致 })

Inspection =
  Object
  * $failures (list[UploadFailure] * { 这次上传查出的全部问题；空列表表示可以接收 })
  * $accepted (bool * { 是否为真：没有问题，可以接收 })
```

## 基本操作

1. 从请求里取出声明的校验和与内容。
2. 把内容交给 `Checksum`，算出校验和与字节数。
3. 核对字节数是否超过上限，核对算出的校验和与声明是否一致。
4. 把查出的问题记成 `UploadFailure`，收进 `Inspection`；没有问题就把 `$accepted` 置为真。

## apis.viba

```bash apis
import readme.types as readme
import checksum.public as checksum


Inspect =
     readme.Inspection
  <- $upload (readme.UploadRequest * { 一次上传请求：文件名、声明的校验和与内容 })
  <- {
    检查：核对字节数与校验和，交回这次上传查出的全部问题
  }
  <- $digest (checksum.Checksum * { 算校验和：交回内容的 SHA-256 与字节数，用来与上限和声明比对 })
```
