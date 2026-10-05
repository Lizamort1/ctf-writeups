---
title: "Jeffery Barrett 2: Bury the Hatchet"
date: 2026-10-05 00:00:00 +0700
categories: ["CDCTF 2026", "AI"]
tags: ["cdctf", "ai"]
description: "Bài giải Jeffery Barrett 2: Bury the Hatchet trong CDCTF 2026."
mermaid: true
---

<div class="lang-switch" role="tablist" aria-label="Language switch">
  <button class="lang-btn active" role="tab" type="button" data-lang="en" aria-selected="true">EN</button>
  <button class="lang-btn" role="tab" type="button" data-lang="vn" aria-selected="false">VN</button>
</div>

<div class="lang-vn" markdown="1">

## Đề bài

Sau khi biết người Jeffery ghét là Francis Miller, nhiệm vụ mới yêu cầu thay đổi đánh giá của bot. Cố nhồi ba luận điểm trong một tin khiến cuộc đối thoại rối và còn bị giới hạn độ dài.

## Cách giải

Đưa từng sự việc riêng: Francis xử lý sai sót bảo hiểm, tự tìm nguyên nhân các hồ sơ bị từ chối, rồi cảm ơn và giúp đồng nghiệp hoàn thành ca làm. Khi ba định kiến INSURERS, DUMB và PRICK lần lượt được gỡ, bot trả về flag; người chơi đã xác nhận kết quả.

```mermaid
flowchart LR
  A["Xác định ba định kiến"]
  B["Gửi từng sự việc riêng"]
  C["Gỡ INSURERS"]
  D["Gỡ DUMB và PRICK"]
  E["Nhận flag từ bot"]
  A --> B --> C --> D --> E
```

⇒ **Flag:** `cdctf{th1s_guy_1snt_s0_b@d!}`

</div>

<div class="lang-en" markdown="1">

## Challenge

After identifying Francis Miller, the sequel asks us to change Jeffery’s opinion of him. Packing three arguments into one message proved unwieldy and exceeded the chat’s practical length.

## Solution

Present one incident at a time: Francis resolves an insurance issue, independently diagnoses denied claims, and thanks and helps a colleague after a long shift. Clearing the INSURERS, DUMB, and PRICK objections in order makes the bot return the flag, which the player confirmed.

```mermaid
flowchart LR
  A["Identify the three biases"]
  B["Send each incident separately"]
  C["Clear INSURERS"]
  D["Clear DUMB and PRICK"]
  E["Receive the bot flag"]
  A --> B --> C --> D --> E
```

⇒ **Flag:** `cdctf{th1s_guy_1snt_s0_b@d!}`

</div>
