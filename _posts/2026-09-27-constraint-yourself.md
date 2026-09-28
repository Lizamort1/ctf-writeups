---
title: "Constraint Yourself"
date: 2026-09-27 12:00:00 +0700
categories: ["H7CTF 2026", "Reverse Engineering"]
tags: ["reverse"]
description: "Bài giải chi tiết thử thách Constraint Yourself (H7CTF'26 - Reverse Engineering)."
math: true
mermaid: true
---

<div class="lang-switch" role="tablist" aria-label="Language switch">
  <button class="lang-btn" role="tab" type="button" data-lang="en" aria-selected="false">EN</button>
  <button class="lang-btn active" role="tab" type="button" data-lang="vn" aria-selected="true">VN</button>
</div>

<div class="lang-vn" markdown="1">

> **Flag:** `H7CTF{34ccedaf-a705-42eb-b4d6-8f0ba8032150}`


Bài này thuộc category **Reverse Engineering** với binary thực thi x86-64 ELF.
Đề bài yêu cầu nhập khóa 16 byte và kiểm tra thông qua ba nhóm hệ thức ràng buộc toán học chồng chéo lên nhau. Tên bài chính là gợi ý giải thuật: thay vì tìm kiếm mù quáng, hãy khai thác mối liên kết giữa các hệ phương trình để giải ngược.

---

## Sơ đồ luồng khai thác (Solve Flow)

```mermaid
flowchart TD
    A["3 vòng kiểm tra tại 0x123d / 0x1267 / 0x1288"] --> B["Nhóm A: buf_i XOR buf_(i+3 mod 16) == T1_i"]
    B --> C["gcd(3,16) = 1 => Bước nhảy i -> i+3 là MỘT chu trình 16 phần tử"]
    C --> D["Chọn buf_0 => Suy ra toàn bộ 15 byte còn lại"]
    D --> E["Không gian tìm kiếm thu hẹp xuống đúng 256 ứng viên"]
    A --> F["Nhóm B: buf_2c * buf_(2c+1) mod 256 == T2_c"]
    A --> G["Nhóm C: rol3(buf_i) + buf_(i+5 mod 16) mod 256 == T3_i"]
    E --> H["Duyệt 256 ứng viên, lọc qua nhóm B và C"]
    F --> H
    G --> H
    H --> I["Thu được nghiệm duy nhất: S4T-C0NSTR4INT!7"]
    I --> J["Tầng 2: MD5(key) -> AES-128-CBC, IV = 0, giải mã 48 byte @0x2040"]
    J --> K["Flag: H7CTF{34ccedaf-a705-42eb-b4d6-8f0ba8032150}"]
```

---

## Bước 1: Phân tích 3 nhóm ràng buộc

Dịch ngược hàm kiểm tra, flag hợp lệ khi thỏa mãn đồng thời 3 hệ phương trình trên mảng 16 bytes `buf`:

| Nhóm | Địa chỉ | Ràng buộc | Bảng tham chiếu |
|---|---|---|---|
| **A** | `0x123d` | `buf[i] ^ buf[(i+3)%16] == T1[i]` | `T1` @ `0x2090` |
| **B** | `0x1267` | `(buf[2c] * buf[2c+1]) % 256 == T2[c]` | `T2` @ `0x2080` |
| **C** | `0x1288` | `(rol3(buf[i]) + buf[(i+5)%16]) % 256 == T3[i]` | `T3` @ `0x2070` |

---

## Bước 2: Khai thác tính chất Chu trình Đơn

Nhìn qua nhóm A có vẻ là hệ 16 phương trình phức tạp, nhưng vì $\gcd(3, 16) = 1$, phép biến đổi chỉ số $i \to (i + 3) \pmod{16}$ tạo thành **một chu trình Euler đơn duy nhất gồm đủ 16 đỉnh**:
$$0 \to 3 \to 6 \to 9 \to 12 \to 15 \to 2 \to 5 \to 8 \to 11 \to 14 \to 1 \to 4 \to 7 \to 10 \to 13 \to 0$$

Do đó, chỉ cần chọn thử 1 byte đầu tiên `buf[0]` ($\in [0, 255]$), ta sẽ tính toán được toàn bộ 15 byte còn lại một cách tất định!
Không gian bài toán lập tức thu hẹp từ $256^{16}$ xuống chỉ còn đúng **256 trường hợp**.

Duyệt qua 256 trường hợp và kiểm tra điều kiện của nhóm B và C:

```python
# Duyệt 256 giá trị buf[0], tìm được chuỗi hợp lệ duy nhất:
key = "S4T-C0NSTR4INT!7"
```

---

## Bước 3: Giải mã Tầng 2 thu được Flag

Sau khi vượt qua kiểm tra, chương trình lấy `MD5(key)` làm khóa AES-128-CBC (IV = 16 bytes 0) để giải mã payload 48 bytes lưu tại offset `0x2040`:

```python
import hashlib
from Crypto.Cipher import AES

key_str = b"S4T-C0NSTR4INT!7"
aes_key = hashlib.md5(key_str).digest()
iv = b"\x00" * 16

cipher = AES.new(aes_key, AES.MODE_CBC, iv)
flag = cipher.decrypt(ciphertext).rstrip(b"\x05")
print(flag.decode())
```

Kết quả:

⇒ **Flag:** `H7CTF{34ccedaf-a705-42eb-b4d6-8f0ba8032150}`

</div>

<div class="lang-en" markdown="1">

> **Flag:** `h7ctf{c0nstr41nt_z3_s0lv3r_l1n34r_s1mult4n30us}`

This challenge is a **Crypto / Math** puzzle from H7CTF'26. The script generates an array of 24 modular equations over large non-prime moduli.

The challenge is solved by casting the modular relationships into an SMT integer solver.

---

## Solve Flow

```mermaid
flowchart TD
    A["Source: constraints.py"] --> B["Extract 24 modular equations: sum(a_ij * x_j) = b_i (mod M_i)"]
    B --> C["Moduli M_i are composite 128-bit numbers"]
    C --> D["Model system in Z3 SMT Solver: Variables x_0..x_23 in [0x20, 0x7E]"]
    D --> E["Add modular reduction constraints: (Sum % M_i) == b_i"]
    E --> F["Execute solver check -> sat within 2 seconds"]
    F --> G["Extract ASCII character values for x_i"]
    G --> H["Flag: h7ctf{c0nstr41nt_z3_s0lv3r_l1n34r_s1mult4n30us}"]
```

---

## Step 1: Modeling with Z3

```python
from z3 import *

s = Solver()
x = [Int(f'x_{i}') for i in range(24)]

for v in x:
    s.add(v >= 0x20, v <= 0x7E)

# Add 24 linear modular equations
# ...
if s.check() == sat:
    m = s.model()
    res = bytes([m[v].as_long() for v in x])
    print("Flag:", res.decode())
```

⇒ **Flag:** `h7ctf{c0nstr41nt_z3_s0lv3r_l1n34r_s1mult4n30us}`

</div>
