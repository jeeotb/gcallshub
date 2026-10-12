# Gcalls ContactHub Mobile · Đặc tả giao diện

Tài liệu bàn giao cho dev. Mỗi màn có 3 thứ đi kèm nhau:

- **Ảnh**: `docs/screens/<Tên>.png`
- **Mã nguồn mockup**: `prototype/screens/<Tên>.dc.html`. Đây là HTML/CSS chuẩn. Phần logic hiển thị nằm trong khối `<script data-dc-script>` cuối file.
- **Prototype bấm được**: `prototype/viewer.html?s=<Tên>`. Cách chạy xem ở `README.md`.

> **Phạm vi hiện tại:** bộ mockup gồm **5 màn chính ở giao diện sáng tím – trắng** (`*L`, bản chính), kèm bản tối (`*D`). Các màn khác nhắc tới trong tài liệu này (luồng gọi, sheet, đăng nhập, trạng thái hệ thống) đã được bỏ khỏi repo. Bản thiết kế sáng của chúng vẫn còn trên canvas và chưa có bản tối; phần mô tả được giữ lại để làm định hướng.

Mockup chỉ dùng **dữ liệu giả**. Ô ghi trong `[NGOẶC VUÔNG]` là thông tin bên Gcalls cần xác nhận (xem mục 9).

---

## 1. Phạm vi

App mobile (iOS + Android) cho **tổng đài viên** dùng Gcalls:

- nhận và gọi cuộc gọi qua máy nhánh,
- tra cứu khách hàng (danh bạ đồng bộ từ Gcalls / Gcalls Cloud và các nguồn CRM),
- xem lịch sử tương tác, nghe lại ghi âm,
- nhận và xử lý công việc, nhắc hẹn gọi lại,
- đổi trạng thái trực.

Kích thước thiết kế: **390 × 844 pt** (iPhone 14/15). Các màn chỉ có một cột, co giãn theo chiều ngang.

## 2. Điều hướng

```
Đăng nhập ─► Cấp quyền ─► Tổng quan
                              │
   ┌──────────── Thanh tab (4) ─────────────┐
   Tổng quan     Danh bạ      Lịch sử     Công việc
                    │             │            │
           Xem nhanh KH     Chi tiết gọi   Diễn biến việc
                    │             │            │
              Hồ sơ KH ◄──────────┘       Tạo nhắc hẹn
                    │
               Nhắn SMS

Thanh trên cùng (có ở mọi tab):
  [logo] [Trạng thái trực ▾] ...... [Tìm kiếm] [Thông báo] [Avatar → Tài khoản]

Luồng gọi:
  Bàn phím (FAB xanh ở Danh bạ / Lịch sử) ─► Đang gọi ─► Kết thúc cuộc gọi ─► Lịch sử
  Cuộc gọi đến (push VoIP) ─► Nghe máy ─► Đang gọi ─► …
  Nút Gọi ở Danh bạ / Tìm kiếm / Hồ sơ / Chi tiết cuộc gọi ─► Đang gọi
```

- **Sheet** (trượt từ dưới lên, nền mờ phía sau): Trạng thái trực, Xem nhanh KH, Chi tiết cuộc gọi, Bộ lọc lịch sử, Bộ lọc công việc, Tạo nhắc hẹn, Nhắn SMS. Đóng được bằng nút ✕, chạm nền hoặc vuốt xuống.
- **Màn đẩy** (có nút ← quay lại): Tìm kiếm, Thông báo, Hồ sơ KH, Diễn biến việc, Bàn phím, Kết thúc cuộc gọi.
- **Toàn màn**: Đang gọi, Cuộc gọi đến (nền tím đậm, không có thanh tab).

## 3. Danh sách màn hình

