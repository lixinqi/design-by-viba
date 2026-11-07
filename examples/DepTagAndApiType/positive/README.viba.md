# 通知服务

## 需求背景

输入是一条通知的收件人、标题与正文 `$notice`；操作有两类：把标题与正文渲染成一条消息，把消息投给收件人并交回回执。本示例是 DepTagAndApiType 的正例：`Notify` 依赖 `Render`，依赖参数带 `$render` 标签，类型写 `render.Render`。

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
import render.public as render


Notify =
     readme.Receipt
  <- $notice (readme.Notice * { 收件人、标题与正文 })
  <- {
    通知：把标题与正文渲染成消息，投给收件人，交回投递回执
  }
  <- $render (render.Render * { 渲染：交回一条消息，用它投给收件人 })
```
