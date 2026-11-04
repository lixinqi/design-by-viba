# 文档站构建

## 需求背景

输入是一个 Markdown 目录的路径 `$root`；操作只有一类：把整个目录构建成一份可以发布的站点。本示例是 SmallFunctions 的反例：`Build` 在同一个提示块里同时做解析、排版、渲染，三个短条件分支也一并计入这一个函数。

## public.viba

```bash public
import readme.types as readme
import readme.apis as readme_api

Site = readme.Site

Build = readme_api.Build
```

## types.viba

```bash types
Site =
  Object
  * $html (str * { 整站拼好的 HTML，可以直接发布 })
```

## 基本操作

1. 把目录路径交给 `Read`，收下每个文件的路径与原文。
2. 逐个把原文的第一个一级标题读成标题，其余内容读成正文；没有一级标题时用文件名去掉扩展名顶上。
3. 把页面按标题排成目录顺序；标题重复时保留读到的先后。
4. 把页面依次拼成整站 HTML；正文为空时留一个占位。
5. 把 HTML 记成 `Site` 交回。

## apis.viba

```bash apis
import readme.types as readme
import read.public as read


Build =
     readme.Site
  <- $root (str * { Markdown 目录的路径 })
  <- {
    构建：逐个把原文的第一个一级标题读成标题、其余内容读成正文，没有一级标题时用文件名顶上；
    把页面按标题排成目录顺序，标题重复时保留读到的先后；把页面依次拼成整站 HTML，
    正文为空时留一个占位；交回一份可以发布的站点
  }
  <- $read (read.Read * { 读取：交回目录里每个文件的路径与原文，用它逐个解析 })
```
