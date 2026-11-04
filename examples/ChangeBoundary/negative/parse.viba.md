# 清单解析

## 需求背景

输入是一份清单文件的路径 `$path`；操作只有一类：逐行读出文件里的路径，交回一张路径表。本示例是 ChangeBoundary 反例的读取方：`parse.viba.md` 出现在改动清单里，任务声明的范围却没有覆盖它。根 README 从这里取 `Parse`。

## public.viba

```bash public
import parse.types as parse
import parse.apis as parse_api

Listing = parse.Listing

Parse = parse_api.Parse
```

## types.viba

```bash types
Listing =
  Object
  * $paths (list[str] * { 清单文件里每一行的路径，顺序与文件一致 })
```

## 基本操作

1. 打开清单文件。
2. 逐行读出文件路径。
3. 按文件里的先后排成一张路径表。

## apis.viba

```bash apis
import parse.types as parse


Parse =
     parse.Listing
  <- $path (str * { 清单文件的路径，每行一个路径 })
  <- {
    解析：逐行读出一份清单里的路径，交回一张路径表
  }
```
