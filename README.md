# Ngô Quý Trường Giang (B23DCAT080) - CTF Writeups & Security Research Blog

Kho lưu trữ mã nguồn Website cá nhân dùng theme **Jekyll Chirpy**, chứa toàn bộ 40 writeup CTF được định dạng chuẩn mực, hỗ trợ song ngữ Anh - Việt (EN / VN toggle tương tự phong cách blog của Duy Long InfosecPTIT), thiết kế tối giản thanh lịch học tập từ anhcd05, tích hợp biểu thức toán học KaTeX, sơ đồ tư duy Mermaid và cơ chế tìm kiếm tức thì.

---

## Danh mục bài giải (40 Challenges)

* **PTITCTF 2026 (14 bài):**
  * *Vòng loại:* Machine Love, PTIT Portfolio Renderer, Palworld Mod, Operation Midnight Drop, baby-heap-V2, baby-heap-V2-revenge, MMO, Winux, GhostVM, Phonefarm, That Should Be NHH.
  * *Chung kết:* Racing Monster, Endgame01, Megalovania.
* **SunshineCTF 2026 (6 bài):**
  * Vecnet (AI / ML), IntMod (Reverse / VM), RoboCall (Forensics / DTMF), FlameOn (Reverse), Helpdesk Freebie (Web), This Code's Got Bars! (Misc).
* **H7CTF'26 / WebVerse (20 bài):**
  * Bartbrack, Broken Telephone, Constraint Yourself, Countersign, Fee Swap, FleetLink, Frame of Reference, Hothouse, Lockstep, Meridian Pay, Model Package Autopsy, Modem Operandi, Overexposed, Public Domain, Rust in Peace, Signed Sealed Delivered, The Ledger Never Sleeps, Toll Story, WorldOutter, Adapter Cartel.

---

## Hướng dẫn Đẩy lên GitHub & Triển khai GitHub Pages

Repository này đã được tích hợp sẵn quy trình CI/CD tự động trong `.github/workflows/pages-deploy.yml`. Khi bạn push mã nguồn lên GitHub, GitHub Actions sẽ tự động biên dịch Jekyll, dựng các trang tĩnh và public lên GitHub Pages mà không cần cài đặt Ruby hay Gem trên máy tính cá nhân.

### Bước 1: Tạo Repository mới trên GitHub
1. Truy cập [GitHub New Repository](https://github.com/new).
2. Đặt tên repository:
   * Nếu muốn web có dạng `https://<username>.github.io` thì đặt tên repo là `<username>.github.io`.
   * Hoặc đặt tên bất kỳ, ví dụ: `ctf-archives` (khi đó link web sẽ là `https://<username>.github.io/ctf-archives`).

### Bước 2: Cập nhật `_config.yml` (nếu cần)
Mở tệp `_config.yml`:
* Nếu tên repo là `<username>.github.io`:
  ```yaml
  url: "https://<username>.github.io"
  baseurl: ""
  ```
* Nếu tên repo là `ctf-archives`:
  ```yaml
  url: "https://<username>.github.io"
  baseurl: "/ctf-archives"
  ```
*(Ghi chú: Giữ nguyên `theme_mode:` để hệ thống bật nút chuyển đổi giao diện Sáng / Tối linh hoạt ở menu góc trái).*

### Bước 3: Đổi Remote Git và Push lên GitHub
Mở terminal tại thư mục `chirpy-blog` và chạy:
```powershell
# Xóa origin mặc định của template starter
git remote remove origin

# Thêm remote dẫn tới GitHub repo của bạn (thay <username> và <repo-name>)
git remote add origin https://github.com/<username>/<repo-name>.git

# Push mã nguồn lên nhánh main
git branch -M main
git push -u origin main
```

### Bước 4: Kích hoạt GitHub Pages từ GitHub Actions
1. Trên trình duyệt, vào trang GitHub repository của bạn.
2. Chọn tab **Settings** -> **Pages** (ở cột bên trái).
3. Tại mục **Build and deployment** -> **Source**:
   * Chuyển từ `Deploy from a branch` sang **`GitHub Actions`**.
4. Chọn tab **Actions** trên repo để theo dõi quá trình build tự động. Chỉ sau khoảng 1-2 phút, trạng thái sẽ báo xanh (Success) kèm đường link website trực tuyến!

---

## Tính năng và Thiết kế

* **Bilingual Switcher (EN / VN):** Nút gạt chuyển đổi song ngữ văn bản tinh tế (`EN   VN`) ở thanh tiêu đề và đầu mỗi bài viết/trang giới thiệu, tự động lưu lựa chọn vào `localStorage`. Không dùng icon, cờ hay emoji AI.
* **Học tập thiết kế từ anhcd05:** Thanh điều hướng cá nhân gọn gàng, hiển thị avatar GitHub thật (`giangnqt`), đầy đủ liên kết mạng xã hội (Facebook, Telegram, Gmail, GitHub) ở góc dưới thanh bên.
* **Light / Dark Mode Toggle:** Nút gạt chuyển đổi giao diện ở thanh điều hướng bên trái, tự động nhận diện chế độ ban đêm của hệ thống.
* **Instant Full-Text Search:** Tìm kiếm bài theo tên, kỹ thuật, category hay flag định dạng tức thì.
* **Math & Mermaid Support:** Hỗ trợ công thức LaTeX qua KaTeX và sơ đồ luồng khai thác trực quan qua Mermaid JS.
