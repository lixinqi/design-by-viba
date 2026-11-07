# 清单解析

## 需求背景

输入是一份清单文件的路径 `$path`；操作只有一类：逐行读出文件里的路径，交回一张路径表。本示例是 ChangeBoundary 正例的读取方：`Parse` 只把清单文件读成路径表，不判断哪一条在范围里。根 README 从这里取 `Parse`。

## public.viba

```viba public
import parse.types as parse
import parse.apis as parse_api

Listing = parse.Listing

Parse = parse_api.Parse
```

## types.viba

```viba types
Listing =
  Object
  * $paths (list[str] * { 清单文件里每一行的路径，顺序与文件一致 })
```

## 基本操作

1. 打开清单文件。
2. 逐行读出文件路径。
3. 按文件里的先后排成一张路径表。

## apis.viba

```viba apis
import parse.types as parse


Parse =
     parse.Listing
  <- $path (str * { 清单文件的路径，每行一个路径 })
  <- {
    解析：逐行读出一份清单里的路径，交回一张路径表
  }
```
