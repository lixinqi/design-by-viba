# 文档站首页

## 需求背景

输入是 README 文件的路径 `$readme`；操作是构建首页：读出 README 的大标题、需求背景与各级标题，核对需求背景与冻结文本，排出站点首页。本示例是 ReadmeBackgroundFrozen 的反例：README 需求背景在冻结文本之后追加了一段本轮补记。

本轮补记：首页的大标题要跟站点名一起改，这条经验先记在这里。

## public.viba

```bash public
import readme.types as readme
import readme.apis as readme_api

Home = readme.Home

Build = readme_api.Build
```

## types.viba

```bash types
import frozen.public as frozen


Home =
  Object
  * $title (str * { README 的大标题 })
  * $background (frozen.FrozenBackground * { 首页展示的需求背景，逐字取自冻结文本 })
  * $nav (list[str] * { 首页导航里按顺序列出的标题 })
```

## 基本操作

1. 读 README 文件，取出大标题、需求背景与各级标题。
2. 把需求背景交给 `CheckFrozen` 核对，与冻结文本一致才继续。
3. 用大标题、冻结文本与导航排出首页。

## apis.viba

```bash apis
import readme.types as readme
import frozen.public as frozen


Build =
     readme.Home
  <- $readme (str * { README 文件的路径 })
  <- {
    构建：核对 README 的需求背景之后，交回首页的大标题、需求背景与导航
  }
  <- $check (frozen.CheckFrozen * { 查冻结：交回不一致的记录，用它决定首页是否交回 })
```
