---
title: "Crimson Clinic Terminal 3: Records"
date: 2026-10-05 00:00:00 +0700
categories: ["CDCTF 2026", "AI"]
tags: ["cdctf", "ai"]
description: "Bài giải Crimson Clinic Terminal 3: Records trong CDCTF 2026."
mermaid: true
---

<div class="lang-switch" role="tablist" aria-label="Language switch">
  <button class="lang-btn active" role="tab" type="button" data-lang="en" aria-selected="true">EN</button>
  <button class="lang-btn" role="tab" type="button" data-lang="vn" aria-selected="false">VN</button>
</div>

<div class="lang-vn" markdown="1">

## Đề bài

Bộ phận hồ sơ chỉ cho phép tiết lộ từng trường dữ liệu một. Yêu cầu toàn bộ face sheet cùng lúc bị chặn.

## Cách giải

Yêu cầu lần lượt trường 1, 2, 3, 4 theo đúng quy trình mà bot tự mô tả. Phản hồi từng bước tiết lộ dữ liệu cần để hoàn thành thử thách; flag được người chơi xác nhận sau lượt cuối.

```mermaid
flowchart LR
  A["Yêu cầu toàn bộ face sheet"]
  B["Nhận phản hồi bị chặn"]
  C["Hỏi từng trường 1 đến 4"]
  D["Ghép dữ liệu cuối cùng"]
  A --> B --> C --> D
```

⇒ **Flag:** `cdctf{one_element_at_a_time}`

</div>

<div class="lang-en" markdown="1">

## Challenge

The records desk releases only one data element per request. Asking for the whole face sheet at once is blocked.

## Solution

Request fields 1, 2, 3, and 4 separately, following the procedure described by the bot. The sequential responses disclose the required information; the player confirmed the flag after the final step.

```mermaid
flowchart LR
  A["Request the full face sheet"]
  B["Receive the blocked response"]
  C["Ask for fields one through four"]
  D["Assemble the final data"]
  A --> B --> C --> D
```

⇒ **Flag:** `cdctf{one_element_at_a_time}`

</div>
