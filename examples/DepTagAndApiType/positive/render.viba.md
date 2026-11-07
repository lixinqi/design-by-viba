# 消息渲染

## 需求背景

输入是通知的标题 `$title` 与正文 `$body`；操作是把这两段文字排成一条可以投递的消息。本示例是 DepTagAndApiType 正例的依赖方：`Render` 只负责渲染，不知道消息如何投递。根 README 从这里取 `Render`。

## public.viba

```viba public
import render.types as render
import render.apis as render_api

Message = render.Message

Render = render_api.Render
```

## types.viba

```viba types
Message =
  Object
  * $subject (str * { 消息的主题，取自通知的标题 })
  * $content (str * { 消息的正文，取自通知的正文 })
```

## 基本操作

1. 把标题作为消息的主题。
2. 把正文作为消息的内容。
3. 两者合成一条消息。

## apis.viba

```viba apis
import render.types as render


Render =
     render.Message
  <- $title (str * { 要渲染成消息主题的文字 })
  <- $body (str * { 要渲染成消息正文的文字 })
  <- {
    渲染：把标题与正文排成一条消息，交回主题与正文
  }
```
