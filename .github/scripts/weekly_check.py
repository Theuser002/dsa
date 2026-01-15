import requests
import json
import os
from datetime import datetime, timedelta
import pytz

# Config
ALFA_LEETCODE_API = "https://alfa-leetcode-api.onrender.com"
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '')
MEMBERS_FILE = 'config/members.json'
PUNISHMENT_FILE = 'config/punishment.json'
DAILY_PROBLEMS_FILE = 'data/daily_problems.json'

def send_telegram_message(message):
    """Send message to Telegram group"""
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("Telegram credentials not configured, skipping message send")
        print(f"Message: {message}")
        return
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        print("Message sent successfully to Telegram")
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")

def get_this_week_daily_problems():
    """Get daily problems for this week (Mon-Fri) from history file"""
    try:
        with open(DAILY_PROBLEMS_FILE, 'r', encoding='utf-8') as f:
            all_problems = json.load(f)
    except Exception as e:
        print(f"Failed to load daily problems history: {e}")
        return {}
    
    # Get this week's date range
    vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    now_vn = datetime.now(vn_tz)
    days_since_monday = now_vn.weekday()
    monday = now_vn - timedelta(days=days_since_monday)
    monday = monday.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Get problems for this week (Mon-Fri only)
    week_problems = {}
    for i in range(5):  # Monday to Friday
        day = monday + timedelta(days=i)
        if day > now_vn:
            break  # Don't check future days
        
        date_str = day.strftime('%Y-%m-%d')
        if date_str in all_problems:
            week_problems[date_str] = all_problems[date_str]
    
    return week_problems, monday, now_vn

def check_daily_problem_completion(username, date_str, problem_slug):
    """Check if user completed a specific daily problem on a specific date"""
    try:
        url = f"{ALFA_LEETCODE_API}/{username}/submission"
        response = requests.get(url, params={"limit": 50}, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        submissions = data.get('submission', [])
        
        # Parse date range for the day
        vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        target_date = datetime.strptime(date_str, '%Y-%m-%d')
        target_date = vn_tz.localize(target_date)
        day_start = target_date.replace(hour=0, minute=0, second=0)
        day_end = target_date.replace(hour=23, minute=59, second=59)
        
        day_start_ts = int(day_start.timestamp())
        day_end_ts = int(day_end.timestamp())
        
        # Check if there's an accepted submission for this problem on this day
        for sub in submissions:
            timestamp = int(sub.get('timestamp', 0))
            title_slug = sub.get('titleSlug', '')
            status = sub.get('statusDisplay', '')
            
            if (day_start_ts <= timestamp <= day_end_ts and 
                title_slug == problem_slug and 
                status == 'Accepted'):
                return True
        
        return False
        
    except Exception as e:
        print(f"Error checking daily problem for {username} on {date_str}: {e}")
        return False

def count_daily_problems_completed(username, week_problems):
    """Count how many daily problems user completed this week"""
    completed_count = 0
    completed_dates = []
    
    for date_str, problem_info in week_problems.items():
        problem_slug = problem_info['titleSlug']
        if check_daily_problem_completion(username, date_str, problem_slug):
            completed_count += 1
            completed_dates.append(date_str)
    
    return completed_count, completed_dates

def main():
    """Main function to check weekly progress and send report"""
    print(f"Starting weekly check at {datetime.now()}")
    
    # Load members
    try:
        with open(MEMBERS_FILE, 'r', encoding='utf-8') as f:
            members = json.load(f)
    except Exception as e:
        print(f"Failed to load members file: {e}")
        return
    
    # Load punishment config
    try:
        with open(PUNISHMENT_FILE, 'r', encoding='utf-8') as f:
            punishment_config = json.load(f)
    except Exception as e:
        print(f"Failed to load punishment config: {e}")
        punishment_config = {"punishment_per_week": 500000, "min_problems_per_week": 3}
    
    min_problems = punishment_config['min_problems_per_week']
    punishment_amount = punishment_config['punishment_per_week']
    
    # Get this week's daily problems
    week_problems, monday, now_vn = get_this_week_daily_problems()
    
    if not week_problems:
        send_telegram_message("⚠️ Không có dữ liệu daily problems cho tuần này!")
        return
    
    # Calculate Friday for display
    friday = monday + timedelta(days=4)
    
    # Build report
    report = f"📊 *WEEKLY DSA REPORT*\n"
    report += f"Tuần: {monday.strftime('%d/%m')} - {friday.strftime('%d/%m/%Y')}\n"
    report += f"Yêu cầu: *{min_problems} bài DAILY*/tuần\n"
    report += f"Số bài daily tuần này: *{len(week_problems)}* bài\n\n"
    
    punishment_list = []
    safe_list = []
    
    for member in members:
        name = member['name']
        username = member['leetcode_username']
        telegram_id = member['telegram_id']
        
        count, completed_dates = count_daily_problems_completed(username, week_problems)
        
        if count >= min_problems:
            report += f"✅ *{name}*: {count}/{len(week_problems)} bài - SAFE\n"
            safe_list.append(name)
        else:
            remaining = min_problems - count
            report += f"❌ *{name}*: {count}/{len(week_problems)} bài - THIẾU {remaining} bài\n"
            punishment_list.append((name, telegram_id, count))
    
    report += "\n"
    
    if punishment_list:
        report += f"💸 *DANH SÁCH PHẠT (NỘP {punishment_amount:,}đ):*\n"
        for name, telegram_id, count in punishment_list:
            report += f"- {telegram_id} ({count}/{min_problems} bài daily)\n"
        report += "\n_Chuyển khoản vào quỹ nhóm trong tuần tới!_\n"
    else:
        report += "🎉 *PERFECT! Toàn bộ team đã hoàn thành mục tiêu tuần này!*\n"
        report += "_Tiếp tục phát huy! 💪_\n"
    
    # Send report
    send_telegram_message(report)
    print("Weekly check completed")

if __name__ == "__main__":
    main()
