---
title: "Welcome to Crimson Clinic (2/3)"
date: 2026-10-05 00:00:00 +0700
categories: ["CDCTF 2026", "OSINT"]
tags: ["cdctf", "osint"]
description: "Bài giải Welcome to Crimson Clinic (2/3) trong CDCTF 2026."
mermaid: true
---

<div class="lang-switch" role="tablist" aria-label="Language switch">
  <button class="lang-btn active" role="tab" type="button" data-lang="en" aria-selected="true">EN</button>
  <button class="lang-btn" role="tab" type="button" data-lang="vn" aria-selected="false">VN</button>
</div>

<div class="lang-vn" markdown="1">

## Đề bài

Giai đoạn hai yêu cầu đăng nhập quản trị bằng mật khẩu yếu của một lãnh đạo. Hồ sơ Crimson Social về Jeffery Barrett và gia đình cung cấp thói quen đặt mật khẩu dựa trên vận động viên, năm sinh và ký tự đặc biệt.

## Cách giải

Đối chiếu trò chơi Madden NFL 2004, nhân vật trên bìa là Michael Vick, với năm sinh 1989 của con trai Brandon. Mật khẩu theo mẫu đó mở dashboard quản trị, nơi chứa flag của giai đoạn này.

```mermaid
flowchart LR
  A["Đọc hồ sơ Jeffery Barrett"]
  B["Suy ra Michael Vick và 1989"]
  C["Dựng mật khẩu yếu"]
  D["Đăng nhập dashboard"]
  E["Đọc flag"]
  A --> B --> C --> D --> E
```

⇒ **Flag:** `cdctf{Whats-a-password-policy-anyways?}`

</div>

<div class="lang-en" markdown="1">

## Challenge

Stage two requires administrator access using an executive’s weak password. Crimson Social profiles of Jeffery Barrett and his family reveal a habit of combining an athlete, a birth year, and a special character.

## Solution

Correlate the cover athlete of Madden NFL 2004, Michael Vick, with Brandon’s birth year, 1989. The resulting pattern opens the admin dashboard, which contains this stage’s flag.

```mermaid
flowchart LR
  A["Read Jeffery Barrett's profile"]
  B["Infer Michael Vick and 1989"]
  C["Build the weak password"]
  D["Log in to the dashboard"]
  E["Read the flag"]
  A --> B --> C --> D --> E
```

⇒ **Flag:** `cdctf{Whats-a-password-policy-anyways?}`

</div>
