# 模板站构建器

## 需求背景

输入是模板目录的路径 `$root` 与数据文件的路径 `$data`；操作类别有两类：解析单个模板，把整个目录的模板渲染成一份站点。本示例是 FixedStructure 的反例：`index.viba.md` 也导出一份 `Build`，与 README 并列，入口不再唯一。

## public.viba

```viba public
import readme.types as readme
import readme.apis as readme_api

Site = readme.Site

Build = readme_api.Build
```

## types.viba

```viba types
import parse.public as parse


Site =
  Object
  * $pages (list[str] * { 渲染出来的页面，顺序与模板目录一致 })
  * $templates (list[parse.Template] * { 这次解析过的模板，按首次解析的顺序排列 })
```

## 基本操作

1. 读数据文件，拿到每个占位符名对应的值。
2. 走一遍模板目录，把每个模板交给 `Parse`，拿到占位符与原文。
3. 把值填进原文里的占位符，得到一份页面。
4. 把页面按目录顺序排好，连同解析过的模板收进 `Site`。

## apis.viba

```viba apis
import readme.types as readme
import parse.public as parse


Build =
     readme.Site
  <- $root (str * { 模板目录的路径 })
  <- $data (str * { 数据文件的路径，键是模板里的占位符名 })
  <- {
    构建：把目录里的每个模板填上数据，渲染成页面，交回整站的页面与解析过的模板
  }
  <- $parse (parse.Parse * { 解析：交回一个模板的占位符与原文，用它填数据 })
```
