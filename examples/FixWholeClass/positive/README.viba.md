# 提示渲染

## 需求背景

输入是一篇提示模板的路径 `$path` 与一份变量表 `$vars`；操作有三类：解析模板，查缓存里有没有同一个键的条目，把变量填进模板渲染出提示。本示例是 FixWholeClass 的正例：`Parse`、`Lookup`、`Store`、`Render` 四个函数的提示块全部折行，没有只改被点到的那一处。

## public.viba

```viba public
import readme.types as readme
import readme.apis as readme_api

Rendered = readme.Rendered

Render = readme_api.Render
```

## types.viba

```viba types
import cache.public as cache


Rendered =
  Object
  * $text (str * { 填好变量、可以直接使用的提示文本 })
  * $entry (cache.Entry * { 这份提示在缓存里的条目，同一个键下次直接取它 })
```

## 基本操作

1. 把模板路径交给 `Parse`，读出模板正文与变量名。
2. 用模板路径和变量表算出键，交给 `Lookup`，看缓存里有没有同一个键的条目。
3. 有就直接用条目里的文本；没有就把变量填进模板，交给 `Store` 存成条目，交回提示文本与条目。

## apis.viba

```viba apis
import readme.types as readme
import parse.public as parse
import cache.public as cache


Render =
     readme.Rendered
  <- $path (str * { 提示模板文件的路径 })
  <- $vars (dict[str, str] * { 变量名与值，填进模板里的占位符 })
  <- {
    渲染：解析模板，查缓存里有没有同一个键的条目；有就直接用，没有就把变量填进模板、存进缓存，交回提示文本与条目
  }
  <- $parse (parse.Parse * { 解析：交回模板的名字、正文与变量名，用它知道要填哪些变量 })
  <- $lookup (cache.Lookup * { 查缓存：交回同一个键下已有的条目，用它跳过重复渲染 })
  <- $store (cache.Store * { 存缓存：交回存好的条目，用它留给下一次渲染 })
```
