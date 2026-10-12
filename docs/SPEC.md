# Gcalls ContactHub Mobile · Đặc tả giao diện

Tài liệu bàn giao cho dev. Mỗi màn có 3 thứ đi kèm nhau:

- **Ảnh**: `docs/screens/<Tên>.png`
- **Mã nguồn mockup**: `prototype/screens/<Tên>.dc.html`. Đây là HTML/CSS chuẩn. Phần logic hiển thị nằm trong khối `<script data-dc-script>` cuối file.
- **Prototype bấm được**: `prototype/viewer.html?s=<Tên>`. Cách chạy xem ở `README.md`.

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

| # | File | Màn | Mở từ | Ghi chú dev |
|---|------|-----|-------|-------------|
| 1 | `Main` | Tổng quan | Tab 1 | Biểu đồ cột chồng gọi đi/đến. Chọn khoảng thời gian (Hôm nay/7/30/90 ngày, tuỳ chỉnh có lịch, nhóm theo giờ/ngày/tuần/tháng). 4 ô chỉ số bấm được. Danh sách "Cần chú ý". Khách gần đây. |
| 2 | `Contacts` | Danh bạ | Tab 2 | Tìm ngay trong danh sách. Lọc theo nguồn dữ liệu. Tab Khách hàng / Nhóm. Nhóm theo chữ cái A–Z. Nút Gọi luôn hiện sẵn. FAB Bàn phím. |
| 3 | `History` | Lịch sử | Tab 3 | Chip lọc Tất cả / Cuộc gọi / Gọi nhỡ / Tin nhắn. Nhóm theo ngày. Icon thể hiện đi / đến / nhỡ / SMS, có icon ghi âm. FAB Bàn phím. |
| 4 | `Tasks` | Công việc | Tab 4 | Vòng tiến độ + Quá hạn / Hôm nay / Chưa nhận. Phân đoạn Đang mở / Hôm nay / Đã xong. Thẻ việc có nút Nhận việc. FAB Nhắc hẹn. |
| 5 | `Account` | Tài khoản | Avatar | Trạng thái trực, máy nhánh, tổng đài, SSO, ngôn ngữ, chỉ rung, đăng xuất. |
| 6 | `StatusSheet` | Trạng thái trực | Pill trạng thái | 4 mức: Sẵn sàng / Tạm nghỉ / Không làm phiền / Hết ca. Công tắc "Chỉ rung" tách riêng. |
| 7 | `Search` | Tìm kiếm | Icon kính lúp | Khách gần đây + gọi nhanh. Tìm khi gõ từ 2 ký tự. |
| 8 | `Notifications` | Thông báo | Icon chuông | Tất cả / Chưa đọc. Chấm tím = chưa đọc. Chạm vào để mở đúng việc / cuộc gọi. |
| 9 | `ContactQuick` | Xem nhanh KH | "⋯" ở Danh bạ, Khách gần đây | 4 hành động: Gọi / Nhắn / Nhắc hẹn / Ghim. |
| 10 | `Customer` | Hồ sơ KH | Xem nhanh, Chi tiết cuộc gọi | Tab Thông tin / Tương tác / Nhắc nhở. Có cùng thanh 4 hành động như Xem nhanh. |
| 11 | `HistoryFilter` | Bộ lọc lịch sử | Nút lọc ở Lịch sử | Nút Áp dụng hiện luôn số kết quả. |
| 12 | `CallDetail` | Chi tiết cuộc gọi | Dòng trong Lịch sử | Trình phát ghi âm ngay trong sheet (phát, thanh tua, tốc độ). |
| 13 | `TaskFilter` | Bộ lọc công việc | Nút lọc ở Công việc | |
| 14 | `TaskTimeline` | Diễn biến công việc | Thẻ việc | |
| 15 | `CreateReminder` | Tạo nhắc hẹn | FAB, Hồ sơ, Kết thúc cuộc gọi | Chọn khách, nội dung, ghi chú, ngày giờ, ưu tiên, lặp lại. |
| 16 | `Dialer` | Bàn phím | FAB xanh | Gõ từ 2 số trở lên sẽ gợi ý khách trùng số trong danh bạ. Chọn đầu số gọi ra. Nút xoá, nhắn tin, gọi. |
| 17 | `InCall` | Đang gọi | Gọi đi / Nghe máy | Đồng hồ, chỉ báo ghi âm, việc đang mở của khách. Tắt mic, loa ngoài, giữ máy, chuyển tiếp, thêm người, ghi chú. Bàn phím DTMF. Nút ⌄ thu nhỏ cuộc gọi. |
| 18 | `Incoming` | Cuộc gọi đến | Push VoIP | Tra khách theo số ngay khi đổ chuông. Hiện lần tương tác trước, việc đang mở, nguồn dữ liệu. Có nút "Nhắn đang bận" và "Nhắc gọi lại". |
| 19 | `AfterCall` | Kết thúc cuộc gọi | Sau khi gác máy | Ghi kết quả, ghi chú, hoàn thành việc liên quan, hẹn gọi lại nhanh. Chọn kết quả "Hẹn gọi lại" thì tự bật nhắc hẹn. |
| 20 | `SendSms` | Nhắn SMS | Nút Nhắn tin ở mọi nơi | Chọn mẫu tin, đếm ký tự và số tin (160 / 153 ký tự mỗi tin). |
| 21 | `Login` | Đăng nhập | Mở app lần đầu | Nhập mã tổng đài (app nhớ cho lần sau), rồi đăng nhập Keycloak SSO. |
| 22 | `Permissions` | Cấp quyền | Sau đăng nhập | Micro và Thông báo là bắt buộc; nút "Bắt đầu" bị khoá đến khi bật đủ. Chạy nền: khuyến nghị. Danh bạ máy: tuỳ chọn. |
| 23 | `HistoryLoading` | Đang tải | Mọi danh sách | Khung xương (skeleton) giữ đúng bố cục danh sách. Không để trang trắng. |
| 24 | `SearchEmpty` | Không có kết quả | Tìm kiếm | Nếu chuỗi tìm là số điện thoại thì cho Gọi / Nhắn ngay. |
| 25 | `Offline` | Mất kết nối | Mất SIP/mạng | Trạng thái chuyển "Ngoại tuyến" (chấm xám). Băng cảnh báo có đếm ngược và nút Thử lại. Nút Gọi bị khoá nhưng vẫn xem được dữ liệu đã lưu. |
| — | `*D`, `*L` | Bản tối / sáng | — | Hai phương án giao diện thử nghiệm cho 5 màn chính, chưa chốt. |

## 4. Design tokens

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

Bản tối (`.app.dk`): `--ink #F4F2F8`, `--surf #1A1620`, `--surf-2 #25212C`, nền `#0D0A11`, accent `#B9B0FF`.

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
- Bản tối / sáng (`*D`, `*L`): chốt một bản hay hỗ trợ cả hai theo cài đặt hệ thống?

## 10. Trợ năng

- Chữ đạt tương phản 4.5:1. Chữ nhỏ nhất 12.5px.
- Mọi nút chỉ có icon đều có `aria-label` (trên mobile là `accessibilityLabel`).
- Công tắc và lựa chọn khai báo vai trò và trạng thái (`switch` / `radio`, checked).
- Không phân biệt trạng thái chỉ bằng màu: gọi nhỡ luôn có chữ "Gọi nhỡ", trạng thái trực luôn có nhãn.
