# Quick Start Guide - TCB DSA Tracker

## ✅ Current Status: TESTED & WORKING!

All scripts have been tested with your Telegram bot and are working perfectly.

## 🚀 Deploy to GitHub Actions (5 minutes)

### Step 1: Add Secrets to GitHub (2 mins)

Go to: https://github.com/Theuser002/dsa/settings/secrets/actions

Add two secrets:

1. **TELEGRAM_BOT_TOKEN**
   ```
   Value: 8318868474:AAHdy-S5_E1MSEvC_-F_fyATtYsOO0PLSdM
   ```

2. **TELEGRAM_CHAT_ID**
   ```
   Value: -5146734961
   ```

### Step 2: Commit and Push (2 mins)

```bash
# Stage all files
git add .github/ config/ docs/ *.md requirements.txt test_setup.py test_with_credentials.sh

# Commit
git commit -m "feat: Add automated DSA tracking system

- Daily check at 23:55 (Mon-Fri)
- Weekly report at 18:00 Friday
- Morning reminder at 09:00 (Mon-Fri)
- Punishment: 500k VND for <3 problems/week
- Using alfa-leetcode-api (no auth required)

Tested and verified working with Telegram integration"

# Push
git push
```

### Step 3: Test Workflows (1 min)

```bash
# Manually trigger each workflow to test
gh workflow run morning_reminder.yml
gh workflow run daily_check.yml
gh workflow run weekly_report.yml

# Check if they ran successfully
gh run list --limit 3
```

## 📅 Schedule Summary

Once deployed, the bot will automatically:

| Time | Action | Message |
|------|--------|---------|
| **09:00** Mon-Fri | Morning Reminder | Daily problem link + difficulty |
| **23:55** Mon-Fri | Daily Check | Who completed today's problem |
| **18:00** Friday | Weekly Report | Punishment list for <3 problems |

## 🧪 Test Locally Anytime

```bash
# Quick test with your credentials
./test_with_credentials.sh

# Or manual test
source venv/bin/activate
export TELEGRAM_BOT_TOKEN=$(grep TELEGRAM_API_KEY .env | cut -d'=' -f2)
export TELEGRAM_CHAT_ID=$(grep TELEGRAM_CHAT_ID .env | cut -d'=' -f2)
python .github/scripts/daily_check.py
```

## ⚙️ Update Configuration

### Add/Remove Members
Edit `config/members.json`:
```json
[
  {
    "name": "New Member",
    "leetcode_username": "their_leetcode_username",
    "telegram_id": "@their_telegram"
  }
]
```

### Change Punishment Rules
Edit `config/punishment.json`:
```json
{
  "punishment_per_week": 1000000,
  "min_problems_per_week": 5,
  "description": "..."
}
```

Then commit and push - workflows will use new config automatically!

## 📊 Monitor Workflows

### View Workflow Status
```bash
# List recent runs
gh run list

# View specific run details
gh run view <run-id>

# View logs
gh run view <run-id> --log
```

### Or use GitHub Web UI
Go to: https://github.com/Theuser002/dsa/actions

## 🐛 Troubleshooting

### Workflow not running?
1. Check if GitHub Actions is enabled in repo settings
2. Verify secrets are added correctly
3. Check workflow syntax with: `gh workflow view <workflow-name>`

### Messages not sent to Telegram?
1. Test locally first: `./test_with_credentials.sh`
2. Verify bot is in the group
3. Check bot has permission to send messages
4. Review workflow logs for errors

### Username not found?
1. Verify LeetCode username:
   ```bash
   curl "https://alfa-leetcode-api.onrender.com/<username>/submission?limit=1"
   ```
2. Update `config/members.json` if needed

## 📱 Expected Telegram Messages

### Morning (09:00)
```
☀️ Chào buổi sáng! DSA Daily Challenge

📝 [Problem Title](link)
Độ khó: Medium

💪 Cùng nhau chinh phục bài hôm nay nhé!
```

### Evening (23:55)
```
📅 DSA Daily Report: 10/01/2026
Bài toán: [Problem Title](link)

✅ Minh: Done
❌ Hùng: MISSING

⚠️ CẢNH BÁO: @hnt0499
Nhớ làm bài để tránh phạt 500,000đ!
```

### Friday (18:00)
```
📊 WEEKLY DSA REPORT
Tuần: 06/01 - 10/01/2026
Yêu cầu tối thiểu: 3 bài/tuần

✅ Minh: 4 bài - SAFE
❌ Hùng: 2 bài - THIẾU 1 bài

💸 DANH SÁCH PHẠT (NỘP 500,000đ):
- @hnt0499 (2/3 bài)
```

## 🎯 Success Checklist

- [x] Scripts created and tested locally ✅
- [x] Telegram bot configured ✅
- [x] API connectivity verified ✅
- [x] Members configured ✅
- [x] Punishment rules set ✅
- [ ] GitHub Secrets added ⏳
- [ ] Workflows tested on GitHub ⏳
- [ ] Monitor first week ⏳

## 📚 Documentation

- **TEST_REPORT.md** - Full test results
- **SUMMARY.md** - Complete overview
- **IMPLEMENTATION.md** - Technical details
- **CHECKLIST.md** - Detailed setup steps
- **docs/SETUP.md** - Comprehensive guide

## 💡 Pro Tips

1. **Test first**: Always run `./test_with_credentials.sh` before pushing changes
2. **Manual triggers**: Use `gh workflow run` to test workflows before waiting for schedule
3. **Watch logs**: Check Actions tab after first few scheduled runs
4. **Update quickly**: Just edit JSON configs and commit - no code changes needed

---

**Ready to deploy?** Just add the secrets and push! 🚀

Need help? Check TEST_REPORT.md for detailed test results.
