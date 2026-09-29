---
title: "Broken Telephone"
date: 2026-09-27 12:00:00 +0700
categories: ["H7CTF 2026", "Crypto"]
tags: ["crypto"]
description: "Bài giải chi tiết thử thách Broken Telephone (H7CTF'26 - Crypto)."
math: true
mermaid: true
---

<div class="lang-switch" role="tablist" aria-label="Language switch">
  <button class="lang-btn active" role="tab" type="button" data-lang="en" aria-selected="true">EN</button>
  <button class="lang-btn" role="tab" type="button" data-lang="vn" aria-selected="false">VN</button>
</div>

<div class="lang-vn" markdown="1">

> **Flag:** `H7CTF{cd2d1c11-5780-41f3-94c4-feb7ddd2fb72}`


Bài này cho đúng 2 file: `MURMUR-1.2.md` (spec giao thức điều khiển mesh) và `murmur_crypto.py`
(bộ primitive tự chứa). Service là một cái tap: `nc pwn.h7tex.com 41372`, nói chuyện với mình bằng
JSON mỗi dòng một sự kiện.

Đọc spec, có 3 cái key ở đây:

* **"h2 is a function of public transcript bytes only ... a passive observer can recompute it"**:
  tác giả nói thẳng là mình tính lại được binding của chiều dài frame mà không cần khóa nào.
* **"the counter advances once per transport message"**: một *message* gồm nhiều *frame*, nhưng
  nonce chỉ tăng một lần ⇒ **keystream và khóa Poly1305 bị dùng lại giữa các frame**. Đây là quả
  bom nguyên tử của bài.
* **"A frame body is never visible in the clear ... a stock Noise stack cannot even find frame
  boundaries"**: muốn gửi frame giả thì trước hết phải gỡ được mặt nạ độ dài `masked_len = len XOR mask_i`, tức phải có `h2` chuẩn.

---

## Sơ đồ luồng khai thác (Solve Flow)

```mermaid
flowchart TD
    A["Tap: nhận n1, g1, n3 + 2 luồng transport"] --> B["Tính h2 từ transcript công khai<br/>padname - prologue - GW static - e1 - ct1 - e2 - ct2"]
    B --> C["mask_i = LE16(BLAKE2s(h2 || 'MURMUR-len' || LE32(i)))"]
    C --> D["Gỡ mặt nạ độ dài: parse trọn 2 luồng, không còn byte thừa"]
    D --> E["So sánh ciphertext giữa các frame"]
    E --> F["4 frame CONTROL có ct trùng nhau từng byte<br/>- cùng nonce, cùng keystream"]
    F --> G["XOR ct của CONTROL với ct của frame DATA<br/>- ra nguyên cục telemetry MURMUR 12"]
    G --> H["Suy ra plaintext CONTROL toàn số 0<br/>- ct của nó CHÍNH LÀ keystream"]
    F --> I["5 (ct, tag) dưới cùng một khóa Poly1305"]
    I --> J["Hồi quy khối: A(m+1) = r.A(m) + (B- L)r^2 + L r<br/>- 2 phương trình bậc 2, triệt tiêu s"]
    J --> K["Giải bậc 2 mod 2^130-5 (P = 3 mod 4) + duyệt carry e 0..4<br/>- ra đúng cặp (r, s)"]
    H --> L["pt = 01 01 len16 'PROVISION' - ct = ks XOR pt - tag = Poly(r,s)"]
    K --> L
    L --> M["Bơm 1 frame qua /rpc: gateway crown, trả CONTROL chứa secret"]
    M --> N["giải mã reply bằng chính keystream reuse của chiều gateway"]
    N --> O["Flag: H7CTF{cd2d1c11-5780-41f3-94c4-feb7ddd2fb72}"]
```

---

## Bước 1: Tính `h2` cho đúng

`murmur_crypto.py` đã có sẵn `Handshake`, nhưng mình không đi theo nó mà tự nối chuỗi hash cho
chắc. Điểm mấu chốt: `mix_key()` **không** đụng vào `h`, nên `h2` chỉ là một chuỗi BLAKE2s trên dữ
liệu công khai:

```python
def compute_h2(n1, g1, rs_hex, prologue=b''):
    h = M.PROTOCOL_NAME
    h = M.blake2s(h) if len(h) > 32 else h + b'\x00' * (32 - len(h))
    for part in (prologue, bytes.fromhex(rs_hex),
                 n1[:32], n1[32:], g1[:32], g1[32:]):
        h = M.blake2s(h + part)
    return h
```

Static key của gateway `15e8896e...1b16` lấy thẳng từ spec, prologue rỗng.

Thử nghiệm quyết đoán: `masked_len` của frame đầu hai chiều phải cho ra độ dài **hợp lý** khi XOR
với cùng một `mask_0` (vì `i` đếm từ 0 theo từng chiều nhưng binding là chung):

```text
n2g masked 0xa63d   g2n masked 0xa6c0   mask_0 = 0xa6af
=> L(n2g) = 146, L(g2n) = 111     (146 XOR 111 = 0xfd = 0xa63d XOR 0xa6c0  - khớp)
```

Parse cả hai luồng bằng `mask_i` ăn theo `i = 0,1,2,...`:

```text
n2g: 5 frames dùng hết 709/709 byte, types=[1,1,1,1,0], plens=[129,155,112,128,90]
g2n: 4 frames dùng hết 509/509 byte, types=[0,1,1,1], plens=[94,141,100,98]
```

Không thừa một byte nào ⇒ `h2` đã đúng. Trước khi có kết quả này mình đã đoán prologue
`MURMUR/1.2` v.v. và đốt cả tiếng.

---

## Bước 2: Chứng minh keystream bị dùng lại

Soi 4 frame CONTROL đầu tiên: ciphertext của chúng **trùng nhau tuyệt đối trên toàn bộ phần ngắn
hơn** (LCP = đúng độ dài của frame ngắn hơn), chỉ khác nhau ở độ dài:

```text
f0(129) vs f1(155) LCP=129   f0 vs f2(112) LCP=112   f0 vs f3(128) LCP=128
```

Cùng keystream ⇒ cùng nonce. Và vì plaintext chỉ khác nhau ở *lượng padding 0*, nên toàn bộ payload
đều là số 0. Kiểm chứng bằng cách XOR với frame DATA (type 0x00) cùng nhóm:

```python
x = bytes(a ^ b for a, b in zip(ct_ctrl, ct_data))
text
b'MURMUR\x12\x00\x00\x00\x00d\x00\x00\x00\x00\x00\x00\x00\xc3\xff\x01\x00NODE-GUEST-0001\x00...'
```

Ra nguyên xi một blob telemetry (magic, seq=0, uptime=100, rssi=-61, queue=1, node_id). Điều này
cho hai thứ một lúc: **plaintext của CONTROL = 0**, nên `ct` của nó **chính là keystream** (dài tới
155 byte), và DATA cũng nằm cùng nonce.

---

## Bước 3: Hồi phục khóa Poly1305 đã dùng lại

Có keystream rồi vẫn chưa đủ, phải ký được frame mới ⇒ cần `(r, s)`. Với 5 cặp `(message, tag)`
dưới cùng một khóa, mình không brute force mà dùng **chính cấu trúc của Poly1305**.

Gọi `A_j(r) = Σ B_i r^{k+1-i} mod P` và `t_j = (A_j + s) mod 2^128`. Lấy hai frame có **số block
hơn kém đúng 1** (padding 0 làm các block đầu trùng nhau nên đa thức bậc tụt xuống 2):

```text
A_a - r.A_b  ≡  (B_last(a) - L_b) r² + L_a r        (mod P)
```

Thế `A_j ≡ T_j - s` với `T_j = t_j + e_j·2^128`, `e_j ∈ {0..4}` (phần carry bị cắt bởi mod 2^128).
Hai phương trình như vậy có cùng hệ số `s(r-1)` ⇒ **trừ đi là mất `s`**, còn lại phương trình bậc
hai theo `r`. Vì `P = 2^130-5 ≡ 3 (mod 4)` nên căn bậc hai chỉ là `Δ^((P+1)/4)`.