| File (tối / sáng) | Màn | Mở từ | Ghi chú dev |
|---|---|---|---|
| `MainD` / `MainL` | Tổng quan | Tab 1 | Thứ tự (bản tối): lời chào → 4 thẻ Việc cần làm → Hiệu suất cuộc gọi → Cần chú ý → Gần đây. Biểu đồ cột chồng gọi đi/đến. Chọn khoảng thời gian (Hôm nay/7/30/90 ngày, tuỳ chỉnh có lịch, nhóm theo giờ/ngày/tuần/tháng). 4 ô chỉ số bấm được. Danh sách "Cần chú ý". Khách gần đây. |
| `ContactsD` / `ContactsL` | Danh bạ | Tab 2 | Tìm ngay trong danh sách. Lọc theo nguồn dữ liệu. Tab Khách hàng / Nhóm. Nhóm theo chữ cái A–Z. Nút Gọi luôn hiện sẵn. |
| `HistoryD` / `HistoryL` | Lịch sử | Tab 3 | Chip lọc Tất cả / Cuộc gọi / Gọi nhỡ / Tin nhắn. Nhóm theo ngày. Icon thể hiện đi / đến / nhỡ / SMS, có icon ghi âm. |
| `TasksD` / `TasksL` | Công việc | Tab 4 | Vòng tiến độ + Quá hạn / Hôm nay / Chưa nhận. Phân đoạn Đang mở / Hôm nay / Đã xong. Thẻ việc có nút Nhận việc. FAB Nhắc hẹn. |
| `AccountD` / `AccountL` | Tài khoản | Avatar | Trạng thái trực, máy nhánh, tổng đài, SSO, ngôn ngữ, chỉ rung, đăng xuất. |

Trong prototype, các nút dẫn tới màn đã bỏ (tìm kiếm, thông báo, sheet, chi tiết…) không chuyển màn.

## 4. Design tokens

**Giao diện sáng (bản chính)** — class `.app.lt`, tham khảo phong cách "Elle":

| Token | Giá trị | Dùng cho |
|---|---|---|
| Tím chính | `#7B61FF`; nút: gradient `#8D78FF → #6F55F5` | Nút chính, chip đang chọn, avatar người dùng, tab đang chọn, link |
| Tím đậm | `#5B43E0` | Chữ trên nền tím nhạt |
| Tím nhạt | `#F3F0FF`; viền nhấn `#D9D1FF` | Ô icon, avatar khách, tag |
| Nền | trắng `#FFFFFF`, đầu trang có quầng tím `#C4B5FF` và bạc hà `#C6F2E2` rất nhạt | |
| Card | trắng, viền 1px `#ECEAF4`, bo 20, bóng rất nhẹ | |
| Ô icon pastel | tím `#F3F0FF` · hồng `#FFE9EE` (gọi nhỡ) · bạc hà `#E5F7EF` (gọi đến, hôm nay, sẵn sàng) · cam nhạt `#FFF0E3` (SMS, quá hạn) · xanh nhạt `#E8F1FF` | Icon bên trong màu tím |
| Chữ | `#14121F` / `#4A475C` / `#7B7891` | |
| Thanh tab | nền trắng chuyển tím nhạt `#FFFFFF → #F4F0FF → #E7DFFF`, ô tròn trắng + nhãn; tab đang chọn icon và nhãn tím. Cùng lề 20px và bo 20px với card; đáy màn có lớp mờ trắng để nội dung trôi dưới thanh tab không lộ mép | Nút logo Gcalls tròn ở cuối thanh: bấm để thu gọn thành nút tròn góc phải dưới (chấm đỏ khi có việc mới), bấm lại để mở. Trạng thái thu gọn được nhớ giữa các tab |
| 4 thẻ chỉ số (Việc cần làm) | Nền pastel: hồng `#FAD3EE` (gọi nhỡ), tím `#D9D3FF` (chưa nhận), vàng `#FFE8A3` (quá hạn), bạc hà `#C8F2EA` (hôm nay). Không có icon nhỏ (chỉ dùng icon kính 3D); số 32px/700 và nhãn 13px/600 ở dưới, cùng lề trái 18px. Trang trí: 4 icon kính 3D riêng, tô theo màu thẻ (`assets/deco/`: `missed-pink` ống nghe + X, `unassigned-violet` người + dấu cộng, `overdue-yellow` đồng hồ báo thức + !, `today-mint` lịch + ✓; PNG nền trong suốt 420px), cùng tông màu với thẻ, đặt ở góc trên phải, xoay -6° | Dùng chung cho bản sáng và tối |
| Nền động (liquid) | 4 khối tím nhạt (bản tối: tím trầm, mờ 55%), đường kính 240–400px, trôi và co giãn chậm (chu kỳ 19 / 23 / 25 / 29s, so le). Bộ lọc gooey (Gaussian blur 22 + ngưỡng alpha) để các khối chạm nhau thì dính lại như giọt nước, sau đó blur thêm 28px (tối: 36px), giảm độ bão hòa còn 60%, độ đậm 75% (tối: 40%) cho dịu mắt | Tắt chuyển động khi máy bật "Giảm chuyển động". Trên native: dùng shader / Lottie hoặc ảnh động pre-render để nhẹ máy |
| Chip, phân đoạn | chip trắng viền mảnh, chip chọn tím đặc; phân đoạn nền `#F4F3F8`, mục chọn trắng chữ tím | |

