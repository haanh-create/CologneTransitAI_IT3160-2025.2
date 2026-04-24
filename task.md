# 📋 Task Log — CologneTransitAI

> Tóm tắt toàn bộ thay đổi so với commit đầu tiên (`de59c7c first commit`)  
> Cập nhật: 2026-04-24

---

## ✅ Môi trường (Tooling)

- [x] Cài đặt **`uv`** (package manager Rust-based) vào `~/.local/bin`
- [x] Tạo virtual environment bằng `uv venv .venv`
- [x] Cài toàn bộ dependencies bằng `uv pip install -r requirements.txt`
- [x] Thêm file **`pyproject.toml`** để khai báo project theo chuẩn PEP 517

---

## ✅ Dọn dẹp

- [x] Xóa `backend/__pycache__/` (cache Python tạm)
- [x] Xóa `frontend/.gitkeep` (placeholder không cần thiết)
- [x] Xóa `task.md` cũ (nội dung từ session trước không còn phù hợp)

---

## ✅ Backend — `engine.py`

### Phân loại tuyến (`classify_line`)
- Thêm hàm `classify_line(line_name)` phân loại tuyến thành 3 nhóm:
  - **`rail`**: tuyến có tên chữ (Innenstadttunnel, SB-Nord, Nord-Süd-Stadtbahn…)
  - **`sub`**: tuyến số 1–99 (KVB Stadtbahn / Stadtbahn)
  - **`train`**: tuyến số 4 chữ số (26xx, 74xx, 92xx — Regional)

### API `get_all_lines()` — thêm `type`
- Trả về list `[{name, type}, ...]` thay vì chỉ list tên
- Sắp xếp theo `(type, name)` để nhóm rail/sub/train ở đầu

### API `get_network_data()` — thêm `line_type`
- Mỗi edge trong response giờ có thêm trường `line_type` (`rail`/`sub`/`train`)
- Frontend dùng để tô màu đường theo loại

### Thuật toán `find_path()` — Dijkstra có Transfer Penalty
- Thay thế `nx.shortest_path()` bằng **Custom Dijkstra** tự cài với `heapq`
- State space mở rộng: `(node_id, current_line)` thay vì chỉ `node_id`
- **Transfer Penalty = 300m**: cộng thêm 300m vào chi phí mỗi lần đổi tuyến
- Kết quả: nếu 2 đường có độ dài tương đương, ưu tiên đường **ít chuyển tuyến hơn**
- Thêm `import heapq` vào đầu file

---

## ✅ Frontend — `index.html`

### Layout: Sidebar + Map cạnh nhau
- **Cũ**: Panel `position: absolute` nổi che bản đồ
- **Mới**: `body { display: flex }` — panel 320px bên trái, bản đồ `flex: 1` bên phải
- Panel có `border-right` thay vì `box-shadow` tròn

### Dark/Light Mode
- Thêm nút toggle ☀️/🌙 góc phải panel header
- Lưu theme vào `localStorage`, áp dụng khi tải lại trang
- Bản đồ tự đổi tile (CARTO dark ↔ CARTO light) theo theme

### Chú giải màu (Legend)
- 4 dòng: Rail 🔵 / Sub 🟢 / Train 🟡 / Đường ngắn nhất 🔴 (nét đứt)

### Admin Panel — chia 3 nhóm có scroll
- 3 group header: 🛤 Rail (7) / 🚇 Sub (34) / 🚆 Train (60)
- Mỗi nhóm có nút ▼/▶ thu gọn/mở rộng
- Mỗi nhóm có scroll riêng (`max-height: 180px`, `overflow-y: auto`)
- Chấm màu ứng theo loại tuyến (xanh lam / xanh lá / vàng)

### CSS mới thêm
- `.line-group-header`, `.line-group-items`, `.btn-group-toggle`
- `.route-steps-container`, `.route-step`, `.step-header`, `.step-route`, `.step-station`, `.step-dot`, `.step-midline`

---

## ✅ Frontend — `cologne_map.js`

### Màu tuyến theo `line_type`
```js
const LINE_COLORS = {
    rail:  '#0085c8',   // xanh lam (Rail)
    sub:   '#00c666',   // xanh lá  (Sub)
    train: '#ffd600',   // vàng     (Train)
};
const PATH_COLOR = '#f44336'; // đỏ — đường ngắn nhất
```

### Sửa bug `classifyLine` (JS)
- **Bug**: `parseInt("Innenstadttunnel")` → `NaN`, JS không throw → rơi vào `return 'train'`
- **Fix**: Thêm `if (isNaN(n)) return 'rail'` trước khi kiểm tra range

### Tile sáng/tối
- Khởi tạo cả `_darkTile` và `_lightTile`
- Hàm `applyTheme()` swap tile khi người dùng chuyển chế độ

### Lộ trình chi tiết (`renderItinerary`)
- Gom các edge liên tiếp cùng tuyến thành 1 **segment**
- Mỗi segment = 1 card với header màu đặc (Rail/Sub/Train) + tên ga đầu/cuối + km
- Tuyến Train (#ffd600 vàng) dùng chữ tối `#1a1a1a` để đọc được
- Không hiển thị block "Chuyển tàu" màu đỏ (xóa do thừa)
- Không hiển thị "X đoạn cạnh" (thuật ngữ đồ thị không có nghĩa với người dùng)

### Admin: loadLineControls phân nhóm
- Đọc `line.type` từ API mới
- Render 3 section Rail / Sub / Train với header riêng
- Hàm `toggleGroup(type, btn)` collapse/expand từng nhóm

---

## 📊 Thống kê thay đổi (git diff HEAD)

| File | Thay đổi |
|------|----------|
| `backend/engine.py` | +178 / −84 dòng |
| `frontend/index.html` | +637 / −273 dòng |
| `frontend/js/cologne_map.js` | +322 / −121 dòng |
| `pyproject.toml` | Mới (thêm vào) |
| `frontend/.gitkeep` | Xóa |
| `task.md` (cũ) | Xóa, thay bằng file này |

---

## 🚀 Cách chạy (sau khi cập nhật)

```powershell
# Kích hoạt môi trường ảo
.venv\Scripts\activate

# Chạy backend (Flask tự serve frontend)
python backend/app.py
```

Truy cập: http://localhost:5000
