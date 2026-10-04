---
title: "CalcuRATor (1/4)"
date: 2026-10-05 00:00:00 +0700
categories: ["CDCTF 2026", "Reverse Engineering"]
tags: ["cdctf", "reverse-engineering"]
description: "Bài giải CalcuRATor (1/4) trong CDCTF 2026."
---

<div class="lang-switch" role="tablist" aria-label="Language switch">
  <button class="lang-btn active" role="tab" type="button" data-lang="en" aria-selected="true">EN</button>
  <button class="lang-btn" role="tab" type="button" data-lang="vn" aria-selected="false">VN</button>
</div>

<div class="lang-vn" markdown="1">

## Đề bài

Phân tích ELF calculator để tìm tên mà tiến trình con sử dụng sau khi chương trình khởi chạy với quyền root.

## Cách giải

Nhánh độc hại gọi fork rồi setsid, sau đó dùng strncpy ghi chuỗi wpad vào argv[0] và xóa các đối số còn lại. Tên tiến trình mới chính là nội dung flag.

⇒ **Flag:** `cdctf{wpad}`

</div>

<div class="lang-en" markdown="1">

## Challenge

Analyze the calculator ELF to find the process name adopted by its child after launch with root privileges.

## Solution

The malicious branch calls fork and setsid, then uses strncpy to write wpad into argv[0] and clears the remaining arguments. That new process name supplies the flag.

⇒ **Flag:** `cdctf{wpad}`

</div>
