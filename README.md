# Pop Assistant - Trợ Lý Ảo Giọng Nói & Giám Sát Hệ Thống Thông Minh

Pop Assistant là một ứng dụng Trợ lý ảo toàn diện dành cho Windows, được phát triển bằng ngôn ngữ **Python** và thiết kế giao diện đồ họa **PyQt6** hiện đại. Ứng dụng tích hợp công nghệ nhận diện giọng nói, giám sát tài nguyên phần cứng thời gian thực, phân tích hành vi người dùng bằng thuật toán tự học và cung cấp một hệ thống quản trị (Admin Panel) chuyên sâu được bảo mật và ẩn kín.

---
##  Các Tính Năng Nổi Bật

### 1. Trợ Lý Ảo Đa Năng & Hội Thoại Giọng Nói
- **Nhận diện giọng nói (Speech-to-Text):** Tích hợp thư viện `speech_recognition` để nghe và chuyển dịch lệnh nói tiếng Việt/Anh một cách chuẩn xác.
- **Phản hồi bằng giọng nói (Text-to-Speech):** Chuyển đổi văn bản thành giọng nói tự nhiên thông qua Google TTS (`gtts`) kết hợp với `AudioService` để phát âm thanh mượt mà.
- **Giao tiếp thông minh (Chatbot):** Tự động phân tích ý đồ (Intent parsing), quản lý luồng hội thoại và lưu trữ toàn bộ lịch sử trò chuyện.

### 2. Giám Sát Phần Cứng Chuyên Sâu (System Monitoring)
- **Tài nguyên cơ bản:** Theo dõi phần trăm sử dụng CPU, RAM, Disk (Ổ đĩa) và trạng thái năng lượng Pin (Battery) thời gian thực.
- **Đo lường nhiệt độ (Temperature Monitor):**
  - Đọc trực tiếp nhiệt độ GPU NVIDIA thông qua thư viện phần cứng NVML (`pynvml`).
  - Hỗ trợ đọc nhiệt độ vi xử lý (CPU) và các cảm biến phần cứng sâu qua giao tiếp WMI với **OpenHardwareMonitor** (OHM) hoặc **LibreHardwareMonitor** (LHM).
- **Cảnh báo tương tác thông minh (Proactive Alerts):**
  - Tự động phát hiện khi CPU quá tải (>85%), RAM cạn kiệt, Pin yếu (<20%) hoặc nhiệt độ linh kiện vượt ngưỡng an toàn.
  - Hiển thị hộp thoại cảnh báo tương tác cho phép người dùng ra quyết định nhanh (ví dụ: tắt bớt tiến trình, bật chế độ tiết kiệm pin).
  - Tự động lưu trữ snapshot sức khỏe hệ thống (`health_snapshots`) vào cơ sở dữ liệu để vẽ biểu đồ lịch sử.
- **Tìm kiếm, khởi động ứng dụng và mở Web:**
  - *Ứng dụng máy tính:* Tìm kiếm và khởi động phần mềm trong PC (Ví dụ: *"mở NOTEPAD"*, *"tìm NOTEPAD"*, *"khởi động NOTEPAD"*, *"chạy NOTEPAD"*).
  - *Trình duyệt Web:* Truy cập nhanh các nền tảng phổ biến (Ví dụ: *"mở GOOGLE"*, *"tìm YOUTUBE"*, *"khởi động FACEBOOK"*, *"chạy WEB"*).

### 3. Tự Học & Gợi Ý Thói Quen Sử Dụng (Habit Tracker)
- **Theo dõi tự động:** Ghi nhận sự kiện khởi chạy và sử dụng các ứng dụng trên Windows (`app_usage`).
- **Thuật toán gợi ý thông minh:**
  - Áp dụng mô hình chấm điểm tăng/giảm (+1/-1) dựa trên các ngày trong tuần trong chu kỳ 7 ngày (Điểm tối đa là `3`).
  - Sắp xếp thứ tự ưu tiên dựa trên tần suất (Frequency) và độ mới nhất (Recency - thời gian mở gần đây nhất).
  - Đưa ra danh sách gợi ý ứng dụng phù hợp nhất cho người dùng vào từng khung giờ/ngày cụ thể.

