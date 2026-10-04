---
title: "Welcome to Crimson Clinic BONUS 3"
date: 2026-10-05 00:00:00 +0700
categories: ["CDCTF 2026", "OSINT"]
tags: ["cdctf", "osint"]
description: "Bài giải Welcome to Crimson Clinic BONUS 3 trong CDCTF 2026."
---

<div class="lang-switch" role="tablist" aria-label="Language switch">
  <button class="lang-btn active" role="tab" type="button" data-lang="en" aria-selected="true">EN</button>
  <button class="lang-btn" role="tab" type="button" data-lang="vn" aria-selected="false">VN</button>
</div>

<div class="lang-vn" markdown="1">

## Đề bài

Kiểm tra các trang hồ sơ phụ của Crimson Social dẫn đến trang emilys_cat_paradise.html. Mục About Me ở đó chứa một chuỗi Base64.

## Cách giải

Giải mã Base64 cho ra flag hoàn chỉnh. Đường dẫn và trường About Me là hai dấu hiệu để phân biệt trang này với các hồ sơ mồi thông thường.

⇒ **Flag:** `cdctf{cats_r_better_than_dogs}`

</div>

<div class="lang-en" markdown="1">

## Challenge

Inspecting auxiliary Crimson Social profiles leads to emilys_cat_paradise.html. Its About Me field contains a Base64 string.

## Solution

Decoding that string yields the complete flag. The page path and About Me field distinguish this hidden profile from ordinary decoys.

⇒ **Flag:** `cdctf{cats_r_better_than_dogs}`

</div>
