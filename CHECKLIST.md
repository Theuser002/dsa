# Setup Checklist - TCB DSA Tracker

## ✅ Completed

- [x] Create project structure
- [x] Configure members.json with 3 team members
- [x] Configure punishment.json (500k VND, 3 bài/tuần)
- [x] Create daily_check.py script
- [x] Create weekly_check.py script
- [x] Create 3 GitHub Actions workflows:
  - [x] morning_reminder.yml (09:00)
  - [x] daily_check.yml (23:55)
  - [x] weekly_report.yml (18:00 Friday)
- [x] Test Alfa LeetCode API (verified working without auth)
- [x] Test scripts locally (working correctly)
- [x] Create comprehensive documentation
- [x] Create test_setup.py for validation

## 🔲 Remaining Tasks (To Do)

### 1. Telegram Bot Setup
- [ ] Chat với @BotFather trên Telegram
- [ ] Create new bot với `/newbot` command
- [ ] Copy TELEGRAM_BOT_TOKEN từ BotFather
- [ ] Add bot vào group chat của team
- [ ] Gửi một message bất kỳ trong group
- [ ] Lấy TELEGRAM_CHAT_ID:
  ```bash
  curl "https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates"
  # Tìm "chat":{"id":-XXXXXXXXX}
  ```

### 2. GitHub Secrets Configuration
- [ ] Vào repo: https://github.com/Theuser002/dsa
- [ ] Settings → Secrets and variables → Actions
- [ ] New repository secret → `TELEGRAM_BOT_TOKEN`
- [ ] New repository secret → `TELEGRAM_CHAT_ID`

### 3. Verify LeetCode Usernames
- [ ] Confirm `minhdq99hp` is correct ✅ (verified)
- [ ] Confirm `hnt99` is correct
- [ ] Update `unknown` with Việt Anh's real username
  ```bash
  # Test username exists:
  curl "https://alfa-leetcode-api.onrender.com/<username>/submission?limit=1"
  ```

### 4. Test Workflows
- [ ] Manually trigger morning_reminder:
  ```bash
  gh workflow run morning_reminder.yml
  ```
- [ ] Manually trigger daily_check:
  ```bash
  gh workflow run daily_check.yml
  ```
- [ ] Manually trigger weekly_report:
  ```bash
  gh workflow run weekly_report.yml
  ```
- [ ] Check Telegram group for messages
- [ ] Review logs in Actions tab

### 5. Monitor First Week
- [ ] Check if morning reminders arrive at 09:00
- [ ] Check if daily checks arrive at 23:55
- [ ] Verify user submissions are detected correctly
- [ ] Adjust timezone if needed
- [ ] Fix any issues found

## 📋 Quick Reference

### Workflow Schedules (VN Time)
- **09:00**: Morning Reminder (Mon-Fri)
- **23:55**: Daily Check (Mon-Fri)  
- **18:00**: Weekly Report (Friday)

### Important Files
```
config/members.json      # Update thành viên
config/punishment.json   # Thay đổi quy định phạt
.github/workflows/       # Chỉnh schedule
.github/scripts/         # Logic scripts
```

### Useful Commands
```bash
# Test locally
python3 -m venv venv
source venv/bin/activate
pip install requests pytz
export TELEGRAM_BOT_TOKEN="..."
export TELEGRAM_CHAT_ID="..."
python .github/scripts/daily_check.py

# Trigger workflows manually
gh workflow run daily_check.yml

# View workflow runs
gh run list
gh run view <run-id>

# Update members
# Edit config/members.json and commit
git add config/members.json
git commit -m "Update members"
git push
```

## 🐛 Troubleshooting

### Issue: Bot không gửi được message
**Check:**
1. Bot đã được add vào group chưa?
2. TELEGRAM_CHAT_ID có dấu `-` không?
3. Token có đúng không?
4. Bot có quyền send message không?

**Solution:**
```bash
# Verify credentials
curl "https://api.telegram.org/bot<TOKEN>/getMe"
curl "https://api.telegram.org/bot<TOKEN>/getUpdates"
```

### Issue: Không detect được submission
**Check:**
1. LeetCode username có đúng không?
2. Submission có status "Accepted" không?
3. Timezone có đúng không?

**Solution:**
```bash
# Test username
curl "https://alfa-leetcode-api.onrender.com/<username>/submission?limit=5"
```

### Issue: Workflow không chạy
**Check:**
1. GitHub Actions có enabled không?
2. Secrets đã setup chưa?
3. Workflow file syntax có đúng không?

**Solution:**
- Check Actions tab trên GitHub
- Manually trigger để test
- Review workflow logs

## 📞 Contact

Nếu cần support:
- Check IMPLEMENTATION.md cho detailed info
- Check docs/SETUP.md cho setup guide
- Review workflow logs trong Actions tab
- Test với test_setup.py script

---

**Next Step**: Setup Telegram Bot và add credentials vào GitHub Secrets, sau đó test workflows!