```python
C2 = (Blast_a - L_b) - (Blast_c - L_d)
C1 = (L_a - L_c) + (T_b - T_d)
C0 = T_c - T_a
r = (-C1 ± sqrt(C1^2 - 4*C2*C0)) / (2*C2)
```

Duyệt 5^4 tổ hợp carry, nghiêm túc kiểm tra lại bằng cách tính lại **cả 5 tag** (kể cả frame DATA
có AAD khác):

```text
r=966f0b400b87b9c0a0717380fc4163d
s=67af8648defec1ae91e0779fce7b5de
```

Cặp block phải **thẳng hàng**, tức hiệu số block chỉ là 0
hoặc 1. Với hiệu ≥2 thì các block lệch nhau, đa thức lên bậc 4-10 và coi như không giải được. Bài
này độ dài padding ra đúng chuỗi 7/8/9/10 block.

---

## Bước 4: Dựng frame giả và bơm vào tap

Payload CONTROL hợp lệ là `[opcode][role][cmd_len LE16][cmd]`, opcode 0x01 PROVISION, role 0x01
admin. Không có ràng buộc nào lên nội dung `cmd`, nên `PROVISION` là ăn.

```python
pt  = bytes([0x01, 0x01]) + struct.pack('<H', len(cmd)) + cmd + b'\x00' * pad
ct  = bytes(a ^ b for a, b in zip(ks, pt))
tag = poly1305(r, s, aad=b'\x01', ct)
body = b'\x01' + ct + tag
frame = (length_mask(h2, 0) ^ len(body)).to_bytes(2, 'little') + body
s.sendall(json.dumps({'cmd': 'inject', 'data': frame.hex()}).encode() + b'\n')
```

Gateway sẽ giải mã bằng nonce nào? Đáp án nằm ở chính cái tap — nó **chỉ mirror
chứ không chuyển tiếp** frame của node (nên mới có lệnh `step` để "nhả frame đang buffer"). Vì vậy
frame tiếp theo mà gateway nhận vẫn là **index 0 / nonce 0** — đúng bộ khóa mình vừa khôi phục.

---

## Bước 5: Đọc câu trả lời

Reply về trên luồng `g2n`, parse được ở **index frame 4** (đếm của chiều gateway chạy liên tục):

```text
reply 71B, 1 frame, type=0x01, pl=52
```

Một frame đơn lẻ thì không tự giải mã được, nhưng mình đã có keystream của **nhóm nonce trước đó ở
chiều gateway** (cũng reuse, cũng plaintext 0). Áp vào:

```text
b'\x02+\x00H7CTF{cd2d1c11-5780-41f3-94c4-feb7ddd2fb72}\x00\x00...'
```

Đúng format `[opcode 0x02][secret_len LE16][secret]` với `secret_len = 0x2b = 43`.

Chạy lại ở một phiên hoàn toàn khác (khóa mới, ephemeral mới, `h2` mới) để loại ăn may: ra **cùng
một cờ**.

⇒ **Flag:** `H7CTF{cd2d1c11-5780-41f3-94c4-feb7ddd2fb72}`

</div>

<div class="lang-en" markdown="1">

> **Flag:** `H7CTF{cd2d1c11-5780-41f3-94c4-feb7ddd2fb72}`


This article gives exactly 2 files: `MURMUR-1.2.md` (mesh control protocol spec) and `murmur_crypto.py` (self-contained primitive set). Service is a tap: `nc pwn.h7tex.com 41372`, talking to me in JSON, one event per line.

Read the spec, there are 3 keys here:

* **"h2 is a function of public transcript bytes only ... a passive observer can recompute it"**:
The author directly said that he can recalculate the binding of frame length without any key.
* **"the counter advances once per transport message"**: a *message* consisting of many *frames*, but
nonce only increments once ⇒ **keystream and Poly1305 key are reused between frames**. This is the atomic bomb of the article.
* **"A frame body is never visible in the clear ... a stock Noise stack cannot even find frame
boundaries"**: If you want to send a fake frame, you must first remove the length mask `masked_len = len XOR mask_i`, which means there must be a standard `h2`.

