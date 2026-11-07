# 报表拼接

## 需求背景

输入是报表的明细行 `$rows`；操作只有一类：把各行按顺序接成报表正文。本示例是 FunctionScope 正例的依赖方：`Join` 自己决定分隔符与末项，调用方只交出明细行。根 README 从这里取 `Row` 与 `Join`。

## public.viba

```viba public
import join.types as join
import join.apis as join_api

Row = join.Row

Join = join_api.Join
```

## types.viba

```viba types
Row =
  Object
  * $text (str * { 报表里一行文本，不含换行 })
```

## 基本操作

1. 按导出顺序取出每一行的文本。
2. 行与行之间空一行，最后一行后面不补空行。
3. 交回拼好的报表正文。

## apis.viba

```viba apis
import join.types as join


Join =
     str
  <- $rows (list[join.Row] * { 报表的明细行，按导出顺序排列 })
  <- {
    拼接：把每一行文本按顺序接起来，行与行之间空一行，末项后面不再补空行；交回报表正文
  }
```
