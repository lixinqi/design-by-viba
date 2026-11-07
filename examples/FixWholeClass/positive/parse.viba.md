# 模板解析

## 需求背景

输入是一篇提示模板文件的路径 `$path`；操作只有一类：读出模板的名字、正文与变量名。根 README 从这里取 `Parse`。

## public.viba

```viba public
import parse.types as parse
import parse.apis as parse_api

Template = parse.Template

Parse = parse_api.Parse
```

## types.viba

```viba types
Template =
  Object
  * $name (str * { 模板的名字，取文件名去掉扩展名 })
  * $text (str * { 模板正文，变量占位符留待渲染时填写 })
  * $variables (list[str] * { 正文里出现的变量名，按第一次出现的先后排列 })
```

## 基本操作

1. 读文件。
2. 把文件名去掉扩展名，记成模板的名字。
3. 把正文里变量占位符的名字按出现顺序记成变量名清单。

## apis.viba

```viba apis
import parse.types as parse


Parse =
     parse.Template
  <- $path (str * { 提示模板文件的路径 })
  <- {
    解析：读出一篇提示模板的名字、正文与变量名
  }
```
