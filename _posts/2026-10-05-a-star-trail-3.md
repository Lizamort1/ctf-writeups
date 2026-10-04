---
title: "A Star Trail 3"
date: 2026-10-05 00:00:00 +0700
categories: ["CSS CTF 2026", "Misc"]
tags: ["misc", "graph", "delaunay", "shortest-path"]
description: "Bài giải A Star Trail 3: phục hồi đồ thị từ phép tam giác hóa Delaunay rồi tìm đường ngắn nhất."
math: true
mermaid: true
---

<div class="lang-switch" role="tablist" aria-label="Language switch">
  <button class="lang-btn active" role="tab" type="button" data-lang="en" aria-selected="true">EN</button>
  <button class="lang-btn" role="tab" type="button" data-lang="vn" aria-selected="false">VN</button>
</div>

<div class="lang-vn" markdown="1">

## Đề bài

Kho lưu trữ mới còn 25.000 tọa độ hành tinh nhưng mất liên kết lân cận. Ta phải khôi phục quy tắc tạo tuyến đường từ kho cũ, tìm hành trình từ `iJ2ZcO` đến `pJk9vy`, rồi lấy một ký tự theo vị trí tuần hoàn từ ID của từng điểm dừng.

```mermaid
flowchart LR
    A["Inspect intact old graph"] --> B["Identify Delaunay rule"]
    B --> C["Rebuild new graph"]
    C --> D["Run Euclidean Dijkstra"]
    D --> E["Extract cyclic ID characters"]
```

## Tìm quy tắc và đường đi

Đồ thị cũ có 29.972 cạnh vô hướng. Tập cạnh này trùng khớp hoàn toàn với phép tam giác hóa Delaunay của tọa độ: không thiếu và không thừa cạnh. Áp dụng đúng quy tắc cho kho mới tạo 74.970 cạnh. Gán trọng số bằng khoảng cách Euclid rồi chạy Dijkstra từ `iJ2ZcO` đến `pJk9vy`.

Đường ngắn nhất có 196 điểm dừng, tính cả hai đầu; tổng chiều dài là `144.0473667550367`. Với điểm dừng đánh số từ 0 (`i`), lấy ký tự thứ `i % 6` trong ID sáu ký tự của nó. Giữ nguyên chữ hoa/thường, ghép các ký tự theo thứ tự đường đi và đặt trong mẫu `CSSCTF{...}`. Bản tái hiện đối chiếu kết quả với thuật toán Dijkstra độc lập của SciPy trên cùng đồ thị.

⇒ **Flag:** `CSSCTF{itr6G8jMTXbOjCmClmMElZxQLqSXqnf53z1Z73liVas3ypn5CJZ4ZGlqZo6Fkc2onoJ6vx5SLfqqEyBotfjpxskQknpUgK9VMfBsFqzc0iEHDbMvv1hwXAo4U1NaimtTt9esb6mskMdUkbgBAjg3TTS1UeTSvf7LFZR0Vxf8KOgkzxHmvO0ifOFaVnwNgwUqpeo9}`

</div>

<div class="lang-en" markdown="1">

## Challenge

The new archive still has 25,000 planetary coordinates but has lost its neighbor links. We must recover the route-generation rule from the intact old archive, find a path from `iJ2ZcO` to `pJk9vy`, and extract a cyclic character from every stop ID.

```mermaid
flowchart LR
    A["Inspect intact old graph"] --> B["Identify Delaunay rule"]
    B --> C["Rebuild new graph"]
    C --> D["Run Euclidean Dijkstra"]
    D --> E["Extract cyclic ID characters"]
```

## Finding the rule and route

The old graph has 29,972 undirected edges. They match the Delaunay triangulation of its coordinates exactly, with no missing or extra edges. Applying the same rule to the new archive produces 74,970 edges. Weight each edge by Euclidean distance and run Dijkstra from `iJ2ZcO` to `pJk9vy`.

The shortest path has 196 stops, counting both endpoints, and total length `144.0473667550367`. For each zero-based stop index `i`, take character `i % 6` from its six-character ID. Preserve case, concatenate in route order, and wrap the result as `CSSCTF{...}`. A reproducer compares the result against an independent SciPy Dijkstra run on the same graph.

⇒ **Flag:** `CSSCTF{itr6G8jMTXbOjCmClmMElZxQLqSXqnf53z1Z73liVas3ypn5CJZ4ZGlqZo6Fkc2onoJ6vx5SLfqqEyBotfjpxskQknpUgK9VMfBsFqzc0iEHDbMvv1hwXAo4U1NaimtTt9esb6mskMdUkbgBAjg3TTS1UeTSvf7LFZR0Vxf8KOgkzxHmvO0ifOFaVnwNgwUqpeo9}`

</div>
