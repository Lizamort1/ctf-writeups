---
title: "MadHatter"
date: 2026-10-05 09:30:00 +0700
categories: ["CDCTF 2026", "Cryptography"]
tags: ["cdctf", "cryptography"]
description: "Bài giải MadHatter trong CDCTF 2026."
---

<div class="lang-switch" role="tablist" aria-label="Language switch">
  <button class="lang-btn active" role="tab" type="button" data-lang="en" aria-selected="true">EN</button>
  <button class="lang-btn" role="tab" type="button" data-lang="vn" aria-selected="false">VN</button>
</div>

<div class="lang-vn" markdown="1">

## Đề bài

Gói tệp chứa key.txt và super_secret.txt. Dữ liệu mã hóa dùng AES-256-CBC theo cơ chế OpenSSL cũ không có salt, rồi còn một lớp XOR đơn giản trên bản rõ.

## Cách giải

Băm mật khẩu bằng SHA-256 để tạo khóa, lấy 16 byte đầu của SHA-256(khóa nối mật khẩu) làm IV, giải CBC và bỏ padding. XOR từng byte với 0x0A cho ra flag. Mã hóa lại kết quả và so sánh đúng ciphertext gốc để kiểm chứng.

⇒ **Flag:** `cdctf{We're_@LL_Mad_h3rE!}`

</div>

<div class="lang-en" markdown="1">

## Challenge

The supplied bundle contains key.txt and super_secret.txt. The ciphertext uses unsalted legacy OpenSSL AES-256-CBC, followed by a simple XOR layer over the plaintext.

## Solution

SHA-256 the password to derive the key, take the first 16 bytes of SHA-256(key concatenated with password) as the IV, then decrypt CBC and unpad. XOR each byte with 0x0A to obtain the flag. Re-encrypting the result reproduces the original ciphertext.

⇒ **Flag:** `cdctf{We're_@LL_Mad_h3rE!}`

</div>
