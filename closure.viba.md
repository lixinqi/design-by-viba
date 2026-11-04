# 用闭包检验模型

## 需求背景

删除不能凭印象，要靠图：从根文档的 public 出发做可达性，够不到的就是孤立物。删之前它只是可疑，删之后图不对了，问题立刻看得见——闭包是成本最低的检验手段。

示例：入口从「整份 README」收紧到「README 的 public」之后，可达定义从 240 个降到 49 个，文档从 12 份减到 8 份；再按提示补回缺的边，稳定在 11 份。它也会暴露错删：`SampleConfigBase` 被删掉那次，不是闭包算错，而是 `RunSpec.$config` 那条边没连上。非文档文件同样适用：被 public 够不到的 102 个文件一次性删掉。根 README 的 `Check` 依赖本篇的 `Reach` 与 `Prune`，所以这篇有 public。

## public.viba

```bash public
import closure.types as closure
import closure.apis as closure_api

Reach = closure_api.Reach

Prune = closure_api.Prune
```

## types.viba

闭包要留下证据：从哪个入口出发、走到了哪些名字、哪些名字没走到。孤立物的种类决定处理方式——定义删掉，文档删掉，文件删掉，代码与生成物也删掉。

```bash types
Closure =
  Object
  * $root (str * { 入口：根文档的 public，例如 README.public })
  * $reached (list[str] * { 走到的名字，按模块分组 })
  * $orphans (list[Unreachable] * { 没走到的名字；空列表表示这张图是连通的 })

Unreachable =
  Oneof
  | $definition (str * { 没走到的类型或操作：从定义处删掉 })
  | $document (str * { 整份文档都够不到：删文件与它的生成物 })
  | $file (str * { 文档之外的文件：删掉并清理空目录 })
  | $reference (str * { 说明文字里指向已删名字的引用：改成描述或删掉 })
```

## 基本操作

1. 算可达：从根 public 出发，顺着字段类型、参数类型与 public 转发走到所有名字。
2. 删孤立：按种类删除；删完重算一次，直到孤立列表为空。
3. 看缺口：如果删掉的东西里有人认为核心，先把引用关系补上再删，不要用恢复文件来掩盖断掉的引用。

## apis.viba

```bash apis
import closure.types as closure

Reach =
     closure.Closure
  <- $root (str * { 入口：根文档的 public })
  <- {
    算可达：从入口出发走引用边；返回走到的名字与没走到的名字。提示文字不算边，public 的转发算边
  }

Prune =
     list[closure.Unreachable]
  <- $closure (closure.Closure * { 一次可达性计算的结果 })
  <- {
    删孤立：按种类删除，definition 与 document 删定义，file 删文件并清理空目录，reference 改说明；返回这一轮删掉的条目，删完再算一次可达
  }
```
