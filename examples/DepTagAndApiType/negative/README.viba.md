# 通知服务

## 需求背景

输入是一条通知的收件人、标题与正文 `$notice`；操作有两类：把标题与正文渲染成一条消息，把消息投给收件人并交回回执。本示例是 DepTagAndApiType 的反例：`Notify` 依赖 `Render`，依赖参数的类型却写成了 `str`，操作名 `Render` 只当字符串传。

## public.viba

```viba public
import readme.types as readme
import readme.apis as readme_api

Notice = readme.Notice

Receipt = readme.Receipt

Notify = readme_api.Notify
```

## types.viba

```viba types
import render.public as render


Notice =
  Object
  * $to (str * { 收件人的账号 })
  * $title (str * { 收件人看到的主题行 })
  * $body (str * { 收件人看到的正文 })

Receipt =
  Object
  * $message (render.Message * { 投给收件人的那条消息 })
  * $to (str * { 收到消息的账号 })
```

## 基本操作

1. 从通知里取出标题与正文，交给 `Render`。
2. 把渲染好的消息投给收件人。
3. 把消息与收件人记成回执。

## apis.viba

```viba apis
import readme.types as readme


Notify =
     readme.Receipt
  <- $notice (readme.Notice * { 收件人、标题与正文 })
  <- {
    通知：按操作名找到渲染器，把标题与正文渲染成消息，投给收件人，交回投递回执
  }
  <- $render (str * { 渲染：传操作名 Render 这个字符串，实现按名字找到渲染器，再用它把通知渲染成消息 })
```
