Tôi đang có nhóm bạn đồng nghiệp - 3 backend developers đang cần luyện DSA trên leetcode. Mục tiêu hiện tại là duy trì việc làm daily problem (trừ thứ 7, chủ nhật). Nhóm tôi có nhóm chat trên telegram. Và sử dụng repo https://github.com/Theuser002/dsa để chia sẻ code, tài liệu về DSA. Tuy nhiên, mọi người đều khá bận với full-time job, và thiếu motivate để duy trì việc luyện DSA hàng ngày như vậy.

Ý tưởng của tôi là có giải pháp automation nào đó để giúp chúng tôi có động lực, cũng như tracking tiến độ, tracking habit, có thưởng, có phạt,... Tôi đang nghĩ đến github actions, n8n workflow, hoặc là telegram chat bot trong nhóm chat đó. 

Bạn có gợi ý gì không? Lên giúp tôi một solution hoàn chỉnh. Code với chúng tôi không thành vấn đề, nhưng cũng cần tận dụng nhiều giải pháp sẵn có càng tốt để tiết kiệm effort của mọi người.

---

Chào bạn, ý tưởng của bạn rất thực tế. Là Backend Developer, tôi hiểu cái khó nhất không phải là độ khó của bài toán, mà là **kỷ luật** (discipline) sau một ngày làm việc mệt mỏi.

Với 3 anh em backend dev, giải pháp cần phải: **Tự động hóa hoàn toàn (Zero manual effort)**, **Minh bạch (Public shaming/praising)**, và **Tận dụng hạ tầng có sẵn (GitHub Repo)**.

Dưới đây là một giải pháp "All-in-one" tôi thiết kế cho team bạn, sử dụng **GitHub Actions** làm engine chính (miễn phí, không cần server riêng như n8n) kết hợp với **Telegram Bot**.

---

### Chiến lược Gamification: "DSA Daily Gym"

Trước khi đi vào code, chúng ta cần "luật chơi" để automation có ý nghĩa:

1. **Tracking:** Bot sẽ check profile LeetCode của từng người vào 23:55 hàng ngày.
2. **Reward:** Cuối tuần, ai full streak sẽ được vinh danh (Badge ảo/Title trong group).
3. **Punishment (Quan trọng):** "Quỹ đen". Ai miss daily problem sẽ phải bank 50k - 100k vào quỹ chung. Cuối tháng dùng quỹ đó đi nhậu hoặc cafe.
4. **Flow:**
* *09:00:* Bot gửi link Daily Problem vào group Telegram.
* *23:55:* Bot quét status, báo cáo ai Done, ai Miss, và cập nhật Leaderboard.



---

### Giải pháp kỹ thuật (Implementation)

Chúng ta sẽ viết một script Python chạy trên GitHub Actions. Lý do chọn Python vì dễ handle JSON và request tới API của LeetCode (GraphQL).

#### Bước 1: Chuẩn bị Telegram Bot

1. Chat với **@BotFather** trên Telegram, tạo bot mới, lấy `TELEGRAM_BOT_TOKEN`.
2. Add con bot đó vào group chat của 3 anh em.
3. Lấy `TELEGRAM_CHAT_ID` của group (có thể dùng bot @userinfobot hoặc getUpdates API để lấy ID, thường bắt đầu bằng dấu âm `-`).

#### Bước 2: Cấu hình User Mapping

Trong repo `dsa` hiện tại, bạn tạo một file `config/members.json`. File này map giữa tên thật và username LeetCode.

```json
[
  { "name": "Dev A", "leetcode_username": "dev_a_leetcode", "telegram_id": "@deva" },
  { "name": "Dev B", "leetcode_username": "dev_b_123", "telegram_id": "@devb" },
  { "name": "Dev C", "leetcode_username": "super_coder", "telegram_id": "@devc" }
]

```

#### Bước 3: Script Python Logic (Core)

Tạo file `.github/scripts/daily_check.py`. Script này sẽ:

1. Lấy thông tin Daily Problem hôm nay.
2. Loop qua từng user trong `members.json`.
3. Query GraphQL của LeetCode để xem user đó đã submit bài Daily hôm nay chưa.
4. Gửi báo cáo về Telegram.

Dưới đây là đoạn code mẫu (tôi đã tối ưu query GraphQL):