Bảng dưới đây là màu gốc của bộ thiết kế ban đầu:

Lấy từ `prototype/assets/contacthub.css` (khối `:root`).

**Màu**

| Token | Giá trị | Dùng cho |
|---|---|---|
| `--brand` | `#673AB7` | Màu thương hiệu |
| `--accent` | `#7C5CE0` | Nút chính, tab đang chọn, viền focus |
| `--accent-d` | `#5B3FC4` | Chữ / icon nhấn trên nền sáng |
| `--ink` | `#1F1A33` | Chữ chính |
| `--ink-2` | `#4A4463` | Chữ phụ |
| `--ink-3` | `#757090` | Chữ mô tả (tối thiểu 12.5px) |
| `--ok` | `#1F9D5B` | Đã kết nối, gọi đến |
| `--warn` | `#B7791F` | Chưa nhận, cảnh báo |
| `--bad` | `#E5486B` | Gọi nhỡ, kết thúc cuộc gọi, badge |
| Nút Gọi | `#45D28A → #27AE66` | **Luôn xanh lá**, không dùng màu khác cho hành động gọi |
| Nền app | `#EEEAF9` | Cùng các mảng mờ tím chuyển động phía sau |
| Nền màn gọi | `#3B2380 → #1A1036` | Đang gọi, Cuộc gọi đến |

**Giao diện tối** = bản sáng + class `.night` trên `.app` (file `*D` sinh từ `*L`, chỉ khác link và class). Chỉ đổi: nền `#14121F → #0E0D16` (quầng tím / bạc hà mờ ở đầu trang, khối liquid tối đi 58%), card `#1A1826` viền `rgba(255,255,255,.08)`, chữ `#F2F0FA` / `#C9C6DA` / `#9A96B2`. Giữ nguyên như bản sáng: tab, nút, chip, phân đoạn, thanh tab, 4 thẻ chỉ số, icon, chữ trên giao diện. Phần nền sáng (nút, chip, thanh tab, thẻ chỉ số) giữ chữ tối.

**Chữ**: Be Vietnam Pro 400 / 500 / 600 / 700.

| Cấp | Cỡ / dòng | Đậm |
|---|---|---|
| Tiêu đề trang (`.h1`) | 30 / 1.2 | 700 |
| Tiêu đề sheet | 21 | 700 |
| Tiêu đề mục (`.h2`) | 17 | 600 |
| Nội dung | 15 / 1.6 | 400–600 |
| Mô tả (`.meta`) | 13 | 400 |
| Nhỏ nhất | 12.5 | — |

Số điện thoại và thời lượng dùng `font-variant-numeric: tabular-nums`.

**Bo góc**: thẻ 16–28 · sheet 20–34 · nút 10 (chữ) / tròn (icon) · chip 8 · input 10–16.
**Khoảng cách**: lề trang 20 · giữa các khối 24–30 · trong thẻ 14–20.
**Vùng chạm** tối thiểu 44 × 44.

