# 上传校验

## 需求背景

输入是声明的校验和 `$checksum` 与上传的内容 `$content`；操作是校验一次上传：算出内容的字节数与校验和，先核对字节数是否超过上限，再核对校验和是否与声明一致，交回失败原因。根 README 从这里取 `Check` 与失败原因的类型：`UploadFailure`、`TooLarge`、`ChecksumMismatch`。

## public.viba

```bash public
import check.types as check
import check.apis as check_api

TooLarge = check.TooLarge

ChecksumMismatch = check.ChecksumMismatch

UploadFailure = check.UploadFailure

Check = check_api.Check
```

## types.viba

```bash types
TooLarge =
  Object
  * $limit (int * { 允许的最大字节数 })
  * $actual (int * { 这次上传的字节数 })

ChecksumMismatch =
  Object
  * $declared (str * { 请求里声明的校验和 })
  * $computed (str * { 从内容算出来的校验和 })

UploadFailure =
  Oneof
  | $too_large (TooLarge * { 内容超过允许的大小 })
  | $checksum_mismatch (ChecksumMismatch * { 内容与声明的校验和不一致 })
```

## 基本操作

1. 接收声明的校验和与内容。
2. 算出内容的字节数与校验和。
3. 先核对字节数，超过上限就记下 `TooLarge`。
4. 没有超过上限就核对校验和，与声明不一致就记下 `ChecksumMismatch`；两项都通过就交回 `nil`。
5. 有失败就交回对应的 `UploadFailure` 变体。

## apis.viba

```bash apis
import check.types as check


Check =
     (check.UploadFailure | nil)
  <- $checksum (str * { 请求里声明的校验和 })
  <- $content (str * { 上传的内容 })
  <- {
    校验：算出内容的字节数与校验和，核对上限与声明，交回失败原因；没有问题交回 nil
  }
```
