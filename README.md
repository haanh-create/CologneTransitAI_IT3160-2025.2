# 🚇 Cologne Transit AI

> Hệ thống tìm đường đi ngắn nhất cho mạng lưới giao thông công cộng tại **Cologne (Köln), Đức**.  
> Dự án sử dụng dữ liệu thực từ OpenStreetMap, thuật toán Dijkstra có heuristic chuyển tuyến, và giao diện bản đồ tương tác.

---

## 📌 Mô tả dự án

Cologne Transit AI là một ứng dụng web full-stack cho phép:

- **Người dùng (User):** Chọn 2 trạm bất kỳ trên bản đồ → Hệ thống tự động tìm và hiển thị **đường đi ngắn nhất** kèm **lộ trình chi tiết** (đi tuyến nào, từ trạm nào đến trạm nào).
- **Quản trị viên (Admin):** Bật/tắt từng tuyến tàu theo 3 nhóm (Rail / Sub / Train) để **mô phỏng sự cố hoặc bảo trì**, hệ thống sẽ tự tính lại đường đi tránh tuyến bị vô hiệu hóa.

Dữ liệu mạng lưới giao thông (**3.634 trạm, 4.744 đoạn đường**) được thu thập trực tiếp từ **OpenStreetMap** thông qua thư viện `osmnx`.

---

## 🏗️ Cấu trúc dự án

```
CologneTransitAI/
├── backend/
│   ├── app.py          # Flask API server, đồng thời serve frontend
│   └── engine.py       # TransitEngine: load đồ thị, Dijkstra + transfer penalty, toggle tuyến
│
├── frontend/
│   ├── index.html      # Giao diện chính: sidebar + bản đồ Leaflet
│   └── js/
│       ├── api.js          # Hàm gọi API backend (fetch wrapper)
│       └── cologne_map.js  # Leaflet.js: render bản đồ, markers, path, lộ trình
│
├── data/
│   └── cologne_network.json    # Dữ liệu đồ thị OSM (nodes + edges)
│
├── scripts/
│   └── fetch_data.py   # Script thu thập dữ liệu từ OpenStreetMap
│
├── pyproject.toml      # Khai báo project (dùng với uv)
├── requirements.txt    # Danh sách thư viện Python
└── README.md
```

---

## 🚀 Cách chạy dự án

### Yêu cầu
- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (khuyến nghị) hoặc pip

### Bước 1 — Tạo môi trường ảo và cài thư viện

**Dùng `uv` (khuyến nghị — nhanh hơn pip ~10×):**
```powershell
uv venv .venv
uv pip install -r requirements.txt
```

**Hoặc dùng pip truyền thống:**
```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

> Các thư viện chính: `flask`, `flask-cors`, `networkx`, `osmnx`, `geopandas`

### Bước 2 — Kích hoạt môi trường ảo

```powershell
.venv\Scripts\activate
```

### Bước 3 — Chạy server

```bash
python backend/app.py
```

Server sẽ khởi động tại: **http://localhost:5000**

> Flask tự động serve cả frontend — **không cần** mở file HTML riêng hay cài thêm Live Server.

### Bước 4 — Mở trình duyệt

Truy cập: [http://localhost:5000](http://localhost:5000)

---

## 🎮 Hướng dẫn sử dụng

| Thao tác | Kết quả |
|----------|---------|
| Click vào 1 trạm trên bản đồ | Chọn **điểm đi** (marker xanh lá) |
| Click vào trạm thứ 2 | Chọn **điểm đến** (marker đỏ) → tự động tìm đường |
| Đường đỏ nét đứt xuất hiện | Đường đi ngắn nhất đã được tìm thấy |
| Kéo xuống trong sidebar | Xem **lộ trình chi tiết** (đi tuyến nào, từ đâu đến đâu, bao nhiêu km) |
| Gạt công tắc trong Admin panel | Vô hiệu hóa / kích hoạt tuyến tàu |
| Nhấn ▼/▶ trên nhóm Rail/Sub/Train | Thu gọn / mở rộng danh sách tuyến |
| Nhấn ☀️/🌙 góc phải | Chuyển giao diện sáng / tối |
| Nhấn "Xóa chọn điểm" | Reset lại lựa chọn và lộ trình |

---

## 🎨 Màu sắc tuyến đường

| Loại | Màu | Mô tả |
|------|-----|-------|
| 🔵 **Rail** | `#0085c8` xanh lam | Tuyến có tên đặc biệt (Innenstadttunnel, SB-Nord…) |
| 🟢 **Sub** | `#00c666` xanh lá | KVB Stadtbahn — số tuyến 1–99 |
| 🟡 **Train** | `#ffd600` vàng | Tàu khu vực Regional — số 4 chữ số (26xx, 74xx…) |
| 🔴 **Đường ngắn nhất** | `#f44336` đỏ | Kết quả pathfinding (nét đứt) |

---

## 🛠️ Công nghệ sử dụng

| Thành phần | Công nghệ |
|-----------|-----------|
| Backend API | Python 3.10+, Flask, Flask-CORS |
| Thuật toán đồ thị | Custom Dijkstra với Transfer Penalty (heapq) |
| Thu thập dữ liệu OSM | OSMnx, GeoPandas |
| Frontend Map | Leaflet.js (tile CARTO dark/light) |
| Giao diện | HTML + Vanilla CSS (Flex layout, Dark/Light mode) |
| Fonts | Google Fonts — Inter |
| Package manager | uv |

---

## 🧠 Thuật toán Pathfinding

Dự án sử dụng **Dijkstra mở rộng theo trạng thái `(node, line)`**:

- **State space**: mỗi nút có nhiều trạng thái, mỗi trạng thái ứng với một tuyến tàu đang đi
- **Transfer Penalty**: mỗi lần đổi tuyến cộng thêm **300m** vào chi phí
- **Kết quả**: nếu 2 đường có khoảng cách gần tương đương, ưu tiên đường **ít chuyển tuyến hơn**

```
cost(edge) = edge.length + (300m nếu đổi tuyến, 0 nếu giữ nguyên)
```

---

## 📡 API Endpoints

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| `GET` | `/api/network` | Lấy toàn bộ nodes + edges (kèm `line_type`) |
| `GET` | `/api/lines` | Lấy danh sách tuyến `{name, type}` + tuyến đang bị tắt |
| `POST` | `/api/find-path` | Tìm đường ngắn nhất (`start_node`, `end_node`) |
| `POST` | `/api/admin/toggle-line` | Bật/tắt tuyến tàu (`line`, `disabled`) |

---

## 👥 Môn học

**IT3160 - Introduction to AI** — Hanoi University of Science and Technology (HUST), 2025.2
