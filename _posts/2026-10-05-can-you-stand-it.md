---
title: "Can You Stand It?"
date: 2026-10-05 00:00:00 +0700
categories: ["CDCTF 2026", "OSINT"]
tags: ["cdctf", "osint"]
description: "Bài giải Can You Stand It? trong CDCTF 2026."
mermaid: true
---

<div class="lang-switch" role="tablist" aria-label="Language switch">
  <button class="lang-btn active" role="tab" type="button" data-lang="en" aria-selected="true">EN</button>
  <button class="lang-btn" role="tab" type="button" data-lang="vn" aria-selected="false">VN</button>
</div>

<div class="lang-vn" markdown="1">

## Đề bài

Bài thơ gợi tới Guy Standing và ảnh trên Wikipedia. Xem lịch sử trang cùng các thảo luận về ảnh để tìm người yêu cầu thay ảnh.

## Cách giải

Trong bản sửa ngày 17/10/2023, tài khoản Geneva2009 tự nhận là vợ của Guy Standing và đề nghị bỏ ảnh gây hiểu lầm. Tên tài khoản với chữ G viết hoa là đáp án.

```mermaid
flowchart LR
  A["Nhận dạng Guy Standing"]
  B["Mở lịch sử trang Wikipedia"]
  C["Đọc thảo luận về ảnh"]
  D["Xác định tài khoản yêu cầu đổi ảnh"]
  A --> B --> C --> D
```

⇒ **Flag:** `cdctf{Geneva2009}`

</div>

<div class="lang-en" markdown="1">

## Challenge

The poem points to Guy Standing and his Wikipedia photo. Inspect the page history and image discussions to identify who requested a change.

## Solution

In the 17 October 2023 edit, account Geneva2009 identifies herself as Guy Standing’s wife and asks to remove the misleading image. The username, with an uppercase G, is the answer.

```mermaid
flowchart LR
  A["Identify Guy Standing"]
  B["Open the Wikipedia revision history"]
  C["Read the image discussion"]
  D["Find the account requesting the change"]
  A --> B --> C --> D
```

⇒ **Flag:** `cdctf{Geneva2009}`

</div>
