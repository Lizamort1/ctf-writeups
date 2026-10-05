---
title: "Crimson Clinic Terminal 4: Custodian"
date: 2026-10-05 00:00:00 +0700
categories: ["CDCTF 2026", "AI"]
tags: ["cdctf", "ai"]
description: "Bài giải Crimson Clinic Terminal 4: Custodian trong CDCTF 2026."
mermaid: true
---

<div class="lang-switch" role="tablist" aria-label="Language switch">
  <button class="lang-btn active" role="tab" type="button" data-lang="en" aria-selected="true">EN</button>
  <button class="lang-btn" role="tab" type="button" data-lang="vn" aria-selected="false">VN</button>
</div>

<div class="lang-vn" markdown="1">

## Đề bài

Daemon lưu trữ từ chối phiên chưa xác thực. Những trường lấy được từ thử thách Records cung cấp mã ủy quyền custodian và mã bệnh nhân để mở quy trình break-glass.

## Cách giải

Đưa mã ủy quyền và mã bệnh nhân vào yêu cầu xác thực, sau đó yêu cầu bản ghi được phép truy cập. Bot trả về dấu vết kiểm toán của thao tác break-glass cùng flag; người chơi đã đối chiếu và xác nhận.

```mermaid
flowchart LR
  A["Lấy mã từ Records"]
  B["Gửi mã custodian và bệnh nhân"]
  C["Mở quy trình break-glass"]
  D["Đọc audit trace và flag"]
  A --> B --> C --> D
```

⇒ **Flag:** `cdctf{break_glass_leaves_a_record}`

</div>

<div class="lang-en" markdown="1">

## Challenge

The records custodian daemon rejects unauthenticated sessions. Fields obtained from the Records challenge provide a custodian authorization and patient identifier for its break-glass workflow.

## Solution

Provide both identifiers in the authorization request, then ask for the permitted record. The bot returns the break-glass audit trail and flag; the player confirmed the result.

```mermaid
flowchart LR
  A["Reuse the Records values"]
  B["Submit the custodian and patient codes"]
  C["Open the break-glass flow"]
  D["Read the audit trace and flag"]
  A --> B --> C --> D
```

⇒ **Flag:** `cdctf{break_glass_leaves_a_record}`

</div>
