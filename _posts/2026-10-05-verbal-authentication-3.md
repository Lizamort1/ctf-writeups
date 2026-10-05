---
title: "Verbal Authentication Transmissions 3/5: Pretty Good Passphrase"
date: 2026-10-05 00:00:00 +0700
categories: ["CDCTF 2026", "Cryptography"]
tags: ["cdctf", "cryptography"]
description: "Bài giải Verbal Authentication Transmissions 3/5: Pretty Good Passphrase trong CDCTF 2026."
---

<div class="lang-switch" role="tablist" aria-label="Language switch">
  <button class="lang-btn active" role="tab" type="button" data-lang="en" aria-selected="true">EN</button>
  <button class="lang-btn" role="tab" type="button" data-lang="vn" aria-selected="false">VN</button>
</div>

<div class="lang-vn" markdown="1">

## Đề bài

Đề phát một thông điệp PGP được khóa bằng passphrase. Dùng bản mã ASCII-armored, bảng từ tham chiếu và khóa PGP để kiểm tra passphrase.

## Cách giải

Passphrase `Password123!` mở được khóa PGP. Dùng GnuPG giải thông điệp; kiểm tra CRC24 của bản mã và kết quả `GOODMDC`. Bản rõ bắt đầu bằng “Good work:” rồi chứa flag; giữ nguyên chữ hoa và chữ số trong chuỗi.

```mermaid
flowchart LR
  A["Lấy bản mã PGP"]
  B["Thử passphrase Password123!"]
  C["Giải bằng GnuPG"]
  D["Kiểm tra CRC24 và MDC"]
  E["Đọc flag"]
  A --> B --> C --> D --> E
```

⇒ **Flag:** `cdctf{pr3t7y_g00d_piv4cy_fl4G}`

</div>

<div class="lang-en" markdown="1">

## Challenge

The challenge provides a passphrase-protected PGP message. Use the ASCII-armored message, reference word list, and PGP key to test the passphrase.

## Solution

The passphrase `Password123!` unlocks the PGP key. Decrypt the message with GnuPG, checking the ciphertext CRC24 and `GOODMDC` result. The plaintext begins “Good work:” and then contains the flag; preserve its capitalization and digits.

```mermaid
flowchart LR
  A["Collect the PGP ciphertext"]
  B["Try Password123!"]
  C["Decrypt with GnuPG"]
  D["Check CRC24 and MDC"]
  E["Read the flag"]
  A --> B --> C --> D --> E
```

⇒ **Flag:** `cdctf{pr3t7y_g00d_piv4cy_fl4G}`

</div>
