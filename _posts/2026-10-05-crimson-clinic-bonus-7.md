---
title: "Welcome to Crimson Clinic BONUS 7"
date: 2026-10-05 00:00:00 +0700
categories: ["CDCTF 2026", "OSINT"]
tags: ["cdctf", "osint"]
description: "Bài giải Welcome to Crimson Clinic BONUS 7 trong CDCTF 2026."
mermaid: true
---

<div class="lang-switch" role="tablist" aria-label="Language switch">
  <button class="lang-btn active" role="tab" type="button" data-lang="en" aria-selected="true">EN</button>
  <button class="lang-btn" role="tab" type="button" data-lang="vn" aria-selected="false">VN</button>
</div>

<div class="lang-vn" markdown="1">

## Đề bài

Crimson Social có các bài đăng rời rạc về hẹn hò bí mật. Theo dõi thời gian, địa điểm và lời ám chỉ của Megan Smith cùng một tài khoản khác thay vì chỉ dựa vào một ảnh.

## Cách giải

Những chi tiết về sự kiện speed dating và các lần gặp sau đó ghép được cặp cpickens với meggysmith. Giữ hai username theo thứ tự đó trong flag.

```mermaid
flowchart LR
  A["Gom các bài đăng hẹn hò"]
  B["Đối chiếu thời gian và địa điểm"]
  C["Xác định hai username"]
  D["Ghép đúng thứ tự"]
  A --> B --> C --> D
```

⇒ **Flag:** `cdctf{cpickens-meggysmith}`

</div>

<div class="lang-en" markdown="1">

## Challenge

Crimson Social scatters clues about a secret relationship across multiple posts. Track times, places, and hints from Megan Smith and another account rather than relying on one photo.

## Solution

The speed-dating event and later meetings connect cpickens with meggysmith. Keep the two usernames in that order in the flag.

```mermaid
flowchart LR
  A["Collect the dating posts"]
  B["Cross-check times and locations"]
  C["Identify the two usernames"]
  D["Join them in order"]
  A --> B --> C --> D
```

⇒ **Flag:** `cdctf{cpickens-meggysmith}`

</div>
