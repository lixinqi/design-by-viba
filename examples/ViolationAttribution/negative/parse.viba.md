# 规则文件解析

## 需求背景

输入是一个规则文件的路径 `$path`；操作只有一类：读出规则文件的原则与正文。原则取第一个一级标题，正文取标题以下的内容，检查器按正文比对仓库里的文件。根 README 从这里取 `Rule` 与 `Parse`。

## public.viba

```bash public
import parse.types as parse
import parse.apis as parse_api

Rule = parse.Rule

Parse = parse_api.Parse
```

## types.viba

```bash types
Rule =
  Object
  * $principle (str * { 第一个一级标题，违规要归因到这个原则 })
  * $body (str * { 标题以下的正文，写清要检查什么 })
```

## 基本操作

1. 读文件。
2. 把第一个一级标题记成原则。
3. 其余内容记成正文，与原则一起记成一条 `Rule`。

## apis.viba

```bash apis
import parse.types as parse


Parse =
     parse.Rule
  <- $path (str * { 规则文件的路径 })
  <- {
    解析：读出规则文件的原则与正文，交回一条规则
  }
```
