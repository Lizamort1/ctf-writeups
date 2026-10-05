---
title: "Welcome to Crimson Clinic BONUS 2"
date: 2026-10-05 00:00:00 +0700
categories: ["CDCTF 2026", "OSINT"]
tags: ["cdctf", "osint"]
description: "Bài giải Welcome to Crimson Clinic BONUS 2 trong CDCTF 2026."
mermaid: true
---

<div class="lang-switch" role="tablist" aria-label="Language switch">
  <button class="lang-btn active" role="tab" type="button" data-lang="en" aria-selected="true">EN</button>
  <button class="lang-btn" role="tab" type="button" data-lang="vn" aria-selected="false">VN</button>
</div>

<div class="lang-vn" markdown="1">

## Đề bài

Tìm bài đăng của Emily Peterson về bữa tiệc Giáng sinh công ty. Bài viết nói rõ cô gặp mèo của sếp Jeffery Barrett tại sự kiện này.

## Cách giải

Tên con mèo xuất hiện nguyên văn trong phần chú thích bài đăng: Bubba. Giữ đúng chữ hoa đầu tên theo định dạng đề.

```mermaid
flowchart LR
  A["Tìm bài đăng của Emily"]
  B["Theo dõi câu chuyện bữa tiệc"]
  C["Đọc tên mèo của Jeffery"]
  D["Giữ đúng chữ hoa"]
  A --> B --> C --> D
```

⇒ **Flag:** `cdctf{Bubba}`

</div>

<div class="lang-en" markdown="1">

## Challenge

Find Emily Peterson’s post about the company Christmas party. It says she met her boss Jeffery Barrett’s cat there.

## Solution

The post explicitly names the cat Bubba. Preserve the initial capital letter in the challenge’s requested format.

```mermaid
flowchart LR
  A["Find Emily's post"]
  B["Follow the company-party story"]
  C["Read Jeffery's cat name"]
  D["Preserve the capitalization"]
  A --> B --> C --> D
```

⇒ **Flag:** `cdctf{Bubba}`

</div>
