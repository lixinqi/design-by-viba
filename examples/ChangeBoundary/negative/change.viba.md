# 改动记录

## 需求背景

输入是任务单声明的范围与改动清单，两者都是一组文件路径；操作只有一类：把改动清单逐项对照范围，算出越界项与是否通过。本示例是 ChangeBoundary 反例的记录方：范围两项，`README.viba.md` 与 `change.viba.md`；改动清单三项，多出的一项是 `parse.viba.md`，它不在范围里，事先也没有获得确认，越界项一项。根 README 从这里取 `Change`、`Boundary` 与 `Check`。

## public.viba

```bash public
import change.types as change
import change.apis as change_api

Change = change.Change

Boundary = change.Boundary

Check = change_api.Check
```

## types.viba

```bash types
Change =
  Object
  * $scope (list[str] * { 任务单声明的范围：允许改动的文件路径，每行一个 })
  * $touched (list[str] * { 改动清单：实际改过的文件路径，落在 $scope 之外的要先获得确认 })

Boundary =
  Object
  * $outside (list[str] * { 改动清单里有、范围里没有的路径，每一项都是一处越界 })
  * $unconfirmed (list[str] * { $outside 里事先没有获得确认的路径 })
  * $passed (bool * { $unconfirmed 为空列表时为 true })
```

## 基本操作

1. 收下要核对的 `Change`：范围在 `$scope`，改动清单在 `$touched`。
2. 把 `$touched` 逐项对照 `$scope`，不在范围里的路径记成 `$outside`。
3. `$outside` 里事先获得确认的放行，其余记成 `$unconfirmed`。
4. `$unconfirmed` 为空列表时 `$passed` 记为 true，把越界项、未获确认的越界项与结论交回。

## apis.viba

```bash apis
import change.types as change


Check =
     change.Boundary
  <- $change (change.Change * { 要核对的范围与改动清单 })
  <- {
    核对：把改动清单逐项对照范围，交回越界项、未获确认的越界项与是否通过
  }
```
