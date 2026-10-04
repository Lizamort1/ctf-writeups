---
title: "Silicon Snare"
date: 2026-10-05 09:46:00 +0700
categories: ["CSS CTF 2026", "Hardware"]
tags: ["hardware", "logic", "svg"]
description: "Bài giải Silicon Snare: truy vết ma trận cổng logic 32 bit."
---

<div class="lang-switch" role="tablist" aria-label="Language switch">
  <button class="lang-btn active" role="tab" type="button" data-lang="en" aria-selected="true">EN</button>
  <button class="lang-btn" role="tab" type="button" data-lang="vn" aria-selected="false">VN</button>
</div>

<div class="lang-vn" markdown="1">

## Đề bài

Sơ đồ SVG chứa ma trận định tuyến quang học với 32 đầu vào. Một số dây chồng lên nhau nhằm gây nhầm; cần tìm đúng mẫu đầu vào khiến nút Override ở giữa lên mức 1.

## Cách giải

Phóng SVG để truy vết từng dây theo tọa độ, phân biệt giao nhau có kết nối với dây chỉ đi đè lên. Chuyển các nút logic thành các ràng buộc Boolean, rồi giải ngược từ Override về 32 đầu vào.

Mẫu 32 bit tìm được là duy nhất và mô phỏng lại cho Override bằng 1. Chia thành bốn byte ASCII cho ra PASS; giữ nguyên 32 bit trong flag theo yêu cầu của đề.

⇒ **Flag:** `CSSCTF{01010000010000010101001101010011}`

</div>

<div class="lang-en" markdown="1">

## Challenge

The SVG schematic describes a 32-input optical routing matrix. Some wires visually overlap without connecting; find the input pattern that drives the central Override node high.

## Solution

Zoom into the SVG and follow each wire by its coordinates, distinguishing connected junctions from simple crossings. Express the logic nodes as Boolean constraints and solve backward from Override to the 32 inputs.

The resulting 32-bit pattern is unique and evaluates Override to 1. Its four ASCII bytes spell PASS; preserve the full bit string in the challenge’s required flag format.

⇒ **Flag:** `CSSCTF{01010000010000010101001101010011}`

</div>
