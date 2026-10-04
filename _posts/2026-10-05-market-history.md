---
title: "Market History"
date: 2026-10-05 09:30:00 +0700
categories: ["CDCTF 2026", "OSINT"]
tags: ["cdctf", "osint"]
description: "Bài giải Market History trong CDCTF 2026."
---

<div class="lang-switch" role="tablist" aria-label="Language switch">
  <button class="lang-btn active" role="tab" type="button" data-lang="en" aria-selected="true">EN</button>
  <button class="lang-btn" role="tab" type="button" data-lang="vn" aria-selected="false">VN</button>
</div>

<div class="lang-vn" markdown="1">

## Đề bài

Tra Adam4EVE xác định IChooseYou Market and Industry ở Orvolle có structure ID 1033196707294. Bảng thu nhập theo ngày của trạm chứa cột Buy Order mà đề yêu cầu.

## Cách giải

Lọc từ ngày 16/05/2026 rồi chọn giá trị Buy Order lớn nhất. Ngày 29/08/2026 đạt 11.680.000 ISK; dữ liệu biểu đồ theo ngày xác nhận cùng kết quả.

⇒ **Flag:** `cdctf{2026-08-29_11680000}`

</div>

<div class="lang-en" markdown="1">

## Challenge

Adam4EVE identifies IChooseYou Market and Industry in Orvolle as structure ID 1033196707294. Its daily income table contains the requested Buy Order column.

## Solution

Filter dates from 16 May 2026 and select the maximum Buy Order income. The peak is 11,680,000 ISK on 29 August 2026; the daily chart data independently confirms it.

⇒ **Flag:** `cdctf{2026-08-29_11680000}`

</div>
