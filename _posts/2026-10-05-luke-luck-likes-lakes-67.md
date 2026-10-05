---
title: "Luke Luck Likes Lakes 67"
date: 2026-10-05 00:00:00 +0700
categories: ["CDCTF 2026", "OSINT"]
tags: ["cdctf", "osint"]
description: "Bài giải Luke Luck Likes Lakes 67 trong CDCTF 2026."
mermaid: true
---

<div class="lang-switch" role="tablist" aria-label="Language switch">
  <button class="lang-btn active" role="tab" type="button" data-lang="en" aria-selected="true">EN</button>
  <button class="lang-btn" role="tab" type="button" data-lang="vn" aria-selected="false">VN</button>
</div>

<div class="lang-vn" markdown="1">

## Đề bài

Ảnh bản đồ đã ẩn nhãn địa danh. So đường viền hồ và con đường chạy sát bờ phía bắc với dữ liệu bản đồ thay vì đoán quốc gia từ màu nền.

## Cách giải

Hình dạng khớp hồ Chūzenji ở Nikkō, gồm cả đường ven bờ phía bắc. Đề yêu cầu tên quốc gia của hồ, nên trả lời Japan.

```mermaid
flowchart LR
  A["So khớp đường viền hồ"]
  B["Đối chiếu đường ven bờ"]
  C["Nhận dạng hồ Chūzenji"]
  D["Lấy tên quốc gia"]
  A --> B --> C --> D
```

⇒ **Flag:** `cdctf{Japan}`

</div>

<div class="lang-en" markdown="1">

## Challenge

The map image removes place labels. Compare the shoreline and the road along its northern edge against map data instead of guessing from colors.

## Solution

The shape matches Lake Chūzenji in Nikkō, including the northern lakeside road. The prompt asks for the country, so the answer is Japan.

```mermaid
flowchart LR
  A["Match the lake outline"]
  B["Compare the shoreline road"]
  C["Identify Lake Chūzenji"]
  D["Extract the country"]
  A --> B --> C --> D
```

⇒ **Flag:** `cdctf{Japan}`

</div>
