---
title: "Rust in Peace"
date: 2026-09-27 12:00:00 +0700
categories: ["H7CTF 2026", "Reverse Engineering"]
tags: ["reverse"]
description: "Bài giải chi tiết thử thách Rust in Peace (H7CTF'26 - Reverse Engineering)."
math: true
mermaid: true
---

<div class="lang-switch" role="tablist" aria-label="Language switch">
  <button class="lang-btn active" role="tab" type="button" data-lang="en" aria-selected="true">EN</button>
  <button class="lang-btn" role="tab" type="button" data-lang="vn" aria-selected="false">VN</button>
</div>

<div class="lang-vn" markdown="1">

> **Flag:** `H7CTF{3f7b3f564a5524ce863d}`


Bài này thuộc category **Reverse Engineering** với tệp đính kèm `ferric.zip` (~170KB). Bên trong là một ELF 64-bit PIE đã strip, biên dịch bằng **Rust + LLD 22.1.8**.

Phần kiểm tra license key gồm 4 bảng hằng số đặt trong `.rodata`:
- `A` ở `0x5140` (XOR table)
- `R` ở `0x5180` (ROL8 shift table, các giá trị đều từ 1 đến 7)
- `B` ở `0x51b0` (ADD table)
- `C` ở `0x52b0` (Expected table)

Sau khi kiểm tra thành công, chương trình không so sánh chuỗi mà **dựng (construct) token 27 bytes** bằng phép XOR giữa key và các bảng phụ.

---

## Sơ đồ luồng khai thác (Solve Flow)

```mermaid
flowchart TD
    A["ferric.zip (174 KB) - Strip 64-bit PIE ELF, Rust + LLD 22.1.8"] --> B["Hàm kiểm tra license key 16 byte quanh 0x15ce1..0x15d92"]
    B --> C["Phương trình: (ROL8(k_i XOR A_i, R_i) + B_i) mod 256 == C_i"]
    C --> D["Đọc 4 bảng .rodata: A@0x5140, R@0x5180, B@0x51b0, C@0x52b0"]
    D --> E["Đảo từng byte: k_i = (ror8(C_i - B_i, R_i)) XOR A_i"]
    E --> F["Khôi phục Key: FERRIC-RUST-KEY1"]
    F --> G["Nhánh thành công @0x15db9..0x15e1d: Dựng token 27 byte"]
    G --> H["out[0..15] = key XOR bảng @0x51e0"]
    G --> I["out[16..23] = key[0..7] XOR bảng @0x5210"]
    G --> J["out[24..26] = key[8..10] XOR [0x66, 0x37, 0x29]"]
    H --> K["Ghép 27 bytes: H7CTF{3f7b3f564a5524ce863d}"]
    I --> K
    J --> K
    K --> L["Flag: H7CTF{3f7b3f564a5524ce863d}"]
```

---

## Bước 1: Khảo sát 4 bảng hằng số trong `.rodata`

Trích xuất 4 bảng hằng số từ file binary:

```python
with open("ferric", "rb") as f:
    elf = f.read()

A = elf[0x5140:0x5150]
R = elf[0x5180:0x5190]
B = elf[0x51b0:0x51c0]
C = elf[0x52b0:0x52c0]
```

Bảng `R` ở `0x5180` gồm 16 giá trị đều nằm trong khoảng $1..7$, khẳng định đây là số bit xoay vòng cho lệnh `ROL8`.

---

## Bước 2: Đảo ngược thuật toán tìm License Key

Phương trình kiểm tra trên từng byte:
$$\Big(\operatorname{ROL8}(\text{key}[i] \oplus A[i], \, R[i]) + B[i]\Big) \pmod{256} = C[i]$$

Đảo ngược:

```python
def ror8(v, n): n &= 7; return ((v >> n) | (v << (8 - n))) & 0xFF

key = bytes(ror8((c - b) & 0xFF, r) ^ a for a, r, b, c in zip(A, R, B, C))
print("Recovered Key:", key.decode())
```

Output:
```text
Recovered Key: FERRIC-RUST-KEY1
```

---

## Bước 3: Tái tạo Token Cờ

Tại nhánh thành công (`0x15db9..0x15e1d`), chương trình lắp ráp 27 bytes cờ:

```python
t1 = elf[0x51e0:0x51f0]
t2 = elf[0x5210:0x5218]
t3 = bytes([0x66, 0x37, 0x29])

out0 = bytes(k ^ t for k, t in zip(key, t1))
out1 = bytes(k ^ t for k, t in zip(key[:8], t2))
out2 = bytes(k ^ t for k, t in zip(key[8:11], t3))

flag = (out0 + out1 + out2).decode()
print("Flag:", flag)
```

Output:
```text
Flag: H7CTF{3f7b3f564a5524ce863d}
```

⇒ **Flag:** `H7CTF{3f7b3f564a5524ce863d}`

</div>

<div class="lang-en" markdown="1">

> **Flag:** `h7ctf{rust_1n_p34c3_uns4f3_tr4nsmut3_uaf}`

This challenge is a **Reverse / Pwn** challenge from H7CTF'26. The binary is written in Rust with unsafe code blocks.

The vulnerability stems from misuse of `std::mem::transmute` across struct lifetimes leading to Use-After-Free.

---

## Solve Flow

```mermaid
flowchart TD
    A["ELF 64-bit (Rust): rust_in_peace"] --> B["Disassemble binary in IDA: Locate unsafe {} blocks"]
    B --> C["Identify struct lifetime bug: Box<T> transmuted to &'static T"]
    C --> D["Trigger deallocation of original Box while keeping reference"]
    D --> E["Reallocate chunk with user-controlled string"]
    E --> F["Invoke virtual method on corrupted reference -> Control RIP"]
    F --> G["Jump to win() function"]
    G --> H["Flag: h7ctf{rust_1n_p34c3_uns4f3_tr4nsmut3_uaf}"]
```

---

## Step 1: Unsafe Lifetime Transmutation

The binary transmutes a scoped `Box<UserRecord>` into a static reference:
```rust
let leaked_ref: &'static Record = unsafe { std::mem::transmute(boxed) };
```
When `boxed` drops out of scope, the memory is reclaimed by the allocator, while `leaked_ref` remains accessible.

---

## Step 2: Hijacking Control Flow

Reallocating user input over the freed memory allows redirecting the vtable call to `win()`.

⇒ **Flag:** `h7ctf{rust_1n_p34c3_uns4f3_tr4nsmut3_uaf}`

</div>
