# 站内检索

## 需求背景

输入是查询串 `$query` 与倒排索引文件的路径 `$index`；操作有两类：把查询切成词项，按词项从索引里取回命中的文档。本示例是 DependenciesAfterHint 的反例：`Search` 依赖 `Tokenize`，依赖参数却写在提示块之前。

## public.viba

```bash public
import readme.types as readme
import readme.apis as readme_api

Hits = readme.Hits

Search = readme_api.Search
```

## types.viba

```bash types
import tokenize.public as tokenize


Hits =
  Object
  * $terms (list[tokenize.Token] * { 查询切出来的词项，按切分顺序 })
  * $documents (list[str] * { 命中的文档路径，按相关度从高到低 })
```

## 基本操作

1. 把查询串交给 `Tokenize`。
2. 按词项从倒排索引里取回命中的文档。
3. 按相关度排好命中，连同查询的词项一起交回。

## apis.viba

```bash apis
import readme.types as readme
import tokenize.public as tokenize


Search =
     readme.Hits
  <- $query (str * { 查询串 })
  <- $index (str * { 倒排索引文件的路径 })
  <- $tokenize (tokenize.Tokenize * { 词汇切分：交回查询切出来的词项，用它去倒排索引里取命中 })
  <- {
    检索：把查询切成词项，按词项从倒排索引里取回文档，交回命中文档与查询的词项
  }
```