```python
import requests
import json
import os
from datetime import datetime
import pytz

# Config
LEETCODE_URL = "https://leetcode.com/graphql"
TELEGRAM_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
MEMBERS_FILE = 'config/members.json'

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

def get_daily_problem():
    query = """
    query questionOfToday {
        activeDailyCodingChallengeQuestion {
            date
            link
            question {
                title
                titleSlug
            }
        }
    }
    """
    r = requests.post(LEETCODE_URL, json={'query': query})
    data = r.json()
    return data['data']['activeDailyCodingChallengeQuestion']

def check_user_submission(username, question_slug):
    # Query check 20 submission gần nhất xem có bài daily không
    query = """
    query recentAcSubmissions($username: String!, $limit: Int!) {
        recentAcSubmissionList(username: $username, limit: $limit) {
            titleSlug
            timestamp
        }
    }
    """
    variables = {"username": username, "limit": 20}
    r = requests.post(LEETCODE_URL, json={'query': query, 'variables': variables})
    submissions = r.json().get('data', {}).get('recentAcSubmissionList', [])
    
    # Check if submission is today (UTC check) and matches slug
    # Note: Logic check time cần điều chỉnh theo Timezone VN nếu cần chính xác tuyệt đối
    # Ở đây check đơn giản: có submission khớp slug là được tính (để đơn giản hóa)
    for sub in submissions:
        if sub['titleSlug'] == question_slug:
            # Có thể check thêm timestamp nếu muốn strict time window
            return True
    return False

def main():
    daily = get_daily_problem()
    question_title = daily['question']['title']
    question_slug = daily['question']['titleSlug']
    
    with open(MEMBERS_FILE, 'r') as f:
        members = json.load(f)
    
    report = f"📅 **DSA Daily Report: {datetime.now().strftime('%d/%m')}**\n"
    report += f"Bài toán: [{question_title}](https://leetcode.com{daily['link']})\n\n"
    
    missing_people = []
    
    for member in members:
        is_done = check_user_submission(member['leetcode_username'], question_slug)
        status = "✅ Done" if is_done else "❌ MISSING"
        report += f"- {member['name']}: {status}\n"
        if not is_done:
            missing_people.append(member['telegram_id'])
            
    if missing_people:
        report += "\n💸 **SHAME LIST (Nộp phạt đi):** " + ", ".join(missing_people)
    else:
        report += "\n🎉 **Tuyệt vời! Full team đã hoàn thành!**"

    send_telegram_message(report)

if __name__ == "__main__":
    main()

```

#### Bước 4: GitHub Actions Workflow

Tạo file `.github/workflows/dsa_tracker.yml`. Workflow này sẽ chạy theo lịch trình (Cron).

```yaml
name: DSA Daily Tracker

on:
  schedule:
    # Chạy vào 23:30 giờ VN (tức là 16:30 UTC) các ngày trong tuần (Mon-Fri)
    - cron: '30 16 * * 1-5'
  workflow_dispatch: # Cho phép chạy thủ công để test

jobs:
  check-progress:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: pip install requests pytz

      - name: Run Check Script
        env:
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
        run: python .github/scripts/daily_check.py

```

*Lưu ý: Bạn cần vào Settings của Repo -> Secrets and variables -> Actions để thêm `TELEGRAM_BOT_TOKEN` và `TELEGRAM_CHAT_ID`.*

---

### Mở rộng (Advanced Features)

Để team thêm hào hứng, bạn có thể bổ sung thêm các tính năng sau này:

1. **Workflow buổi sáng:** Tạo thêm một file workflow khác chạy lúc 9:00 sáng, chỉ đơn giản là gọi API lấy link bài daily và gửi vào group để nhắc nhở ("Morning Reminder").
2. **Leaderboard dài hạn:** Lưu kết quả vào một file `stats.json` ngay trong repo (dùng action `stefanzweifel/git-auto-commit-action` để commit lại file sau khi chạy script). Script sẽ đọc file này để tính streak liên tục bao nhiêu ngày.
3. **Sync Code:** Khuyến khích mọi người setup **LeetCode Sync** (Extension chrome) để khi submit trên web LeetCode, code tự động push về repo Github cá nhân hoặc repo chung này.

### Tại sao giải pháp này phù hợp với bạn?

1. **Zero Maintenance:** GitHub Actions chạy trên server của GitHub, bạn không cần lo tiền host hay VPS chết.
2. **Đánh vào tâm lý:** Thông báo gửi thẳng vào Telegram group nơi mọi người chat hàng ngày. Việc bị tag tên vào "Shame list" trước mặt đồng nghiệp là động lực rất lớn.
3. **Scalable:** Sau này có thêm thành viên, chỉ cần thêm 1 dòng vào file `members.json`.

### Bước tiếp theo tôi có thể làm cho bạn

Bạn có muốn tôi viết sẵn **File Python Script hoàn chỉnh** (bao gồm cả xử lý múi giờ Việt Nam chuẩn xác và xử lý lỗi khi API LeetCode timeout) để bạn chỉ việc copy-paste vào repo không?