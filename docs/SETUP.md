# TCB DSA Tracker

Hệ thống tự động tracking và nhắc nhở làm LeetCode Daily Problem cho team TCB Backend Developers.

## 🎯 Mục tiêu

- Duy trì thói quen làm LeetCode Daily Problem (Thứ 2 - Thứ 6)
- Tối thiểu **3 bài/tuần**
- Phạt **500,000 VND** nếu không đạt mục tiêu tuần

## 🤖 Tính năng

### 1. Morning Reminder (09:00 VN)
- Gửi link bài Daily Problem mỗi sáng
- Thông báo độ khó của bài

### 2. Daily Check (23:55 VN)
- Kiểm tra ai đã hoàn thành bài hôm nay
- Cảnh báo ngay những người chưa làm
- Nhắc nhở về mức phạt tuần

### 3. Weekly Report (18:00 Thứ 6)
- Tổng kết số bài đã làm trong tuần
- Danh sách những người bị phạt
- Số tiền phải nộp vào quỹ nhóm

## ⚙️ Cấu hình

### 1. Members Configuration
File: `config/members.json`
```json
[
  {
    "name": "Minh",
    "leetcode_username": "minhdq99hp",
    "telegram_id": "@mstarkdev"
  }
]
```

### 2. Punishment Rules
File: `config/punishment.json`
```json
{
  "punishment_per_week": 500000,
  "min_problems_per_week": 3,
  "description": "Nếu làm ít hơn 3 bài daily/tuần sẽ bị phạt 500k VND"
}
```

## 🚀 Setup

### 1. Tạo Telegram Bot

1. Chat với [@BotFather](https://t.me/BotFather) trên Telegram
2. Gửi `/newbot` và làm theo hướng dẫn
3. Lưu lại `TELEGRAM_BOT_TOKEN`

### 2. Lấy Chat ID

1. Add bot vào group chat
2. Gửi một tin nhắn bất kỳ trong group
3. Truy cập: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. Tìm `"chat":{"id":-XXXXXXXXX}` - đó là `TELEGRAM_CHAT_ID`

### 3. Cấu hình GitHub Secrets

Vào **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Thêm 2 secrets:
- `TELEGRAM_BOT_TOKEN`: Token từ BotFather
- `TELEGRAM_CHAT_ID`: Chat ID của group (bao gồm dấu `-`)

### 4. Kiểm tra cấu hình

```bash
# Test daily check
gh workflow run daily_check.yml

# Test weekly report
gh workflow run weekly_report.yml

# Test morning reminder
gh workflow run morning_reminder.yml
```

## 📊 Cách hoạt động

### Tracking System
- Sử dụng [Alfa LeetCode API](https://github.com/alfaarghya/alfa-leetcode-api) để lấy submissions
- API không cần authentication, hoàn toàn public
- Check submissions trong timezone Vietnam (UTC+7)

### Punishment System
- Mỗi tuần (Thứ 2 - Thứ 6) cần làm tối thiểu 3 bài Daily
- Thiếu = phạt 500k VND vào quỹ nhóm
- Cuối tháng dùng quỹ đi nhậu/cafe

### Notification Schedule
- **09:00**: Morning reminder với link bài mới
- **23:55**: Daily check + warning
- **18:00 Thứ 6**: Weekly report + punishment list

## 🧪 Testing Local

```bash
# Install dependencies
pip install requests pytz

# Set environment variables
export TELEGRAM_BOT_TOKEN="your_token"
export TELEGRAM_CHAT_ID="your_chat_id"

# Test daily check
python .github/scripts/daily_check.py

# Test weekly check
python .github/scripts/weekly_check.py
```

## 📝 Notes

- Chỉ tính submissions **Accepted**
- Không tính Thứ 7, Chủ Nhật
- Thời gian tính theo timezone Vietnam (UTC+7)
- Bot sẽ tag trực tiếp Telegram ID để reminder

## 🔧 Maintenance

### Thêm/Xóa thành viên
Edit `config/members.json` và commit lên repo

### Thay đổi mức phạt
Edit `config/punishment.json` và commit lên repo

### Xem logs
Vào **Actions** tab trên GitHub để xem execution logs

## 🤝 Contributors

- Minh (@mstarkdev) - minhdq99hp
- Hùng (@hnt0499) - hnt99
- Việt Anh (@unknown) - unknown

---

💪 *"Discipline beats motivation!"*
