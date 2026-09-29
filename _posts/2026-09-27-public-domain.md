---
title: "Public Domain"
date: 2026-09-27 12:00:00 +0700
categories: ["H7CTF 2026", "OSINT"]
tags: ["osint"]
description: "Bài giải chi tiết thử thách Public Domain (H7CTF'26 - OSINT / Web)."
math: true
mermaid: true
---

<div class="lang-switch" role="tablist" aria-label="Language switch">
  <button class="lang-btn active" role="tab" type="button" data-lang="en" aria-selected="true">EN</button>
  <button class="lang-btn" role="tab" type="button" data-lang="vn" aria-selected="false">VN</button>
</div>

<div class="lang-vn" markdown="1">

> **Flag:** `H7CTF{4fb846630ae38a205b}`


Bài này có mô tả thử thách:

> Some operators still think their domains are private. Infrastructure has a longer memory than they do.

Đọc description, có 2 cái key ở đây:
* **"operators"**: trong ban tổ chức/infra giải này có Abu, domain cá nhân quen thuộc là `abu.rocks`
* **"Infrastructure has a longer memory than they do"**: câu này gợi ý trực tiếp đến **Certificate Transparency (CT Logs)**. Bất kỳ chứng chỉ SSL nào từng được cấp phát (Let's Encrypt, Cloudflare, DigiCert...) đều bị ghi vĩnh viễn vào log công khai của CA, dù sau đó admin có xóa DNS hay ẩn subdomain đi thì hạ tầng vẫn lưu vết mãi mãi.

---

## Sơ đồ luồng khai thác (Solve Flow)

```mermaid
flowchart TD
    A["Description: Infrastructure has a longer memory than they do"] --> B["Tra cứu CT Logs của abu.rocks (Certspotter / crt.sh)"]
    B --> C["Phát hiện 3 subdomain: clearpane, cdn-static-3, openpgpkey"]
    C --> D["Kiểm tra clearpane.abu.rocks (Whistleblower platform)"]
    C --> E["openpgpkey.abu.rocks (WKD Service)"]
    D --> F["Soi source thấy load https://cdn-static-3.abu.rocks/site.css"]
    F --> G["Phát hiện comment rò rỉ: served to clearpane.abu.rocks, halcyon-strategies.h7tex.com"]
    G --> H["Pivot sang https://halcyon-strategies.h7tex.com"]
    H --> I["Check https://halcyon-strategies.h7tex.com/.well-known/security.txt"]
    I --> J["Trích xuất: Contact curator@abu.rocks và Key xuất bản qua WKD"]
    J --> K["Hash local-part 'curator' bằng SHA-1"]
    K --> L["Encode Z-Base-32: ny73kpdzrpmxkmtuocdhuu4nfffd6k8z"]
    E --> M["Tải PGP Key từ WKD: https://openpgpkey.abu.rocks/.well-known/openpgpkey/abu.rocks/hu/ny73..."]
    L --> M
    M --> N["Parse binary packet OpenPGP (Tag 13 - User ID)"]
    N --> O["Flag trong User ID Comment: Curator (H7CTF{4fb846630ae38a205b})"]
```

---

## Bước 1: Check CT Logs của abu.rocks

Mình dùng Certspotter API để dump toàn bộ subdomain từng được cấp SSL certificate:

```bash
curl -s "https://api.certspotter.com/v1/issuances?domain=abu.rocks&include_subdomains=true&expand=dns_names" | jq -r '.[].dns_names[]' | sort -u
```

Nó nhả ra một đống domain:
```text
abu.rocks
cdn-static-3.abu.rocks
clearpane.abu.rocks
oob.abu.rocks
openpgpkey.abu.rocks
upload.abu.rocks
```

Có 3 cái đáng chú ý:
* `clearpane.abu.rocks`
* `cdn-static-3.abu.rocks`
* `openpgpkey.abu.rocks` (nhìn tên là thấy mùi Web Key Directory của PGP rồi)

---

## Bước 2: Soi `clearpane.abu.rocks` & Cú leak trong file CSS

Mở `https://clearpane.abu.rocks` lên thì thấy đây là trang nhận tin tố cáo nặc danh (*"ClearPane - Secure Anonymous Submissions"*).

F12 soi source xem có gì thì thấy nó load CSS và JS từ subdomain CDN:
```html
<link rel="stylesheet" href="https://cdn-static-3.abu.rocks/site.css">
<script src="https://cdn-static-3.abu.rocks/m.js" data-account="PA-9F3C71E8"></script>
```

Mở file `https://cdn-static-3.abu.rocks/site.css` ra xem thì thấy ngay quả leak cực kỳ bất cẩn của dev:
```css
/* front-end theme -- static asset bundle
 * origin: cdn-static-3.abu.rocks
 * served to: clearpane.abu.rocks, halcyon-strategies.h7tex.com
 * internal use only. do not redistribute.
 */
```

Dev note thẳng luôn là bundle này được dùng chung cho cả `clearpane.abu.rocks` và **`halcyon-strategies.h7tex.com`**!
Trang whistleblower nặc danh hóa ra chung hạ tầng và chủ sở hữu với một công ty bên ngoài.

---

## Bước 3: Pivot sang `halcyon-strategies.h7tex.com`

Vào `https://halcyon-strategies.h7tex.com` thì đây là một công ty xử lý khủng hoảng truyền thông (*Strategic Communications & Narrative Risk Management*).

Mình check các path quen thuộc của RFC web standard, phát hiện ra file `.well-known/security.txt`:
`https://halcyon-strategies.h7tex.com/.well-known/security.txt`

Nội dung trả về:
```text
# Halcyon Strategies -- secure contact
# All sensitive correspondence is encrypted. Our key is published via WKD; fetch it by address.
Contact: mailto:curator@abu.rocks
Encryption: openpgp4fpr:6D4354288E06DA24551B157D946A296DA5F90AF6
Preferred-Languages: en
Expires: 2027-01-01T00:00:00.000Z
```

Có 2 cái key ở đây:
* Email: `curator@abu.rocks`
* Fingerprint: `6D4354288E06DA24551B157D946A296DA5F90AF6`
* Kèm lời dặn: *"Our key is published via WKD; fetch it by address."*

Ban đầu mình thử vác fingerprint lên mấy cái keyserver như `keys.openpgp.org`, `ubuntu`, `mit` để search nhưng đều 404. Đúng như nó bảo, key được host qua WKD.

---

## Bước 4: Lấy PGP Key qua WKD (Web Key Directory)

WKD là chuẩn tự động phát hiện OpenPGP key qua HTTPS dựa vào địa chỉ email.
Cơ chế của nó là:
1. Lấy `local-part` của email: `curator`
2. Băm SHA-1 chuỗi `curator`: `sha1("curator")`
3. Encode kết quả ra bảng mã **z-base-32** (32 ký tự: `ybndrfg8ejkmcpqxot1uwisza345h769`)
4. Theo chuẩn Advanced WKD, URL sẽ là:
   `https://openpgpkey.abu.rocks/.well-known/openpgpkey/abu.rocks/hu/<zbase32_hash>`

Viết script python để băm và kéo key:

```python
import hashlib, urllib.request, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

zbase32 = "ybndrfg8ejkmcpqxot1uwisza345h769"

def encode_zbase32(b):
    res, val, bits = [], 0, 0
    for byte in b:
        val = (val << 8) | byte
        bits += 8
        while bits >= 5:
            bits -= 5
            res.append(zbase32[(val >> bits) & 0x1f])
    if bits > 0:
        res.append(zbase32[(val << (5 - bits)) & 0x1f])
    return "".join(res)

local_part = "curator"
h = hashlib.sha1(local_part.encode('utf-8')).digest()
wkd_hash = encode_zbase32(h)
print("WKD Hash:", wkd_hash)

url = f"https://openpgpkey.abu.rocks/.well-known/openpgpkey/abu.rocks/hu/{wkd_hash}"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, context=ctx) as resp:
    data = resp.read()
    print(f"Status: {resp.status}, Size: {len(data)} bytes")
    with open("key.pgp", "wb") as f:
        f.write(data)
```

Chạy script:
```text
WKD Hash: ny73kpdzrpmxkmtuocdhuu4nfffd6k8z
Status: 200, Size: 436 bytes
```

Kéo thành công file `key.pgp` dung lượng 436 bytes.

---

## Bước 5: Đọc PGP Packet lấy Flag

Mở file `key.pgp` soi bằng strings hoặc parse binary packet RFC 4880:

```python
with open("key.pgp", "rb") as f:
    data = f.read()

import re
print(re.findall(b'[\x20-\x7e]{5,}', data))
```

Output:
```text
[b'Curator (H7CTF{4fb846630ae38a205b}) <curator@abu.rocks>']
```

User ID packet (Tag 13) có format `Name (Comment) <Email>`, tác giả nhét luôn flag vào trường Comment của User ID.

⇒ **Flag:** `H7CTF{4fb846630ae38a205b}`

</div>

<div class="lang-en" markdown="1">

> **Flag:** `H7CTF{4fb846630ae38a205b}`


This article has a challenge description:

> Some operators still think their domains are private. Infrastructure has a longer memory than they do.

Read the description, there are 2 keys here:
* **"operators"**: in the organizing committee/infra of this tournament is Abu, his familiar personal domain is `abu.rocks`
* **"Infrastructure has a longer memory than they do"**: this sentence directly suggests **Certificate Transparency (CT Logs)**. Any SSL certificate that has ever been issued (Let's Encrypt, Cloudflare, DigiCert...) is permanently recorded in the CA's public log, even if the admin later deletes DNS or hides the subdomain, the infrastructure will still be recorded forever.

---

## Solve Flow Diagram

```mermaid
flowchart TD
    A["Description: Infrastructure has a longer memory than they do"] --> B["Look up CT Logs of abu.rocks (Certspotter / crt.sh)"]
    B --> C["Detected 3 subdomains: clearpane, cdn-static-3, openpgpkey"]
    C --> D["Check out clearpane.abu.rocks (Whistleblower platform)"]
    C --> E["openpgpkey.abu.rocks (WKD Service)"]
    D --> F["Look at the source and see the load https://cdn-static-3.abu.rocks/site.css"]
    F --> G["Detected leaked comments: served to clearpane.abu.rocks, halcyon-strategies.h7tex.com"]
    G --> H["Pivot to https://halcyon-strategies.h7tex.com"]
    H --> I["Check https://halcyon-strategies.h7tex.com/.well-known/security.txt"]
    I --> J["Extract: Contact curator@abu.rocks and Key published via WKD"]
    J --> K["Hash local-part 'curator' using SHA-1"]
    K --> L["Encode Z-Base-32: ny73kpdzrpmxkmtuocdhuu4nfffd6k8z"]
    E --> M["Download PGP Key from WKD: https://openpgpkey.abu.rocks/.well-known/openpgpkey/abu.rocks/hu/ny73..."]
    L --> M
    M --> N["Parse binary packet OpenPGP (Tag 13 - User ID)"]
    N --> O["Flag in the User ID comment: Curator (H7CTF{4fb846630ae38a205b})"]
```

---

## Step 1: Check CT Logs of abu.rocks

I use Certspotter API to dump all subdomains that have been issued SSL certificates:

```bash
curl -s "https://api.certspotter.com/v1/issuances?domain=abu.rocks&include_subdomains=true&expand=dns_names" | jq -r '.[].dns_names[]' | sort -u
```

It spits out a bunch of domains:
```text
abu.rocks
cdn-static-3.abu.rocks
clearpane.abu.rocks
oob.abu.rocks
openpgpkey.abu.rocks
upload.abu.rocks
```

There are 3 notable ones:
* `clearpane.abu.rocks`
* `cdn-static-3.abu.rocks`
* `openpgpkey.abu.rocks` (looking at the name, it smells like PGP's Web Key Directory)

---

## Step 2: Look for `clearpane.abu.rocks` & Leaks in the CSS file

Open `https://clearpane.abu.rocks` and see that this is a page that receives anonymous denunciations (*"ClearPane - Secure Anonymous Submissions"*).

F12 looks at the source to see what's there and it loads CSS and JS from the CDN subdomain:
```html
<link rel="stylesheet" href="https://cdn-static-3.abu.rocks/site.css">
<script src="https://cdn-static-3.abu.rocks/m.js" data-account="PA-9F3C71E8"></script>
```

Open the file `https://cdn-static-3.abu.rocks/site.css` and immediately see the extremely careless leak of the dev:
```css
/* front-end theme -- static asset bundle
 * origin: cdn-static-3.abu.rocks
 * served to: clearpane.abu.rocks, halcyon-strategies.h7tex.com
 * internal use only. do not redistribute.
 */
```

Dev notes directly that this bundle is shared by both `clearpane.abu.rocks` and **`halcyon-strategies.h7tex.com`**! The anonymous whistleblower site turned out to share infrastructure and ownership with an outside company.

---

## Step 3: Pivot to `halcyon-strategies.h7tex.com`

Go to `https://halcyon-strategies.h7tex.com` and this is a crisis communications company (*Strategic Communications & Narrative Risk Management*).

I checked the familiar paths of the RFC web standard, discovered the file `.well-known/security.txt`: `https://halcyon-strategies.h7tex.com/.well-known/security.txt`

Return content:
```text
# Halcyon Strategies -- secure contact
# All sensitive correspondence is encrypted. Our key is published via WKD; fetch it by address.
Contact: mailto:curator@abu.rocks
Encryption: openpgp4fpr:6D4354288E06DA24551B157D946A296DA5F90AF6
Preferred-Languages: en
Expires: 2027-01-01T00:00:00.000Z
```

There are 2 keys here:
* Email: `curator@abu.rocks`
* Fingerprint: `6D4354288E06DA24551B157D946A296DA5F90AF6`
* With instructions: *"Our key is published via WKD; fetch it by address."*

At first, I tried to put the fingerprint on keyservers like `keys.openpgp.org`, `ubuntu`, `mit` to search but they all got 404. As it said, the key is hosted via WKD.

---

## Step 4: Get PGP Key via WKD (Web Key Directory)

WKD is a standard that automatically detects OpenPGP keys over HTTPS based on email addresses. Its mechanism is:
1. Get the `local-part` of the email: `curator`
2. SHA-1 hash of the string `curator`: `sha1("curator")`
3. Encode the result to the **z-base-32** charset (32 characters: `ybndrfg8ejkmcpqxot1uwisza345h769`)
4. According to Advanced WKD standards, the URL will be:
`https://openpgpkey.abu.rocks/.well-known/openpgpkey/abu.rocks/hu/<zbase32_hash>`

Write a python script to hash and pull keys:

```python
import hashlib, urllib.request, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

zbase32 = "ybndrfg8ejkmcpqxot1uwisza345h769"

def encode_zbase32(b):
    res, val, bits = [], 0, 0
    for byte in b:
        val = (val << 8) | byte
        bits += 8
        while bits >= 5:
            bits -= 5
            res.append(zbase32[(val >> bits) & 0x1f])
    if bits > 0:
        res.append(zbase32[(val << (5 - bits)) & 0x1f])
    return "".join(res)

local_part = "curator"
h = hashlib.sha1(local_part.encode('utf-8')).digest()
wkd_hash = encode_zbase32(h)
print("WKD Hash:", wkd_hash)

url = f"https://openpgpkey.abu.rocks/.well-known/openpgpkey/abu.rocks/hu/{wkd_hash}"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, context=ctx) as resp:
    data = resp.read()
    print(f"Status: {resp.status}, Size: {len(data)} bytes")
    with open("key.pgp", "wb") as f:
        f.write(data)
```

Run script:
```text
WKD Hash: ny73kpdzrpmxkmtuocdhuu4nfffd6k8z
Status: 200, Size: 436 bytes
```

Successfully pulled the 436 bytes file `key.pgp`.

---

## Step 5: Read PGP Packet to get Flag

Open file `key.pgp` with strings or parse binary packet RFC 4880:

```python
with open("key.pgp", "rb") as f:
    data = f.read()

import re
print(re.findall(b'[\x20-\x7e]{5,}', data))
```

Output:
```text
[b'Curator (H7CTF{4fb846630ae38a205b}) <curator@abu.rocks>']
```

The User ID packet (Tag 13) has the format `Name (Comment) <Email>`, the author puts the flag in the Comment field of the User ID.

⇒ **Flag:** `H7CTF{4fb846630ae38a205b}`
</div>
