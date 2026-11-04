# 区域销售报表

## 需求背景

输入是一个订单明细 CSV 文件的路径 `$path`；操作有两类：读取明细行，把明细行按区域汇总成一份可以发布的报表。本示例是 InterfaceAnswersNeed 的正例：`Report` 收下背景里说的 `$path`，交回带标题与各区域合计的 `Table`，参数对应输入，返回值对应要发布的报表。

## public.viba

```bash public
import readme.types as readme
import readme.apis as readme_api

Table = readme.Table

Report = readme_api.Report
```

## types.viba

```bash types
RegionRow =
  Object
  * $region (str * { 区域名 })
  * $amount (int * { 该区域订单金额的合计，单位元 })

Table =
  Object
  * $title (str * { 报表标题 })
  * $rows (list[RegionRow] * { 每个区域一行，按合计从大到小排列 })
```

## 基本操作

1. 把明细文件交给 `Load`，收下订单行的清单。
2. 把区域相同的订单金额累加。
3. 每个区域一行，按合计从大到小排好。
4. 加上报表标题，把整张报表交回。

## apis.viba

```bash apis
import readme.types as readme
import orders.public as orders


Report =
     readme.Table
  <- $path (str * { 订单明细 CSV 文件的路径 })
  <- {
    生成：把明细按区域汇总，交回带标题与各区域合计的报表
  }
  <- $load (orders.Load * { 读取：交回明细行的清单，用它按区域汇总金额 })
```