### 4. Bảng Điều Khiển Admin Ẩn (Hidden Admin Panel - Sử dụng Konami Code)
Một trong những tính năng thú vị và mạnh mẽ nhất của hệ thống là bảng quản trị dành riêng cho quản trị viên, được giấu kín tại màn hình đăng nhập:
- **Cách kích hoạt:** Tại màn hình đăng nhập, **nhấn phím `Alt` 3 lần liên tiếp** trong vòng 2 giây để kích hoạt màn hình đăng nhập Admin ẩn (`AdminLoginView`).
- **Các Tab chức năng trong Admin Panel (`AdminPanelView`):**
  - **Quản lý người dùng (Users Tab):** Xem danh sách người dùng, thêm mới, cập nhật thông tin cá nhân hoặc chặn/xóa tài khoản.
  - **Xem lịch sử hội thoại (Conversations Tab):** Truy xuất toàn bộ lịch sử chat của hệ thống, xem chi tiết nội dung tương tác giữa bot và người dùng.
  - **Dashboard sức khỏe (Health Tab):** Trực quan hóa tài nguyên CPU, RAM, Disk, Nhiệt độ bằng biểu đồ đường (Line Chart) thời gian thực cực kỳ sinh động.
  - **Quản lý CSDL (Database Tab):** Công cụ quản lý SQLite trực quan cho phép sao lưu (Backup), phục hồi (Restore), tối ưu hóa DB và chạy trực tiếp các câu lệnh SQL tự do.
  - **Thống kê tổng quan (Stats Tab):** Phân tích thống kê tần suất sử dụng ứng dụng và các từ khóa trò chuyện phổ biến.

---

##  Kiến Trúc Thư Mục Dự Án (Project Structure)

Dự án tuân thủ nghiêm ngặt mô hình thiết kế **MVC (Model-View-Controller)** giúp tách biệt rõ ràng logic nghiệp vụ và giao diện hiển thị:

```text
Virtual-Assistant-main/
│
├── main.py                     # Entry point khởi tạo giao diện chính Pop Assistant
├── login.py                    # Trình chạy/Launcher quản lý vòng đời Đăng nhập & Gọi Admin ẩn
├── pyproject.toml              # Cấu hình đóng gói dự án
├── README.md                   # Tài liệu hướng dẫn sử dụng (File này)
│
├── admin/                      # Module quản trị hệ thống (Ẩn)
│   ├── controller/             # Xử lý logic nghiệp vụ cho Admin
│   ├── model/                  # Model dữ liệu riêng của Admin
│   └── view/                   # Giao diện Admin (AdminLogin, AdminPanel & các Tabs)
│       └── tabs/               # Các tab chức năng: users, health, database, conversations, stats
│
├── view/                       # Giao diện người dùng thường (View)
│   ├── pop_view.py             # Cửa sổ chính bong bóng trợ lý ảo Pop
│   ├── login_view.py           # Giao diện đăng nhập/đăng ký người dùng thường
│   ├── history_viewer.py       # Cửa sổ xem lịch sử hội thoại
│   └── widgets/                # Các widget giao diện nhỏ, tái sử dụng
│
├── controller/                 # Điều hướng và xử lý logic (Controller)
│   ├── pop_controller.py       # Controller chính kết nối PopView và các Service
│   ├── habit_tracker.py        # Quản lý logic tự học và theo dõi thói quen ứng dụng
│   ├── system_controller.py    # Điều khiển thu thập tài nguyên hệ thống
│   ├── voice_controller.py     # Điều khiển luồng thu âm và nhận diện giọng nói
│   └── user_controller.py      # Xử lý đăng nhập, hồ sơ người dùng
│
├── service/                    # Lớp dịch vụ hỗ trợ (Service Layer)
│   ├── system_monitoring_service.py # Theo dõi CPU, RAM, Disk, Battery, Temp
│   ├── proactive_service.py    # Phân tích sự cố hệ thống đưa ra cảnh báo chủ động
│   ├── AudioService.py         # Quản lý phát âm thanh, lời chào, tiếng click
│   ├── conversation_service.py # Xử lý hội thoại chatbot với database
│   ├── login_service.py        # Kiểm tra xác thực thông tin đăng nhập/đăng ký
│   └── wake_word.py            # Nhận diện từ khóa kích hoạt (Wake Word)
│
├── database/                   # Cơ sở dữ liệu SQLite & Repositories
│   ├── conversations.db        # File CSDL SQLite thực tế
│   ├── conversation_db.py      # Lớp điều khiển chính, định nghĩa Schema và Query CSDL
│   ├── base_repository.py      # Repository cơ sở
│   ├── habit_repository.py     # Đọc/ghi logs sử dụng ứng dụng & điểm thói quen
│   └── database_migration.py   # Quản lý nâng cấp, tạo cấu trúc bảng tự động
│
├── model/                      # Các tiện ích hệ thống và lớp thực thể (Model)
│   ├── temperature_monitor.py  # Core quản lý vòng đời & giao tiếp WMI với OHM/LHM
│   ├── usage_tracker.py        # Công cụ theo dõi ứng dụng đang active trên Windows
│   └── pop_system_utils.py     # Tiện ích tương tác Windows API
│
├── tools/                      # Các công cụ bổ trợ đi kèm
│   └── OpenHardwareMonitor/    # Thư mục chứa file thực thi OHM để đo nhiệt độ CPU
│
└── tests/                      # Thư mục chứa các kịch bản kiểm thử (Unit Tests)
    ├── test_habit_recommendation.py    # Kiểm thử hệ thống gợi ý thói quen
    ├── test_interactive_alert_service.py# Kiểm thử cảnh báo tương tác
    └── test_voice_session_service.py   # Kiểm thử tương tác giọng nói
