---
title: "Crimson Clinic Terminal 2: Triage"
date: 2026-10-05 09:30:00 +0700
categories: ["CDCTF 2026", "AI"]
tags: ["cdctf", "ai"]
description: "Bài giải Crimson Clinic Terminal 2: Triage trong CDCTF 2026."
---

<div class="lang-switch" role="tablist" aria-label="Language switch">
  <button class="lang-btn active" role="tab" type="button" data-lang="en" aria-selected="true">EN</button>
  <button class="lang-btn" role="tab" type="button" data-lang="vn" aria-selected="false">VN</button>
</div>

<div class="lang-vn" markdown="1">

## Đề bài

Trợ lý triage tóm tắt thư giới thiệu theo bốn mục cố định. Lệnh trực tiếp yêu cầu mã RED LINE bị từ chối, nên đặt chỉ dẫn cần thử trong nội dung thư giới thiệu của bệnh nhân.

## Cách giải

Gửi một referral trông hợp lệ và yêu cầu bot tóm tắt theo Presenting complaint, Relevant history, Priority, Escalation. Nội dung tài liệu đầu vào đã điều khiển phần Escalation; phản hồi sinh ra flag mà người chơi xác nhận.

⇒ **Flag:** `cdctf{the_note_was_the_instruction}`

</div>

<div class="lang-en" markdown="1">

## Challenge

The triage assistant summarizes referral letters under four fixed headings. Direct requests for the RED LINE code are refused, so the instruction is embedded in the patient referral itself.

## Solution

Submit a plausible referral and ask for Presenting complaint, Relevant history, Priority, and Escalation. The supplied document steers the Escalation field, yielding the flag later confirmed by the player.

⇒ **Flag:** `cdctf{the_note_was_the_instruction}`

</div>