---

## Solve Flow Diagram

```mermaid
flowchart TD
    A["Tap: receive n1, g1, n3 + 2 transport streams"] --> B["Calculate h2 from public transcript<br/>padname - prologue - GW static - e1 - ct1 - e2 - ct2"]
    B --> C["mask_i = LE16(BLAKE2s(h2 || 'MURMUR-len' || LE32(i)))"]
    C --> D["Remove the length mask: parse both streams completely, no extra bytes left"]
    D --> E["Compare ciphertext between frames"]
    E --> F["The 4 CONTROL frames have identical bytes<br/>- same nonce, same keystream"]
    F --> G["XOR ct of CONTROL with ct of frame DATA<br/>- get the whole telemetry MURMUR 12"]
    G --> H["It follows that the CONTROL plaintext, all 0<br/>- ct, IS the keystream"]
    F --> I["5 (ct, tag) under the same Poly1305 key"]
    I --> J["Cubic regression: A(m+1) = r.A(m) + (B- L)r^2 + L r<br/>- 2 quadratic equations, eliminating s"]
    J --> K["Solve the second order mod 2^130-5 (P = 3 mod 4) + browse carry e 0..4<br/>- get the correct pair (r, s)"]
    H --> L["pt = 01 01 len16 'PROVISION' - ct = ks XOR pt - tag = Poly(r,s)"]
    K --> L
    L --> M["Pump 1 frame via /rpc: gateway crown, return CONTROL containing secret"]
    M --> N["decode the reply using the gateway's keystream reuse"]
    N --> O["Flag: H7CTF{cd2d1c11-5780-41f3-94c4-feb7ddd2fb72}"]
```

---

## Step 1: Calculate `h2` correctly

`murmur_crypto.py` already has `Handshake`, but I don't follow it and instead concatenate the hash string myself to be sure. Bottom line: `mix_key()` **doesn't** touch `h`, so `h2` is just a string of BLAKE2s on public data:

```python
def compute_h2(n1, g1, rs_hex, prologue=b''):
    h = M.PROTOCOL_NAME
    h = M.blake2s(h) if len(h) > 32 else h + b'\x00' * (32 - len(h))
    for part in (prologue, bytes.fromhex(rs_hex),
                 n1[:32], n1[32:], g1[:32], g1[32:]):
        h = M.blake2s(h + part)
    return h
```

The gateway's static key `15e8896e...1b16` is taken directly from the spec, the prologue is empty.

Assertive test: The bidirectional first frame's `masked_len` should yield a **reasonable** length when XORed with the same `mask_0` (because `i` counts from 0 in each direction but the binding is common):

```text
n2g masked 0xa63d   g2n masked 0xa6c0   mask_0 = 0xa6af
=> L(n2g) = 146, L(g2n) = 111     (146 XOR 111 = 0xfd = 0xa63d XOR 0xa6c0  - khớp)
```

Parse both streams with `mask_i` following `i = 0,1,2,...`:

```text
n2g: 5 frames dùng hết 709/709 byte, types=[1,1,1,1,0], plens=[129,155,112,128,90]
g2n: 4 frames dùng hết 509/509 byte, types=[0,1,1,1], plens=[94,141,100,98]
```

No extra bytes ⇒ `h2` is correct. Before getting this result, I guessed prologue `MURMUR/1.2` etc. and burned for a whole hour.

---

## Step 2: Prove that the keystream is reused

Look at the first 4 CONTROL frames: their ciphertext is **absolutely identical throughout the shorter part** (LCP = exact length of the shorter frame), only different in length:

```text
f0(129) vs f1(155) LCP=129   f0 vs f2(112) LCP=112   f0 vs f3(128) LCP=128
```

Same keystream ⇒ same nonce. And because the plaintext only differs in *amount of padding 0*, the entire payload is 0. Verify by XORing with DATA frame (type 0x00) of the same group:

```python
x = bytes(a ^ b for a, b in zip(ct_ctrl, ct_data))
text
b'MURMUR\x12\x00\x00\x00\x00d\x00\x00\x00\x00\x00\x00\x00\xc3\xff\x01\x00NODE-GUEST-0001\x00...'
```

