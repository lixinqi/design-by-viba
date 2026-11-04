# 校验和计算

## 需求背景

输入是一段上传内容 `$content`；操作是算出这段内容的 SHA-256，交回十六进制串与参与计算的字节数。根 README 从这里取 `Checksum` 与 `Digest`。

## public.viba

```bash public
import checksum.types as checksum
import checksum.apis as checksum_api

Digest = checksum.Digest

Checksum = checksum_api.Checksum
```

## types.viba

```bash types
Digest =
  Object
  * $value (str * { SHA-256 的十六进制串 })
  * $size (int * { 参与计算的字节数 })
```

## 基本操作

1. 按 UTF-8 把内容编码成字节。
2. 算出字节的 SHA-256。
3. 把十六进制串与字节数记成 `Digest`。

## apis.viba

```bash apis
import checksum.types as checksum

Checksum =
     checksum.Digest
  <- $content (str * { 上传的内容，按 UTF-8 编码成字节 })
  <- {
    算校验和：算出内容的 SHA-256，交回十六进制串与字节数
  }
```
