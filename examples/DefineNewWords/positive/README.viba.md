# 文档索引构建

## 需求背景

输入是一个文档目录的路径 `$root`；操作有两类：解析单篇文档，把整个目录建成一份倒排索引（倒排：从词到文档编号的表）。本示例是 DefineNewWords 的正例：背景第一次出现“倒排”时就当场说明它指什么，读者不必先知道这个词。

## public.viba

```viba public
import readme.types as readme
import readme.apis as readme_api

Index = readme.Index

Build = readme_api.Build
```

## types.viba

```viba types
import parse.public as parse


Index =
  Object
  * $documents (list[parse.Document] * { 解析出来的文档，按目录顺序，编号就是它在列表里的位置 })
  * $terms (dict[str, list[int]] * { 词到文档编号的对照，键是词项 })
```

## 基本操作

1. 把目录里的每篇文档交给 `Parse`，读出标题与词项。
2. 按目录顺序给每篇文档编一个编号，从零开始。
3. 把每篇文档的词项逐条记到这个编号上，连同文档一起交回。

## apis.viba

```viba apis
import readme.types as readme
import parse.public as parse


Build =
     readme.Index
  <- $root (str * { 文档目录的路径 })
  <- {
    建索引：把目录里的每篇文档解析出来，把词项记到文档编号上，交回一份倒排索引
  }
  <- $parse (parse.Parse * { 解析：交回一篇文档的标题与词项，用它把词项记到文档编号上 })
```
