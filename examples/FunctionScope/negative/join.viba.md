# 报表拼接

## 需求背景

输入是报表的一行 `$row` 与这一行是不是末项 `$is_last`；操作只有一类：把一行接成报表正文里的一段。本示例是 FunctionScope 反例的依赖方：`Join` 不再判断末项，末项由调用方按位置告诉它。根 README 从这里取 `Row` 与 `Join`。

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

1. 收下一行的文本与它是不是末项。
2. 不是末项就在文本后面补一个空行；是末项就原样保留。
3. 交回这一段，由调用方按顺序接成正文。

## apis.viba

```viba apis
import join.types as join


Join =
     str
  <- $row (join.Row * { 报表里的一行文本 })
  <- $is_last (bool * { 这一行是不是报表的末项，由调用方按导出顺序判断 })
  <- {
    拼接：交回一行拼好的一段；不是末项就在后面补一个空行，是末项就原样交回
  }
```
