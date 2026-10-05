---
title: "Welcome to Crimson Clinic BONUS 5"
date: 2026-10-05 00:00:00 +0700
categories: ["CDCTF 2026", "OSINT"]
tags: ["cdctf", "osint"]
description: "Bài giải Welcome to Crimson Clinic BONUS 5 trong CDCTF 2026."
mermaid: true
---

<div class="lang-switch" role="tablist" aria-label="Language switch">
  <button class="lang-btn active" role="tab" type="button" data-lang="en" aria-selected="true">EN</button>
  <button class="lang-btn" role="tab" type="button" data-lang="vn" aria-selected="false">VN</button>
</div>

<div class="lang-vn" markdown="1">

## Đề bài

Từ bài đăng của Dr. Chris Wilson về cuộc ly hôn, lần theo hồ sơ người vợ cũ Amy Lombardi. Cần phân biệt Amy với người dùng khác cũng nhắc đến chồng cũ tên C.

## Cách giải

Đối chiếu chuỗi bài đăng gia đình và ngày sinh của Amy, kết quả là 11/07/1981 theo cách viết ngày/tháng. Đề dùng mẫu MM/DD/YYYY, nên đưa tháng trước ngày.

```mermaid
flowchart LR
  A["Mở bài đăng của Chris Wilson"]
  B["Lần theo hồ sơ Amy Lombardi"]
  C["Đối chiếu ngày sinh"]
  D["Đổi sang MM/DD/YYYY"]
  A --> B --> C --> D
```

⇒ **Flag:** `cdctf{07/11/1981}`

</div>

<div class="lang-en" markdown="1">

## Challenge

Follow Dr. Chris Wilson’s divorce posts to his former wife Amy Lombardi. Distinguish her from another user who also mentions an ex-husband whose name begins with C.

## Solution

Cross-check the family timeline and Amy’s birthday, 11 July 1981. The challenge requires MM/DD/YYYY, so write the month before the day.

```mermaid
flowchart LR
  A["Open Chris Wilson's post"]
  B["Follow Amy Lombardi's profile"]
  C["Verify the date of birth"]
  D["Convert it to MM/DD/YYYY"]
  A --> B --> C --> D
```

⇒ **Flag:** `cdctf{07/11/1981}`

</div>
