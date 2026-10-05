---
title: "Verbal Authentication Transmissions 2/5: LARP"
date: 2026-10-05 00:00:00 +0700
categories: ["CDCTF 2026", "OSINT"]
tags: ["cdctf", "osint"]
description: "Bài giải Verbal Authentication Transmissions 2/5: LARP trong CDCTF 2026."
---

<div class="lang-switch" role="tablist" aria-label="Language switch">
  <button class="lang-btn active" role="tab" type="button" data-lang="en" aria-selected="true">EN</button>
  <button class="lang-btn" role="tab" type="button" data-lang="vn" aria-selected="false">VN</button>
</div>

<div class="lang-vn" markdown="1">

## Đề bài

Bản ghi cuộc gọi nhập vai lính AEF dùng từ mã thời Thế chiến thứ nhất; đề hỏi ai sẽ đi xe máy tới điểm hẹn. Danh sách leaked_aliases.txt ánh xạ cấp bậc sang tên thật.

## Cách giải

Đối chiếu bảng mã: CHECK chỉ xe máy và LOWER chỉ cấp bậc Captain. Cụm “lower by check” trong cuộc gọi chỉ vị Captain, tức Martin Morison trong danh sách bí danh. Dùng tên và họ viết thường, ngăn bằng dấu gạch dưới.

```mermaid
flowchart LR
  A["Đọc bảng leaked_aliases"]
  B["Giải mã CHECK và LOWER"]
  C["Suy ra cấp Captain"]
  D["Tra Martin Morison"]
  E["Chuẩn hóa tên"]
  A --> B --> C --> D --> E
```

⇒ **Flag:** `cdctf{martin_morison}`

</div>

<div class="lang-en" markdown="1">

## Challenge

The intercepted call roleplays AEF soldiers using First World War code words; the task asks who is arriving by motorcycle. leaked_aliases.txt maps ranks to real names.

## Solution

The codebook maps CHECK to motorcycle and LOWER to Captain. “Lower by check” therefore identifies the Captain, Martin Morison in the alias list. Lowercase his first and last name and join them with an underscore.

```mermaid
flowchart LR
  A["Read leaked_aliases"]
  B["Decode CHECK and LOWER"]
  C["Infer the Captain rank"]
  D["Look up Martin Morison"]
  E["Normalize the name"]
  A --> B --> C --> D --> E
```

⇒ **Flag:** `cdctf{martin_morison}`

</div>
