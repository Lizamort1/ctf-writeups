---
title: "Epic Rat Encoding"
date: 2026-10-05 00:00:00 +0700
categories: ["CDCTF 2026", "Reverse Engineering"]
tags: ["cdctf", "reverse-engineering"]
description: "Bài giải Epic Rat Encoding trong CDCTF 2026."
mermaid: true
---

<div class="lang-switch" role="tablist" aria-label="Language switch">
  <button class="lang-btn active" role="tab" type="button" data-lang="en" aria-selected="true">EN</button>
  <button class="lang-btn" role="tab" type="button" data-lang="vn" aria-selected="false">VN</button>
</div>

<div class="lang-vn" markdown="1">

## Đề bài

Tệp message_encoder.c biến thông điệp thành các số lớn. Đọc lại chiều chuyển đổi để biết từng số biểu diễn một khối tám byte.

## Cách giải

Chuyển từng số về tám byte big-endian rồi ghép theo thứ tự ban đầu. Bản rõ hẹn gặp tại Tom Bevill Building vào trưa thứ Năm tuần sau; mã hóa ngược xác nhận khớp cả tám số đầu vào.

```mermaid
flowchart LR
  A["Đọc quy tắc trong message_encoder.c"]
  B["Đổi số về 8 byte big-endian"]
  C["Ghép các khối theo thứ tự"]
  D["Đọc thông điệp và flag"]
  A --> B --> C --> D
```

⇒ **Flag:** `cdctf{Tom_Bevill_Building_at_noon_next_week_Thursday}`

</div>

<div class="lang-en" markdown="1">

## Challenge

The message_encoder.c file turns a message into large integers. Reverse its conversion to see that each integer represents an eight-byte block.

## Solution

Convert every integer to eight big-endian bytes and concatenate the blocks in order. The plaintext names Tom Bevill Building at noon next Thursday; encoding it again matches all eight input integers.

```mermaid
flowchart LR
  A["Read the rule in message_encoder.c"]
  B["Convert each number to 8-byte big-endian"]
  C["Join the blocks in order"]
  D["Read the message and flag"]
  A --> B --> C --> D
```

⇒ **Flag:** `cdctf{Tom_Bevill_Building_at_noon_next_week_Thursday}`

</div>
