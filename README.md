# 🎮 Dự án Cờ Caro AI (9x9) - Hướng Dẫn Vận Hành

Bài tập lớn môn Trí tuệ nhân tạo hiện thực hóa trò chơi cờ Caro đối kháng đối thủ máy (AI) trên lưới bàn cờ kích thước 9x9. Chương trình so sánh trực quan hiệu suất tính toán giữa thuật toán cây **Minimax cơ bản** và thuật toán cải tiến **Alpha-Beta Pruning**.

## 🎯 Luật Chơi (Game Rules)

### 1. Tổng quan
Caro (Gomoku) là trò chơi chiến thuật dành cho hai người chơi trên bàn cờ ô vuông.  
Trong dự án này, người chơi sẽ đấu với AI trên bàn cờ kích thước **9x9**.
---
### 2. Luật chơi

- Bàn cờ gồm lưới ô vuông kích thước **9x9**.
- Có hai bên tham gia:
  - Người chơi: ký hiệu `X` (đi trước)
  - Máy AI: ký hiệu `O`
- Hai bên lần lượt đặt quân vào các ô trống trên bàn cờ.
- Người chiến thắng là bên tạo được:
  - 4 quân liên tiếp theo:
    - hàng ngang
    - hàng dọc
    - hoặc đường chéo
- Không áp dụng luật chặn hai đầu.
- Nếu bàn cờ đầy mà không bên nào tạo được 4 quân liên tiếp thì kết quả là hòa.
  
## 📂 Cấu trúc thư mục mã nguồn (Project Structure)

Dự án được cấu trúc tường minh và chuẩn hóa theo đúng Barebone mẫu của học phần, giúp phân tách rõ ràng giữa giao diện, logic trò chơi và các module thuật toán:
```text
📁 23021319_23021284_23021279_CaroAI
├── 📁 source_code/             # Thư mục chứa toàn bộ mã nguồn thực thi
│   ├── 📄 main.py              # File chạy chính (Khởi chạy luồng game và giao diện Pygame)
│   ├── 📄 caro_logic.py        # Quản lý ma trận bàn cờ, kiểm tra luật thắng/hòa, sinh nước đi
│   ├── 📄 ai_player.py         # Hiện thực cơ chế tìm kiếm cây quyết định (Minimax & Alpha-Beta)
│   ├── 📄 scoring.py           # Hàm đánh giá heuristic cục bộ (Tính toán trọng số ô cờ)
│   └── 📄 ai_tester.py         # Module đo đạc Benchmark (Thời gian phản hồi, số trạng thái đã xét)
├── 📄 README.md                # Tài liệu hướng dẫn vận hành hệ thống (File này)
└── 📄 requirements.txt         # Khai báo các thư viện phụ thuộc của dự án (Pygame)
