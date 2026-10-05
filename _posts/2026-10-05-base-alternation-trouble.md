---
title: "Base Alternation Trouble"
date: 2026-10-05 00:00:00 +0700
categories: ["CDCTF 2026", "Forensics"]
tags: ["cdctf", "forensics"]
description: "Bài giải Base Alternation Trouble trong CDCTF 2026."
mermaid: true
---

<div class="lang-switch" role="tablist" aria-label="Language switch">
  <button class="lang-btn active" role="tab" type="button" data-lang="en" aria-selected="true">EN</button>
  <button class="lang-btn" role="tab" type="button" data-lang="vn" aria-selected="false">VN</button>
</div>

<div class="lang-vn" markdown="1">

## Đề bài

Tệp bat.wav dài khoảng bốn giây chứa tiếng nói bị dịch lên vùng gần 20 kHz, nên nghe trực tiếp không rõ.

## Cách giải

Phân tích phổ rồi dịch tần xuống dải nghe được, lưu âm thanh phục hồi và đối chiếu kết quả nhận dạng. Ba lượt nhận dạng đều đọc cùng ba từ “lark pepsi shed”.

```mermaid
flowchart LR
  A["Phân tích phổ bat.wav"]
  B["Dịch tín hiệu xuống dải nghe"]
  C["Khôi phục âm thanh"]
  D["Nhận dạng giọng nói"]
  E["Ghép từ thành flag"]
  A --> B --> C --> D --> E
```

⇒ **Flag:** `cdctf{lark pepsi shed}`

</div>

<div class="lang-en" markdown="1">

## Challenge

The roughly four-second bat.wav recording carries speech shifted near 20 kHz, making direct playback unintelligible.

## Solution

Inspect the spectrum, shift the signal back into the audible band, save the recovered audio, and compare independent transcriptions. Three recognition passes agree on “lark pepsi shed”.

```mermaid
flowchart LR
  A["Inspect the bat.wav spectrum"]
  B["Shift the signal into audible range"]
  C["Restore the audio"]
  D["Run speech recognition"]
  E["Assemble the flag words"]
  A --> B --> C --> D --> E
```

⇒ **Flag:** `cdctf{lark pepsi shed}`

</div>
