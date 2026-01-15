# Daily Problem Tracking System

## ⚠️ IMPORTANT CHANGE: Tracking DAILY Problems Only

### The Problem
Initially, the system counted ANY accepted problems in a week. But the requirement is:
> **Phạt 500k nếu làm ít hơn 3 bài DAILY/tuần**

This means we need to track **daily problems specifically**, not random problems.

## 📊 How It Works Now

### 1. Daily Problem History (`data/daily_problems.json`)

Every day when `daily_check.py` runs, it:
1. Fetches today's daily problem from LeetCode
2. Saves it to `data/daily_problems.json` with the date

Example:
```json
{
  "2026-01-06": {
    "titleSlug": "maximum-product-of-splitted-binary-tree",
    "title": "Maximum Product of Splitted Binary Tree"
  },
  "2026-01-07": {
    "titleSlug": "max-dot-product-of-two-subsequences",
    "title": "Max Dot Product of Two Subsequences"
  },
  "2026-01-10": {
    "titleSlug": "minimum-ascii-delete-sum-for-two-strings",
    "title": "Minimum ASCII Delete Sum for Two Strings"
  }
}
```

### 2. Weekly Check Process

At the end of the week (Friday 18:00), `weekly_check.py`:

1. **Loads the daily problems history** from `data/daily_problems.json`
2. **Gets this week's daily problems** (Monday to Friday only)
3. **For each member**, checks their submissions:
   - Did they solve Monday's daily problem on Monday?
   - Did they solve Tuesday's daily problem on Tuesday?
   - etc.
4. **Counts** how many daily problems each member completed
5. **Compares** with minimum requirement (3 daily problems)
6. **Reports** who needs punishment

## 🔍 Example Scenario

### Week of Jan 6-10, 2026

**Daily Problems:**
- Mon 06/01: "Maximum Product of Splitted Binary Tree"
- Tue 07/01: "Max Dot Product of Two Subsequences"
- Wed 08/01: "Smallest Subtree with all the Deepest Nodes"
- Thu 09/01: "Find Eventually Safe States"
- Fri 10/01: "Minimum ASCII Delete Sum for Two Strings"

**Minh's Activity:**
- Mon: ✅ Solved "Maximum Product..." 
- Tue: ✅ Solved "Max Dot Product..."
- Wed: ❌ Didn't solve
- Thu: ❌ Solved a different problem (doesn't count!)
- Fri: ✅ Solved "Minimum ASCII..."

**Result:** Minh completed 3/5 daily problems → **SAFE** ✅

**Hùng's Activity:**
- Mon: ✅ Solved "Maximum Product..."
- Tue: ❌ Didn't solve
- Wed: ❌ Didn't solve
- Thu: ❌ Didn't solve
- Fri: ❌ Didn't solve

**Result:** Hùng completed 1/5 daily problems → **PUNISHMENT 500k** 💸

## 🎯 Key Differences from Before

### ❌ OLD (Incorrect)
- Counted ANY accepted problems in the week
- If you solved 3 random problems → SAFE
- Not tracking daily problems specifically

### ✅ NEW (Correct)
- Only counts DAILY problems
- Must solve the specific daily problem on that day (or later)
- Tracks exact daily problem history
- If you solved the Monday daily on Tuesday → still counts!
- But solving a random problem doesn't count

## 📁 File Structure

```
tcb-dsa/
├── data/
│   └── daily_problems.json    # History of daily problems
├── config/
│   ├── members.json           # Team members
│   └── punishment.json        # Rules (500k, 3 problems)
└── .github/
    └── scripts/
        ├── daily_check.py     # Runs at 23:55, saves daily problem
        └── weekly_check.py    # Runs Friday 18:00, checks history
```

## 🔧 How Data is Maintained

### Automatic (GitHub Actions)
- **Daily Check (23:55)**: Automatically saves today's daily problem
- **Weekly Report (Friday 18:00)**: Uses saved history to check

### Manual (If Needed)
If you miss a day or need to add historical data:

```bash
# Edit data/daily_problems.json
{
  "2026-01-XX": {
    "titleSlug": "problem-slug-here",
    "title": "Problem Title Here"
  }
}
```

Get the problem info from: https://alfa-leetcode-api.onrender.com/daily

## ✅ Testing

Current week (Jan 6-10, 2026):
- ✅ Minh: 3/5 daily problems → SAFE
- ❌ Hùng: 1/5 daily problems → 500k punishment
- ✅ Việt Anh: 3/5 daily problems → SAFE

This is the correct behavior!

## 🚨 Important Notes

1. **You can solve daily problems late**: If you missed Monday's daily, you can still solve it on Tuesday and it counts.

2. **Only accepted submissions count**: Wrong answers don't count.

3. **Data persists**: The `data/daily_problems.json` file is committed to the repo, so history is preserved.

4. **Weekend doesn't count**: Only Monday-Friday daily problems.

5. **Minimum is 3 out of 5**: Even if there are 5 daily problems, you only need 3 to avoid punishment.

## 📊 API Used

### Alfa LeetCode API
- **Daily Problem**: `GET https://alfa-leetcode-api.onrender.com/daily`
  - Returns today's daily problem with date, title, slug
  
- **User Submissions**: `GET https://alfa-leetcode-api.onrender.com/{username}/submission?limit=50`
  - Returns user's recent submissions with timestamps
  
- **No authentication required!** ✅

## 🔄 Workflow

```
Monday 09:00  → Morning reminder (today's daily)
Monday 23:55  → Daily check + save to history

Tuesday 09:00  → Morning reminder
Tuesday 23:55  → Daily check + save to history

... (repeat Wed, Thu)

Friday 09:00  → Morning reminder
Friday 18:00  → Weekly report (check all 5 days)
Friday 23:55  → Daily check + save to history
```

---

**This ensures accurate tracking of DAILY problems, not just any problems!** 🎯