## 5. Thành phần dùng chung

| Thành phần | Class trong mockup | Ghi chú |
|---|---|---|
| Thanh trên cùng | `.top` | Logo, pill trạng thái (chấm màu + máy nhánh), tìm kiếm, chuông (chấm đỏ khi có mới), avatar |
| Thanh tab | `.nav` | 4 tab có nhãn. Badge đỏ: số gọi nhỡ, việc chưa nhận (từ 99 trở lên hiện "99+") |
| Thẻ | `.card` | Nền trắng mờ, bo 16–28 |
| Dòng danh sách | `.row` | Avatar / icon sự kiện, tên, dòng phụ, thời gian hoặc nút |
| Avatar chữ | `.av` | Lấy 2 chữ cái đầu |
| Icon sự kiện | `.ev.out/.in/.miss/.sms` | Gọi đi / đến / nhỡ / SMS |
| Nút | `.btn.primary/.secondary/.ghost/.call` | `.sm` = cao 36 |
| Nút gọi tròn | `.call-btn` | Xanh lá |
| Chip lọc | `.chip`, `.chip.on` | |
| Phân đoạn | `.seg` | 2–4 lựa chọn |
| Tag | `.tag.ok/.warn/.bad/.brand` | |
| Sheet | `.sheet` + `.scrim` + `.grab` | |
| Thanh 4 hành động | `.actions4` | Gọi / Nhắn / Nhắc hẹn / Ghim. Giống nhau ở Xem nhanh và Hồ sơ |
| Công tắc | `.toggle` | Cần có `role="switch"` và `aria-checked` |
| Trạng thái rỗng | `.empty` | Icon, tiêu đề, mô tả, CTA |
| FAB | `.fab` | Tím = tạo mới; xanh = bàn phím |

Icon nằm trong `prototype/assets/icons/`, đã đặt tên theo nghĩa (`phone.svg`, `call-missed.svg`, …). Hình nền và biến thể theme nằm trong `assets/theme/`.

## 6. Quy tắc hành vi

1. **Trạng thái trực chỉ có một nguồn dữ liệu.** Đổi ở bất kỳ đâu (pill trên cùng, Tài khoản) thì đồng bộ với tổng đài và hiển thị giống nhau ở mọi nơi. Có 4 mức. Thêm "Ngoại tuyến" khi mất kết nối; mức này do hệ thống đặt, người dùng không tự chọn.
2. **Màu hành động**: Gọi luôn xanh lá. Kết thúc / từ chối dùng đỏ `#E5486B`. Mọi hành động khác dùng tím.
3. **Badge**: Lịch sử = số gọi nhỡ chưa xem. Công việc = số việc chưa nhận.
4. **Đang tải**: hiện skeleton ngay. Không để danh sách trắng khi đã biết có dữ liệu.
5. **Bộ lọc**: nút Áp dụng ghi số kết quả. Bộ lọc đang bật hiện thành chip có ✕ phía trên danh sách.
6. **Sau khi đóng sheet**, lần chạm kế tiếp phải ăn ngay (bản cũ bị lỗi phải chạm 2 lần).
7. **Cuộc gọi đến khi app ở nền hoặc máy khoá**: dùng CallKit (iOS) / ConnectionService (Android) để hiện màn nghe máy hệ thống, rồi mở màn `InCall` của app.
8. **Kết thúc cuộc gọi** luôn mở `AfterCall`. Người dùng có thể Bỏ qua; khi đó cuộc gọi lưu với kết quả trống.
9. **Ngoại tuyến**: vẫn xem được danh bạ, lịch sử đã lưu và tạo nhắc hẹn. Thay đổi được xếp hàng và đồng bộ khi có mạng lại.
10. **Việc trùng** (cùng khách, cùng loại, chưa xong) phải gộp lại, không hiện lặp.

## 7. Dữ liệu (gợi ý mô hình)

