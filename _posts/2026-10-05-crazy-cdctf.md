---
title: "Crazy?"
date: 2026-10-05 00:00:00 +0700
categories: ["CDCTF 2026", "Misc"]
tags: ["cdctf", "misc"]
description: "Bài giải Crazy? trong CDCTF 2026."
---

<div class="lang-switch" role="tablist" aria-label="Language switch">
  <button class="lang-btn active" role="tab" type="button" data-lang="en" aria-selected="true">EN</button>
  <button class="lang-btn" role="tab" type="button" data-lang="vn" aria-selected="false">VN</button>
</div>

<div class="lang-vn" markdown="1">

## Đề bài

Tệp văn bản 496.800 byte lặp một khối chín dòng mười lần. So sánh các khối cho thấy đúng một bản thay câu “I was crazy once.” bằng phiên bản leetspeak.

## Cách giải

Sai khác bắt đầu ở offset 297115. Thay đoạn khác biệt trở lại câu gốc làm cả mười khối giống hệt nhau; vì vậy lấy nguyên văn đoạn leetspeak, giữ cả khoảng trắng.

⇒ **Flag:** `cdctf{1 w@5 cr@zy 0nc3}`

</div>

<div class="lang-en" markdown="1">

## Challenge

The 496,800-byte text repeats one nine-line block ten times. Comparing the blocks reveals a single copy where “I was crazy once.” is replaced with leetspeak.

## Solution

The difference begins at offset 297115. Restoring the original sentence makes all ten blocks identical, so the exceptional leetspeak text, including its spaces, is the answer.

⇒ **Flag:** `cdctf{1 w@5 cr@zy 0nc3}`

</div>
