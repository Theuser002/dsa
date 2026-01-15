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

def get_daily_problem():
    """Get today's daily problem from Alfa LeetCode API"""
    try:
        r = requests.get(f"{ALFA_LEETCODE_API}/daily", timeout=10)
        r.raise_for_status()
        data = r.json()
        return {
            'date': data['date'],
            'link': data['questionLink'],
            'question': {
                'title': data['questionTitle'],
                'titleSlug': data['titleSlug']
            }
        }
    except Exception as e:
        print(f"Failed to fetch daily problem: {e}")
        return None

def save_daily_problem(date_str, title_slug, title):
    """Save daily problem to history file"""
    try:
        # Load existing history
        if os.path.exists(DAILY_PROBLEMS_FILE):
            with open(DAILY_PROBLEMS_FILE, 'r', encoding='utf-8') as f:
                history = json.load(f)
        else:
            history = {}
        
        # Add today's problem
        history[date_str] = {
            'titleSlug': title_slug,
            'title': title
        }
        
        # Save back
        with open(DAILY_PROBLEMS_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
        
        print(f"Saved daily problem for {date_str}: {title}")
    except Exception as e:
        print(f"Failed to save daily problem: {e}")

def check_user_submission_today(username, question_slug):
    """Check if user has submitted the daily problem today using alfa-leetcode-api"""
    try:
        # Get recent submissions from alfa-leetcode-api
        url = f"{ALFA_LEETCODE_API}/{username}/submission"
        params = {"limit": 20}
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        submissions = data.get('submission', [])
        
        # Get current time in Vietnam timezone
        vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        now_vn = datetime.now(vn_tz)
        today_start = now_vn.replace(hour=0, minute=0, second=0, microsecond=0)
        today_start_ts = int(today_start.timestamp())
        
        # Check if there's a submission for today's daily problem
        for sub in submissions:
            timestamp = int(sub.get('timestamp', 0))
            title_slug = sub.get('titleSlug', '')
            status = sub.get('statusDisplay', '')
            
            # Check if submission is from today and matches the daily problem
            if timestamp >= today_start_ts and title_slug == question_slug:
                # Only count accepted submissions
                if status == 'Accepted':
                    return True, "✅"
                
        return False, "❌"
        
    except Exception as e:
        print(f"Error checking submission for {username}: {e}")
        return False, "⚠️"

def main():
    """Main function to check daily progress and send report"""
    print(f"Starting daily check at {datetime.now()}")
    
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
    
    # Get daily problem
    daily = get_daily_problem()
    if not daily:
        send_telegram_message("⚠️ Không thể lấy thông tin bài Daily Problem hôm nay!")
        return
    
    question_title = daily['question']['title']
    question_slug = daily['question']['titleSlug']
    question_link = daily['link']
    date_str = daily['date']
    
    # Save daily problem to history
    save_daily_problem(date_str, question_slug, question_title)
    
    # Get current time in Vietnam timezone
    vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    now_vn = datetime.now(vn_tz)
    
    # Build report
    report = f"📅 *DSA Daily Report: {now_vn.strftime('%d/%m/%Y')}*\n"
    report += f"Bài toán: [{question_title}]({question_link})\n\n"
    
    missing_people = []
    completed_people = []
    
    for member in members:
        name = member['name']
        username = member['leetcode_username']
        telegram_id = member['telegram_id']
        
        is_done, status_emoji = check_user_submission_today(username, question_slug)
        
        if is_done:
            report += f"{status_emoji} *{name}*: Done\n"
            completed_people.append(name)
        else:
            report += f"{status_emoji} *{name}*: MISSING\n"
            missing_people.append(telegram_id)
    
    report += "\n"
    
    if missing_people:
        report += f"⚠️ *CẢNH BÁO:* {', '.join(missing_people)}\n"
        report += f"Nhớ làm bài để tránh phạt {punishment_config['punishment_per_week']:,}đ nếu thiếu quá {punishment_config['min_problems_per_week']} bài daily/tuần!\n"
    else:
        report += "🎉 *Tuyệt vời! Full team đã hoàn thành!*\n"
    
    # Send report
    send_telegram_message(report)
    print("Daily check completed")

if __name__ == "__main__":
    main()
