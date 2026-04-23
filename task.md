# Task Log — Cologne Transit AI

Danh sách các nhiệm vụ đã thực hiện trong quá trình xây dựng dự án.

---

## ✅ Giai đoạn 1: Thiết kế & Thu thập dữ liệu

- [x] Xác định yêu cầu dự án: tìm đường ngắn nhất + admin toggle tuyến
- [x] Chọn tech stack: Flask (backend) + Leaflet.js (frontend) + NetworkX (đồ thị)
- [x] Viết `scripts/fetch_data.py` để thu thập dữ liệu mạng lưới tàu Cologne từ OpenStreetMap (OSMnx)
- [x] Lưu dữ liệu dưới dạng `data/cologne_network.json` (3.634 nodes, 4.744 edges, ~2.5MB)

---

## ✅ Giai đoạn 2: Backend (Flask + NetworkX)

- [x] Xây dựng `backend/engine.py` — class `TransitEngine`:
  - [x] Load đồ thị từ JSON vào NetworkX Graph
  - [x] `get_all_lines()` — lấy danh sách tất cả tuyến tàu
  - [x] `toggle_line()` — bật/tắt tuyến, lưu vào `disabled_lines` set
  - [x] `find_path()` — xây subgraph loại trừ tuyến bị tắt, chạy Dijkstra
  - [x] `get_network_data()` — trả nodes + edges + trạng thái active cho frontend
- [x] Xây dựng `backend/app.py` — Flask REST API:
  - [x] `GET /api/network` — trả toàn bộ đồ thị
  - [x] `GET /api/lines` — trả danh sách tuyến
  - [x] `POST /api/find-path` — tìm đường ngắn nhất
  - [x] `POST /api/admin/toggle-line` — toggle trạng thái tuyến
  - [x] Serve frontend tĩnh (`/` và `/js/*`) trực tiếp qua Flask

---

## ✅ Giai đoạn 3: Frontend (Leaflet.js)

- [x] Xây dựng `frontend/index.html` — layout chính:
  - [x] Dark glassmorphism side panel (Admin v1.0)
  - [x] Loading overlay spinner khi tải dữ liệu
  - [x] Hiển thị điểm đi / điểm đến / tổng khoảng cách
  - [x] Danh sách toggle switch cho từng tuyến tàu
- [x] Xây dựng `frontend/js/api.js` — fetch wrapper gọi tới backend API
- [x] Xây dựng `frontend/js/cologne_map.js`:
  - [x] Khởi tạo Leaflet map, dark tile từ CARTO
  - [x] `renderNetwork()` — vẽ edges (polyline màu theo tuyến) và nodes (circle marker)
  - [x] `selectNode()` — click chọn điểm đi/đến, đổi màu marker
  - [x] `findPath()` — gọi API, vẽ đường vàng dashed lên bản đồ, fit bounds
  - [x] `loadLineControls()` — render danh sách toggle cho Admin panel
  - [x] `toggleLine()` — gọi API toggle, refresh bản đồ, tính lại path
  - [x] `getLineColor()` — màu theo tuyến KVB Cologne chuẩn

---

## ✅ Giai đoạn 4: Debug & Hoàn thiện

- [x] **Sửa bug: Double `window.onload`** — `cologne_map.js` và `index.html` đều đặt `window.onload`, gây conflict. Giữ lại duy nhất ở `index.html`.
- [x] **Sửa bug: `TypeError: unhashable type: 'list'`** — dữ liệu OSM có field `line` là list (nhiều tuyến chung đường), cần normalize về list trước khi dùng `in set`. Thêm hàm `_normalize_line()` và `_is_edge_disabled()` vào `engine.py`.
- [x] **Sửa bug: Frontend không load qua `file://`** — CORS block khi gọi API từ file protocol. Giải pháp: Flask serve luôn cả static frontend.
- [x] Kiểm thử end-to-end: map load, station click, pathfinding, admin toggle
- [x] Cập nhật `README.md` với mô tả đầy đủ, cấu trúc dự án, hướng dẫn chạy, bảng API
- [x] Cập nhật `task.md` liệt kê toàn bộ nhiệm vụ đã hoàn thành