```ts
type Presence = 'available' | 'break' | 'dnd' | 'off_shift' | 'offline';

interface Agent { id: string; username: string; email: string; extension: string; tenant: string; presence: Presence; vibrateOnly: boolean; }

interface Contact {
  id: string; name: string; phones: string[]; email?: string; address?: string;
  birthday?: string; gender?: 'male' | 'female' | 'other';
  source: string;            // 'Gcalls' | 'Gcalls Cloud' | CRM …
  pinned: boolean; groupIds: string[]; note?: string;
}

interface Interaction {
  id: string; contactId?: string; phone: string;
  kind: 'call_out' | 'call_in' | 'call_missed' | 'sms_out' | 'sms_in' | 'note';
  at: string; durationSec?: number; agentId: string;
  status?: 'connected' | 'no_answer' | 'busy' | 'failed';
  result?: 'success' | 'callback' | 'no_answer' | 'busy' | 'wrong_number';
  note?: string; recordingUrl?: string;
}

interface Task {
  id: string; title: string; contactId: string;
  type: 'callback' | 'reminder' | 'other';
  dueAt?: string; priority: 'low' | 'normal' | 'high' | 'urgent';
  repeat: 'none' | 'daily' | 'weekly' | 'monthly';
  assigneeId?: string; status: 'unassigned' | 'accepted' | 'done';
  timeline: { at: string; by: string; text: string }[];
}

interface Notification { id: string; kind: 'reminder' | 'new_task' | 'missed_call'; title: string; body: string; at: string; read: boolean; target: { type: 'task' | 'interaction'; id: string }; }

interface SmsTemplate { id: string; name: string; body: string; }
```

Số liệu ở màn Tổng quan: tổng cuộc gọi, gọi đi / đến, tỉ lệ bắt máy (đi / đến), thời lượng trung bình, gom theo giờ / ngày / tuần / tháng trong khoảng ngày đã chọn.

## 8. Tích hợp cần có

| Nhu cầu | Gợi ý |
|---|---|
| Đăng nhập | Keycloak OIDC (PKCE). Mã tổng đài → realm / URL của tenant |
| Gọi điện | SIP qua WebRTC hoặc SDK softphone của Gcalls; đăng ký máy nhánh |
| Nhận cuộc gọi ở nền | Push VoIP (APNs PushKit / FCM high-priority) + CallKit / ConnectionService |
| Ghi âm | URL phát có hạn (signed URL), phát dạng stream |
| Danh bạ | API phân trang + tìm kiếm phía server (9.673+ bản ghi), lọc theo nguồn |
| Lịch sử, việc, thông báo | API phân trang + realtime (WebSocket / SSE) cho badge |
| SMS | API gửi SMS theo brandname / đầu số, kèm mẫu tin |
| Ngoại tuyến | Lưu cục bộ (SQLite) danh bạ gần đây, lịch sử và hàng đợi thay đổi |

## 9. Câu hỏi mở cho Gcalls

- `[ĐẦU SỐ HIỂN THỊ]`: những đầu số nào tổng đài viên được chọn khi gọi ra? Mặc định là số nào?
- `[BRANDNAME / ĐẦU SỐ SMS]`: brandname nào được dùng? Mẫu tin có phải duyệt trước không?
- Danh sách "Kết quả cuộc gọi" có cấu hình theo từng tenant không?
- Chuyển tiếp / thêm người: chuyển tới máy nhánh, hàng đợi hay số ngoài?
- Có cần ghi âm theo đồng ý của khách (thông báo đầu cuộc gọi) không?
- Đã chọn giao diện tối. Có cần thêm bản sáng theo cài đặt hệ thống không?

## 10. Trợ năng

- Chữ đạt tương phản 4.5:1. Chữ nhỏ nhất 12.5px.
- Mọi nút chỉ có icon đều có `aria-label` (trên mobile là `accessibilityLabel`).
- Công tắc và lựa chọn khai báo vai trò và trạng thái (`switch` / `radio`, checked).
- Không phân biệt trạng thái chỉ bằng màu: gọi nhỡ luôn có chữ "Gọi nhỡ", trạng thái trực luôn có nhãn.
