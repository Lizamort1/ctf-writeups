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

Khôi phục passphrase từ gợi ý và dùng GnuPG giải thông điệp. Tệp plaintext sau giải mã bắt đầu bằng “Good work:” rồi chứa flag; giữ nguyên chữ hoa và chữ số trong chuỗi.

⇒ **Flag:** `cdctf{pr3t7y_g00d_piv4cy_fl4G}`

</div>

<div class="lang-en" markdown="1">

## Challenge

The challenge provides a passphrase-protected PGP message. Use the ASCII-armored message, reference word list, and PGP key to test the passphrase.

## Solution

Recover the passphrase from the clues and decrypt the message with GnuPG. The resulting plaintext begins “Good work:” and then contains the flag; preserve its original capitalization and digits.

⇒ **Flag:** `cdctf{pr3t7y_g00d_piv4cy_fl4G}`

</div>
