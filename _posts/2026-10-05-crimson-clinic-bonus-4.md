---
title: "Welcome to Crimson Clinic BONUS 4"
date: 2026-10-05 00:00:00 +0700
categories: ["CDCTF 2026", "OSINT"]
tags: ["cdctf", "osint"]
description: "Bài giải Welcome to Crimson Clinic BONUS 4 trong CDCTF 2026."
---

<div class="lang-switch" role="tablist" aria-label="Language switch">
  <button class="lang-btn active" role="tab" type="button" data-lang="en" aria-selected="true">EN</button>
  <button class="lang-btn" role="tab" type="button" data-lang="vn" aria-selected="false">VN</button>
</div>

<div class="lang-vn" markdown="1">

## Đề bài

Đề hỏi món tráng miệng nổi tiếng của Maryanne Barrett. Tìm các bài đăng liên quan gia đình Barrett và bữa tiệc của trường trên Crimson Social.

## Cách giải

Một bài viết cảm ơn mẹ của Mrs. Barrett-Reynolds mang món peach cobbler tới buổi họp mặt; bài của Brandon Barrett cũng nhắc món mẹ thường làm. Dùng tên món với dấu cách như cú pháp mẫu.

```mermaid
flowchart LR
  A["Tìm bài đăng gia đình Barrett"]
  B["Đối chiếu bài về buổi họp mặt"]
  C["Xác định món tráng miệng"]
  D["Giữ dấu cách trong đáp án"]
  A --> B --> C --> D
```

⇒ **Flag:** `cdctf{peach cobbler}`

</div>

<div class="lang-en" markdown="1">

## Challenge

The challenge asks for Maryanne Barrett’s signature dessert. Search Crimson Social posts about the Barrett family and a school gathering.

## Solution

A post thanks Mrs. Barrett-Reynolds’s mother for bringing peach cobbler; Brandon Barrett also mentions his mother’s usual dessert. Use the dish name with a space, matching the prompt’s format.

```mermaid
flowchart LR
  A["Search the Barrett family posts"]
  B["Cross-check the gathering post"]
  C["Identify the dessert"]
  D["Preserve the space in the answer"]
  A --> B --> C --> D
```

⇒ **Flag:** `cdctf{peach cobbler}`

</div>
