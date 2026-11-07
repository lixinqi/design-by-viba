# 改动范围核对

## 需求背景

输入是任务单声明的范围文件路径 `$scope_path` 与改动清单文件路径 `$touched_path`；操作有两类：把一份清单读成路径表，核对改动是否越出范围。本示例是 ChangeBoundary 的正例：`change.viba.md` 的改动清单两项都落在范围里，越界项为空列表，`Audit` 交回通过。

## public.viba

```viba public
import readme.types as readme
import readme.apis as readme_api

AuditReport = readme.AuditReport

Audit = readme_api.Audit
```

## types.viba

```viba types
import change.public as change


AuditReport =
  Object
  * $change (change.Change * { 要核对的范围与改动清单 })
  * $boundary (change.Boundary * { 越界项、未获确认的越界项与是否通过 })
```

## 基本操作

1. 把范围文件交给 `Parse`，读出允许改动的路径表。
2. 把改动清单文件交给 `Parse`，读出实际改过的路径表。
3. 两张表记成一份 `Change`，交给 `Check`，取回越界项、未获确认的越界项与是否通过。
4. 把 `Change` 与核对结果装进 `AuditReport`。

## apis.viba

```viba apis
import readme.types as readme
import parse.public as parse
import change.public as change


Audit =
     readme.AuditReport
  <- $scope_path (str * { 范围文件的路径，每行一个允许改动的文件 })
  <- $touched_path (str * { 改动清单文件的路径，每行一个实际改过的文件 })
  <- {
    核对：把两份清单读成路径表，记成一份改动，对照范围交回越界项与是否通过
  }
  <- $parse (parse.Parse * { 解析：交回一份清单里的路径表，用它读出范围文件与改动清单文件里的路径 })
  <- $check (change.Check * { 核对：交回越界项、未获确认的越界项与是否通过，用它写出核对结论 })
```
