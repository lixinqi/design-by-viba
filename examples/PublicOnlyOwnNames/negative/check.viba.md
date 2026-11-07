# 链接检查

## 需求背景

输入是一组页面文件的路径 `$pages`；操作是读出每个页面里的链接，交回打不开的那些。本示例是 PublicOnlyOwnNames 反例的依赖方：`Check` 只负责检查链接，不知道文档如何排版。根 README 从这里取 `Check`。

## public.viba

```viba public
import check.types as check
import check.apis as check_api

Report = check.Report

Check = check_api.Check
```

## types.viba

```viba types
Report =
  Object
  * $broken (list[str] * { 无法打开的链接，按出现顺序 })
```

## 基本操作

1. 逐个打开页面文件。
2. 读出页面里的每个链接。
3. 把打不开的链接按出现顺序记下来。

## apis.viba

```viba apis
import check.types as check


Check =
     check.Report
  <- $pages (list[str] * { 待检查的页面文件路径 })
  <- {
    检查：读出每个页面里的链接，交回无法打开的链接
  }
```
