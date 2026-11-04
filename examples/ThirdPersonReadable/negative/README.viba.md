# 团队知识库构建器

## 需求背景

输入是一个 Markdown 笔记目录的路径 `$root`；操作有两类：解析单篇笔记，把整个目录构建成一份团队知识库的目录树。目录树的排法：把上一轮说的那个结构落进文档。本示例是 ThirdPersonReadable 的反例：需求背景没有给出“目录树”的定义，用“上一轮说的那个结构”代替，读者没有看过对话就读不懂。

## public.viba

```bash public
import readme.types as readme
import readme.apis as readme_api

Site = readme.Site

Build = readme_api.Build
```

## types.viba

```bash types
import parse.public as parse


Site =
  Object
  * $pages (list[parse.Page] * { 解析出来的页面，按一级标题排好 })
```

## 基本操作

1. 把目录里的每篇笔记交给 `Parse`。
2. 按一级标题把页面分进目录树的节点。
3. 生成一份可以按标题浏览的团队知识库。

## apis.viba

```bash apis
import readme.types as readme
import parse.public as parse


Build =
     readme.Site
  <- $root (str * { Markdown 笔记目录的路径 })
  <- {
    构建：把目录里的每篇笔记解析出来，按一级标题排成目录树，交回团队知识库的页面清单
  }
  <- $parse (parse.Parse * { 解析：交回一篇笔记的标题与正文，用它排目录树 })
```
