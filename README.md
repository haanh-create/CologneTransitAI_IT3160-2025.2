# 🚇 Cologne Transit AI

> Hệ thống tìm đường đi ngắn nhất cho mạng lưới giao thông công cộng tại **Cologne (Köln), Đức**.  
> Dự án sử dụng dữ liệu thực từ OpenStreetMap, thuật toán đồ thị Dijkstra, và giao diện bản đồ tương tác.

---

## 📌 Mô tả dự án

Cologne Transit AI là một ứng dụng web full-stack cho phép:

- **Người dùng (User):** Chọn 2 trạm bất kỳ trên bản đồ → Hệ thống tự động tìm và hiển thị **đường đi ngắn nhất** giữa hai trạm đó.
- **Quản trị viên (Admin):** Bật/tắt từng tuyến tàu (Subway, Tram, S-Bahn) để **mô phỏng sự cố hoặc bảo trì**, hệ thống sẽ tự tính lại đường đi tránh tuyến bị vô hiệu hóa.

Dữ liệu mạng lưới giao thông (3.634 trạm, 4.744 tuyến đường) được thu thập trực tiếp từ **OpenStreetMap** thông qua thư viện `osmnx`.

---

## 🏗️ Cấu trúc dự án

```
CologneTransitAI/
├── backend/
│   ├── app.py          # Flask API server, đồng thời serve frontend
│   └── engine.py       # TransitEngine: load đồ thị, Dijkstra, toggle tuyến
│
├── frontend/
│   ├── index.html      # Giao diện chính: bản đồ + side panel
│   └── js/
│       ├── api.js          # Hàm gọi API backend (fetch wrapper)
│       └── cologne_map.js  # Leaflet.js: render bản đồ, markers, path
│
├── data/
│   └── cologne_network.json    # Dữ liệu đồ thị OSM (nodes + edges)
│
├── scripts/
│   └── fetch_data.py   # Script thu thập dữ liệu từ OpenStreetMap
│
├── requirements.txt    # Danh sách thư viện Python cần thiết
└── README.md
```

---

## 🚀 Cách chạy dự án

### Yêu cầu
- Python 3.9+
- pip

### Bước 1 — Cài đặt thư viện

```bash
pip install -r requirements.txt
```

> Các thư viện chính: `flask`, `flask-cors`, `networkx`, `osmnx`

### Bước 2 — Chạy server

```bash
python backend/app.py
```

Server sẽ khởi động tại: **http://localhost:5000**

> Flask tự động serve cả frontend, **không cần** mở file HTML riêng hay cài thêm Live Server.

### Bước 3 — Mở trình duyệt

Truy cập: [http://localhost:5000](http://localhost:5000)

---

## 🎮 Hướng dẫn sử dụng

| Thao tác | Kết quả |
|----------|---------|
| Click vào 1 trạm trên bản đồ | Chọn **điểm đi** (marker xanh lá) |
| Click vào trạm thứ 2 | Chọn **điểm đến** (marker đỏ) → tự động tìm đường |
| Đường vàng dashed xuất hiện | Đường đi ngắn nhất đã được tìm thấy |
| Gạt công tắc trong Admin panel | Vô hiệu hóa / kích hoạt tuyến tàu |
| Nhấn "Xóa chọn điểm" | Reset lại lựa chọn |

---

## 🛠️ Công nghệ sử dụng

| Thành phần | Công nghệ |
|-----------|-----------|
| Backend API | Python, Flask, Flask-CORS |
| Thuật toán đồ thị | NetworkX (Dijkstra shortest path) |
| Thu thập dữ liệu OSM | OSMnx |
| Frontend Map | Leaflet.js (dark tile từ CARTO) |
| Giao diện | HTML + Vanilla CSS (Glassmorphism, dark mode) |
| Fonts | Google Fonts — Inter |

---

## 📡 API Endpoints

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| `GET` | `/api/network` | Lấy toàn bộ nodes + edges |
| `GET` | `/api/lines` | Lấy danh sách tuyến + tuyến đang bị tắt |
| `POST` | `/api/find-path` | Tìm đường ngắn nhất (`start_node`, `end_node`) |
| `POST` | `/api/admin/toggle-line` | Bật/tắt tuyến tàu (`line`, `disabled`) |

---

## 👥 Môn học

**IT3160 - Introduction to AI** — Hanoi University of Science and Technology (HUST), 2025.2
