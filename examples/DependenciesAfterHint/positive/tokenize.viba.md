# 查询分词

## 需求背景

输入是查询串 `$text`；操作是把查询切成词项，并记下每个词项在查询里的起始位置。`Tokenize` 只负责切分，不知道命中如何取回与排序。根 README 从这里取 `Tokenize`。

## public.viba

```viba public
import tokenize.types as tokenize
import tokenize.apis as tokenize_api

Token = tokenize.Token

Tokenize = tokenize_api.Tokenize
```

## types.viba

```viba types
Token =
  Object
  * $text (str * { 词项的文本 })
  * $position (int * { 词项在查询里的起始字符位置 })
```

## 基本操作

1. 扫描查询串。
2. 把连续的字母与数字记成一个词项。
3. 记下词项的文本与它在查询里的起始字符位置。

## apis.viba

```viba apis
import tokenize.types as tokenize


Tokenize =
     list[tokenize.Token]
  <- $text (str * { 查询串 })
  <- {
    切分：把查询串切成词项，交回每个词项的文本与在查询里的起始位置
  }
```