Output a telemetry blob in its entirety (magic, seq=0, uptime=100, rssi=-61, queue=1, node_id). This gives two things at once: **CONTROL's plaintext = 0**, so its `ct` **is the keystream** (up to 155 bytes long), and DATA is also in the same nonce.

---

## Step 3: Recover the reused Poly1305 key

Having a keystream is not enough, we must sign a new frame ⇒ need `(r, s)`. With 5 `(message, tag)` pairs under the same key, I do not brute force but use **Poly1305's own structure**.

Let `A_j(r) = Σ B_i r^{k+1-i} mod P` and `t_j = (A_j + s) mod 2^128`. Take two frames with **number of blocks exactly 1** (padding 0 causes the first blocks to overlap so the polynomial degree drops to 2):

```text
A_a - r.A_b  ≡  (B_last(a) - L_b) r² + L_a r        (mod P)
```

Then `A_j ≡ T_j - s` with `T_j = t_j + e_j·2^128`, `e_j ∈ {0..4}` (carry part is cut by mod 2^128). Two such equations have the same coefficient `s(r-1)` ⇒ **subtracting means losing `s`**, leaving a quadratic equation in terms of `r`. Since `P = 2^130-5 ≡ 3 (mod 4)` the square root is just `Δ^((P+1)/4)`.

```python
C2 = (Blast_a - L_b) - (Blast_c - L_d)
C1 = (L_a - L_c) + (T_b - T_d)
C0 = T_c - T_a
r = (-C1 ± sqrt(C1^2 - 4*C2*C0)) / (2*C2)
```

Browse 5^4 carry combinations, seriously check again by recalculating **all 5 tags** (including DATA frames with different AAD):

```text
r=966f0b400b87b9c0a0717380fc4163d
s=67af8648defec1ae91e0779fce7b5de
```

The pair of blocks must be **aligned**, meaning the block difference is only 0 or 1. With a difference ≥2, the blocks are different, the polynomial increases to the order of 4-10 and is considered unsolvable. In this article, the padding length is the correct sequence of 7/8/9/10 blocks.

---

## Step 4: Build a fake frame and inject it into the tap

A valid payload CONTROL is `[opcode][role][cmd_len LE16][cmd]`, opcode 0x01 PROVISION, role 0x01 admin. There are no constraints on the `cmd` content, so `PROVISION` is fine.

```python
pt  = bytes([0x01, 0x01]) + struct.pack('<H', len(cmd)) + cmd + b'\x00' * pad
ct  = bytes(a ^ b for a, b in zip(ks, pt))
tag = poly1305(r, s, aad=b'\x01', ct)
body = b'\x01' + ct + tag
frame = (length_mask(h2, 0) ^ len(body)).to_bytes(2, 'little') + body
s.sendall(json.dumps({'cmd': 'inject', 'data': frame.hex()}).encode() + b'\n')
```

What nonce will the Gateway decode? The answer lies in the tap itself — it **only mirrors, does not forward** the node's frame (hence the `step` command to "release a buffered frame"). So the next frame that the gateway receives is still **index 0 / nonce 0** — the exact set of keys I just restored.

---

## Step 5: Read the answer

Reply back on stream `g2n`, parsed at **index frame 4** (count of continuously running gateway direction):

```text
reply 71B, 1 frame, type=0x01, pl=52
```

A single frame cannot be decoded on its own, but I already have the keystream of the **previous nonce group in the gateway dimension** (also reused, also plaintext 0). Apply:

```text
b'\x02+\x00H7CTF{cd2d1c11-5780-41f3-94c4-feb7ddd2fb72}\x00\x00...'
```

Correct format `[opcode 0x02][secret_len LE16][secret]` with `secret_len = 0x2b = 43`.

Run again in a completely different session (new key, new ephemeral, new `h2`) to eliminate the fluke: output **same flag**.

⇒ **Flag:** `H7CTF{cd2d1c11-5780-41f3-94c4-feb7ddd2fb72}`
</div>
