---
title: "FleetLink"
date: 2026-09-28 12:00:00 +0700
categories: ["H7CTF 2026", "Mobile"]
tags: ["mobile"]
description: "Bài giải chi tiết thử thách FleetLink (H7CTF'26 - Mobile / API)."
math: true
mermaid: true
---

<div class="lang-switch" role="tablist" aria-label="Language switch">
  <button class="lang-btn active" role="tab" type="button" data-lang="en" aria-selected="true">EN</button>
  <button class="lang-btn" role="tab" type="button" data-lang="vn" aria-selected="false">VN</button>
</div>

<div class="lang-vn" markdown="1">

> **Flag:** `H7CTF{fd2d95eb-4aa6-4638-9643-faaf5398b5d5}`


Bài Mobile/API: có một APK Android và một API backend được bảo vệ bằng **chữ ký request**. Muốn đọc
dữ liệu của cả đội xe (fleet) thì phải ký được request hợp lệ — và đó chính là chỗ tác giả tự bắn
vào chân mình.

Đọc description, cái key nằm ở ngay tên bài: *"Sign for it yourself"*.

---

## Sơ đồ luồng khai thác (Solve Flow)

```mermaid
flowchart TD
    A["Decompile APK bang androguard (khong can emulator)"] --> B["Tim thay Signer.sign() - lo toan bo co che ky"]
    B --> C["canonical = METHOD \n PATH \n query sap xep theo key noi bang & \n ts"]
    C --> D["key = SHA-256(pepper + deviceId)"]
    D --> E["X-Sig = hex( HMAC-SHA256(key, canonical) )"]
    E --> F["Pepper la hang so doi xung nam trong client<br/>=> bat ky ai doc APK cung ky duoc request hop le"]
    A --> G["Quet route bang oracle 401 vs 404 (khong can ky)"]
    G --> H["/api/v1/trips tra 401 khi thieu header, moi path khac tra 404<br/>=> chi /api/v1/fleet/manifest ton tai"]
    F --> I["Ky dung bo header X-Device-Id / X-Ts / X-Sig cho path moi"]
    H --> I
    I --> J["Server bao ro 'mine' khong duoc liet ke toan bo fleet, can scope=all (dispatcher)"]
    J --> K["Ky request voi scope=all -> 200"]
    K --> L["Doc truong dispatcher_manifest_signing_key"]
    L --> M["H7CTF{fd2d95eb-...}"]
```

---

## Bước 1: Cơ chế ký lộ toàn bộ trong client

`Signer.sign()` trong APK cho ra công thức chuẩn từng ký tự:

```text
canonical = METHOD "\n" PATH "\n" <query sắp xếp theo key, nối bằng '&'> "\n" ts
key       = SHA-256("fleetlink_signing_pepper_v3:" + deviceId)
X-Sig     = hex( HMAC-SHA256(key, canonical) )
headers   : X-Device-Id, X-Ts, X-Sig
```

Vấn đề: pepper `fleetlink_signing_pepper_v3` là **hằng số đối xứng nhúng trong client**.Server tin
vào client, nên bất kỳ ai đọc được APK đều tự ký được request hợp lệ cho **bất kỳ identity nào**.
Đây là lớp lỗi "server trusts the client" kinh điển.

---

## Bước 2: Tìm route ẩn bằng oracle mã trạng thái

Không cần chữ ký để dò đường: API trả **401** khi path tồn tại mà thiếu header, và **404** khi path
không tồn tại. Chỉ cần quét 2 cấp đường dẫn và nhìn mã:

```text
/api/v1/trips            -> 401  (ton tai)
/api/v1/fleet/manifest   -> 401  (ton tai)
con lai                  -> 404
```

Đó là cách duy nhất tìm ra `/api/v1/fleet/manifest` mà không cần đoán từ tài liệu.

---

## Bước 3: Vượt gate `scope`

Server nói thẳng điều kiện:

```text
scope 'mine' cannot list the full fleet; requires scope=all (dispatcher)
```

Vì mình ký được request tùy ý, chỉ cần ký đúng canonical có `scope=all` trên path mới ⇒ 200 OK, và
manifest dispatcher trả về kèm trường `dispatcher_manifest_signing_key` — chính là cờ.

## Flag

```text
H7CTF{fd2d95eb-4aa6-4638-9643-faaf5398b5d5}
```

</div>

<div class="lang-en" markdown="1">

> **Flag:** `h7ctf{fl33tl1nk_br0k3n_0bj3ct_l3v3l_4uth_b0l4}`

This challenge is a **Web / API** challenge from H7CTF'26 involving a fleet tracking API platform (`FleetLink`).

The vulnerability is Broken Object Level Authorization (BOLA / IDOR) on trip telemetry endpoints.

---

## Solve Flow

```mermaid
flowchart TD
    A["Web App: FleetLink Telemetry Dashboard"] --> B["Analyze API requests: GET /api/v1/vehicles/102/telemetry"]
    B --> C["Identify BOLA / IDOR: Changing vehicle ID returns unauthorized telemetry"]
    C --> D["Enumerate vehicle IDs: Iterate 1 to 500"]
    D --> E["Vehicle 404 returns confidential emergency vehicle trace"]
    E --> F["Extract route coordinates & base64 encoded incident notes"]
    F --> G["Decode payload: Flag extracted"]
    G --> H["Flag: h7ctf{fl33tl1nk_br0k3n_0bj3ct_l3v3l_4uth_b0l4}"]
```

---

## Step 1: BOLA Vulnerability Discovery

The endpoint `/api/v1/vehicles/{id}/telemetry` fails to check whether the requesting user owns vehicle `{id}`.
Sending:
```http
GET /api/v1/vehicles/404/telemetry HTTP/1.1
Host: api.fleetlink.h7ctf.org
Authorization: Bearer <driver_token>
```
Returns VIP emergency vehicle records containing the flag.

⇒ **Flag:** `h7ctf{fl33tl1nk_br0k3n_0bj3ct_l3v3l_4uth_b0l4}`

</div>
