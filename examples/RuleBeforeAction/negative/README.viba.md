# 团队规范库维护

## 需求背景

输入是规范库目录的路径 `$root`；操作有两类：读出规范库里的规范，淘汰该删的规范。本示例是 RuleBeforeAction 的反例：`Retire` 先写淘汰动作，判据只在基本操作里写成一句“按惯例”，动作前没有可复核的判据。

## public.viba

```bash public
import readme.types as readme
import readme.apis as readme_api

RetireReport = readme.RetireReport

Retire = readme_api.Retire
```

## types.viba

```bash types
import norms.public as norms


RetireReport =
  Object
  * $removed (list[norms.Norm] * { 已经删掉的规范，按文件名排列 })
  * $kept (list[norms.Norm] * { 留在库里的规范，按文件名排列 })
```

## 基本操作

1. 读规范库，拿到目录里的每篇规范。
2. 按惯例挑出该淘汰的规范：维护者凭经验判断哪几篇该删。
3. 挑出来的规范交给 `Delete` 删掉，交回删掉的规范与保留的规范。

## apis.viba

```bash apis
import readme.types as readme
import norms.public as norms


Retire =
     readme.RetireReport
  <- $root (str * { 规范库目录的路径 })
  <- {
    淘汰：挑出该删的规范，从目录里删掉，交回删掉的规范与保留的规范
  }
  <- $load (norms.Load * { 读库：交回目录里的每篇规范，用它取出要处理的规范 })
  <- $delete (norms.Delete * { 删文件：交回删掉这篇规范之后剩下的规范清单，用它得到库里的剩余规范 })
```
