---
title: "The Astrolobe Overwrite"
date: 2026-10-05 00:00:00 +0700
categories: ["CSS CTF 2026", "Misc"]
tags: ["misc", "virtual-machine", "self-modifying-code"]
description: "Bài giải The Astrolobe Overwrite: dựng telemetry cho máy ảo tự sửa mã và vượt cổng ba vòng."
mermaid: true
---

<div class="lang-switch" role="tablist" aria-label="Language switch">
  <button class="lang-btn active" role="tab" type="button" data-lang="en" aria-selected="true">EN</button>
  <button class="lang-btn" role="tab" type="button" data-lang="vn" aria-selected="false">VN</button>
</div>

<div class="lang-vn" markdown="1">

## Mục tiêu

The Astrolobe Overwrite chạy một bộ thông dịch tự thay đổi ánh xạ lệnh. Dịch vụ in `beacon` riêng cho mỗi phiên; ta phải gửi vector telemetry để bốn thanh ghi vòng đạt trạng thái đích, rồi dừng đúng cửa sổ 112–128 chu kỳ.

```mermaid
flowchart LR
    A["Read session beacon"] --> B["Compute four target words"]
    B --> C["Track key and opcode permutation"]
    C --> D["Emit state-aware instructions"]
    D --> E["Pad cycles and halt"]
    E --> F["Verify gate and submit"]
```

## Khôi phục trạng thái cần đạt

Bộ kiểm tra cuối dùng modulo `65521` và bốn giá trị gốc `(1, 218, 59611, 783)`. Với từng phiên, đặt `W[i] = (X[i] + beacon) mod 65521`. Payload phải đưa bốn thanh ghi `W` về đúng các giá trị đó.

Opcode không nằm cố định ở cùng vị trí. Slot dispatch bằng `(byte0 ^ key) & 7`; `key` được cập nhật từ giá trị thấp của `W[0]`, còn bảng hoán vị opcode bị đổi sau mỗi lệnh. Vì vậy mỗi byte lệnh phải được tính từ trạng thái VM ngay lúc phát ra, không thể dùng một payload tĩnh.

## Dựng payload

Script mô phỏng VM tiến từng lệnh, phát bốn lệnh `SET` theo thứ tự để nạp thanh ghi đích. Nó thêm các lệnh `SET` ghi lại cùng giá trị nhằm tiêu thụ đủ chu kỳ, rồi phát `HALT`. Bản ghi thử cho thấy payload 412 byte đạt trạng thái `GATE` và dịch vụ phản hồi “TELEMETRY STABILIZED”.

⇒ **Flag:** `CSSCTF{0ur0b0r0s_g00d_j0b_b01s_heh3_67}`

</div>

<div class="lang-en" markdown="1">

## Objective

The Astrolobe Overwrite runs an interpreter whose instruction mapping changes during execution. The service prints a session-specific `beacon`. We must submit a telemetry vector that sets four ring registers to their target state and halts within a 112–128-cycle window.

```mermaid
flowchart LR
    A["Read session beacon"] --> B["Compute four target words"]
    B --> C["Track key and opcode permutation"]
    C --> D["Emit state-aware instructions"]
    D --> E["Pad cycles and halt"]
    E --> F["Verify gate and submit"]
```

## Recovering the target state

The final gate works modulo `65521` and expects base values `(1, 218, 59611, 783)`. For each session, calculate `W[i] = (X[i] + beacon) mod 65521`. The payload must leave the four `W` registers at those exact values.

Opcodes do not occupy fixed positions. The dispatch slot is `(byte0 ^ key) & 7`. The `key` changes using the low byte of `W[0]`, and the opcode permutation swaps after each instruction. Each emitted instruction byte therefore depends on the live VM state; a fixed payload cannot work.

## Building the payload

The solver advances a local VM model instruction by instruction, emitting four `SET` operations to load the target registers. It pads the cycle count with idempotent `SET` operations, then emits `HALT`. The captured run shows a 412-byte payload reaching `GATE`; the service replied “TELEMETRY STABILIZED”.

⇒ **Flag:** `CSSCTF{0ur0b0r0s_g00d_j0b_b01s_heh3_67}`

</div>
