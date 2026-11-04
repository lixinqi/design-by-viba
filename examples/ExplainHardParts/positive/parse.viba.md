# 查询解析

## 需求背景

输入是一个查询串 `$query`；操作只有一类：把查询串拆成要匹配的词项与要排除的词项。根 README 从这里取 `Query` 与 `Parse`。

## public.viba

```bash public
import parse.types as parse
import parse.apis as parse_api

Query = parse.Query

Parse = parse_api.Parse
```

## types.viba

```bash types
Query =
  Object
  * $terms (list[str] * { 要匹配的词项，按查询串里的先后排列 })
  * $excluded (list[str] * { 要排除的词项，查询串里以减号开头 })
```

## 基本操作

1. 按空白把查询串拆成词。
2. 减号开头的词去掉减号，记进要排除的词项。
3. 其余的词记进要匹配的词项，保持查询串里的先后。

## apis.viba

```bash apis
import parse.types as parse


Parse =
     parse.Query
  <- $query (str * { 要解析的查询串 })
  <- {
    解析：把查询串拆成要匹配的词项与要排除的词项
  }
```
