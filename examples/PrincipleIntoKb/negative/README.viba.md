# 团队知识库

## 需求背景

输入是知识库目录的路径 `$root`；操作只有一类：审查整个知识库，按规则集交回违规报告。本示例是 PrincipleIntoKb 的反例：知识库的规则集只在基本操作里写了一句“提示要折行”，没有把它写成规则类型，也没有附示例。

## public.viba

```bash public
import readme.types as readme
import readme.apis as readme_api

AuditReport = readme.AuditReport

Audit = readme_api.Audit
```

## types.viba

```bash types
import rules.public as rules


AuditReport =
  Object
  * $findings (list[rules.Finding] * { 检查发现的违规，按文档在目录里的先后排列 })
  * $passed (bool * { 没有违规时为 true })
```

## 基本操作

1. 走一遍知识库目录，拿到每篇文档的路径。
2. 读出文档全文，交给 `Check`，收下违规条目。
3. 把全部违规条目收成 `AuditReport`，没有违规时 `$passed` 记为 true。

## apis.viba

```bash apis
import readme.types as readme
import rules.public as rules


Audit =
     readme.AuditReport
  <- $root (str * { 知识库目录的路径 })
  <- {
    审查：把目录里每篇文档交给规则检查，交回整库的违规报告
  }
  <- $check (rules.Check * { 查规则：交回一篇文档的违规条目，用它收成整库的违规报告 })
```
