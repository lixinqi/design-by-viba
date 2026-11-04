# 团队规范库

## 需求背景

输入是一句训斥的原话 `$scold` 与规范库目录的路径 `$root`；操作有两类：从原话反推一条规则，把规则写进规范库。本示例是 ScoldingIsRequirement 的正例：规则叶子把训斥的原话逐字抄进 `$evidence`，`$statement` 从原话反推出来。

## public.viba

```bash public
import readme.types as readme
import readme.apis as readme_api

RuleBook = readme.RuleBook

Adopt = readme_api.Adopt
```

## types.viba

```bash types
import rules.public as rules


RuleBook =
  Object
  * $rules (list[rules.Rule] * { 规范库里的规则，按收录先后排列 })
```

## 基本操作

1. 收下训斥的原话与规范库目录的路径。
2. 把原话交给 `Record`，收下一条规则。
3. 把这条规则追加进 `$root` 下的规范库，交回新的规范库。

## apis.viba

```bash apis
import readme.types as readme
import rules.public as rules


Adopt =
     readme.RuleBook
  <- $root (str * { 规范库所在目录的路径 })
  <- $scold (str * { 训斥的原话，逐字抄录 })
  <- {
    收录：把训斥的原话交给记录，反推成规则并追加进规范库，交回新的规范库
  }
  <- $record (rules.Record * { 记录：交回一条规则，用它追加进规范库 })
```
