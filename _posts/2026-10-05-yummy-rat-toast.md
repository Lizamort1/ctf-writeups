---
title: "Yummy Rat Toast"
date: 2026-10-05 09:30:00 +0700
categories: ["CDCTF 2026", "Password Cracking"]
tags: ["cdctf", "password-cracking"]
description: "Bài giải Yummy Rat Toast trong CDCTF 2026."
---

<div class="lang-switch" role="tablist" aria-label="Language switch">
  <button class="lang-btn active" role="tab" type="button" data-lang="en" aria-selected="true">EN</button>
  <button class="lang-btn" role="tab" type="button" data-lang="vn" aria-selected="false">VN</button>
</div>

<div class="lang-vn" markdown="1">

## Đề bài

Đề cho mã băm MD5 3f1ebefc63dc39f3c9b934a30accb221 và gợi ý về Remy trong Ratatouille: mật khẩu dựa trên tên người bạn của chú chuột.

## Cách giải

Xây từ điển theo nhân vật phim và biến thể có số. Chuỗi “Alfredo Linguini01” cho đúng MD5 đã cho. Đặt nguyên chuỗi này trong cặp ngoặc của flag, gồm cả dấu cách.

⇒ **Flag:** `cdctf{Alfredo Linguini01}`

</div>

<div class="lang-en" markdown="1">

## Challenge

The challenge supplies MD5 hash 3f1ebefc63dc39f3c9b934a30accb221 and a Ratatouille clue: Remy’s password is based on a friend’s name.

## Solution

Build a character-themed word list with numeric variants. “Alfredo Linguini01” hashes to the supplied MD5. Place the exact string inside the flag braces, including its space.

⇒ **Flag:** `cdctf{Alfredo Linguini01}`

</div>
