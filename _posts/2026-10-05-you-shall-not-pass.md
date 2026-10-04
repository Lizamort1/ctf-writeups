---
title: "You Shall not Pass!"
date: 2026-10-05 09:30:00 +0700
categories: ["CDCTF 2026", "Password Cracking"]
tags: ["cdctf", "password-cracking"]
description: "Bài giải You Shall not Pass! trong CDCTF 2026."
---

<div class="lang-switch" role="tablist" aria-label="Language switch">
  <button class="lang-btn active" role="tab" type="button" data-lang="en" aria-selected="true">EN</button>
  <button class="lang-btn" role="tab" type="button" data-lang="vn" aria-selected="false">VN</button>
</div>

<div class="lang-vn" markdown="1">

## Đề bài

Gói dữ liệu Gandalf's Hat Market chứa tài khoản và mật khẩu đã băm. Đề cho một SHA-256 dài 64 ký tự và yêu cầu tìm username của hàng tương ứng.

## Cách giải

Băm các mật khẩu ứng viên trong tệp rò rỉ. SHA-256 của Este4#Healing khớp chính xác giá trị đích; username trên cùng hàng là CirdanTheShipwright.

⇒ **Flag:** `cdctf{CirdanTheShipwright}`

</div>

<div class="lang-en" markdown="1">

## Challenge

The Gandalf’s Hat Market leak contains accounts and hashed passwords. The challenge supplies a 64-character SHA-256 digest and asks for the matching username.

## Solution

Hash candidate passwords from the leak. SHA-256 of Este4#Healing exactly matches the target digest; the username on that row is CirdanTheShipwright.

⇒ **Flag:** `cdctf{CirdanTheShipwright}`

</div>
