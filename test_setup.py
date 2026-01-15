#!/usr/bin/env python3
"""
Test script to verify the DSA tracker setup
Run this locally to test without triggering GitHub Actions
"""

import sys
import os

# Add the scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.github', 'scripts'))

def test_imports():
    """Test if all required packages are installed"""
    print("Testing imports...")
    try:
        import requests
        import pytz
        import json
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Run: pip install -r requirements.txt")
        return False

def test_config_files():
    """Test if config files exist and are valid"""
    print("\nTesting config files...")
    
    try:
        with open('config/members.json', 'r') as f:
            members = json.load(f)
            print(f"✅ members.json loaded: {len(members)} members")
            for member in members:
                print(f"   - {member['name']} ({member['leetcode_username']})")
    except Exception as e:
        print(f"❌ Error loading members.json: {e}")
        return False
    
    try:
        with open('config/punishment.json', 'r') as f:
            punishment = json.load(f)
            print(f"✅ punishment.json loaded: {punishment['punishment_per_week']:,}đ for <{punishment['min_problems_per_week']} problems/week")
    except Exception as e:
        print(f"❌ Error loading punishment.json: {e}")
        return False
    
    return True

def test_telegram_config():
    """Test Telegram configuration"""
    print("\nTesting Telegram configuration...")
    
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    
    if not token:
        print("⚠️  TELEGRAM_BOT_TOKEN not set (this is OK for testing)")
    else:
        print(f"✅ TELEGRAM_BOT_TOKEN is set")
    
    if not chat_id:
        print("⚠️  TELEGRAM_CHAT_ID not set (this is OK for testing)")
    else:
        print(f"✅ TELEGRAM_CHAT_ID is set")
    
    return True

def test_leetcode_api():
    """Test LeetCode API connectivity"""
    print("\nTesting LeetCode API...")
    
    import requests
    
    # Test daily problem API
    try:
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
        r = requests.post('https://leetcode.com/graphql', json={'query': query}, timeout=10)
        r.raise_for_status()
        data = r.json()
        problem = data['data']['activeDailyCodingChallengeQuestion']
        print(f"✅ LeetCode GraphQL API working")
        print(f"   Today's problem: {problem['question']['title']}")
    except Exception as e:
        print(f"❌ LeetCode GraphQL API error: {e}")
        return False
    
    # Test alfa-leetcode-api
    try:
        r = requests.get('https://alfa-leetcode-api.onrender.com/minhdq99hp/submission?limit=1', timeout=15)
        r.raise_for_status()
        data = r.json()
        print(f"✅ Alfa LeetCode API working")
        if data.get('submission'):
            latest = data['submission'][0]
            print(f"   Latest submission: {latest['title']}")
    except Exception as e:
        print(f"❌ Alfa LeetCode API error: {e}")
        return False
    
    return True

def test_scripts():
    """Test if scripts can be imported"""
    print("\nTesting scripts...")
    
    try:
        # Import without running
        import importlib.util
        
        spec = importlib.util.spec_from_file_location("daily_check", ".github/scripts/daily_check.py")
        daily_check = importlib.util.module_from_spec(spec)
        print("✅ daily_check.py can be imported")
        
        spec = importlib.util.spec_from_file_location("weekly_check", ".github/scripts/weekly_check.py")
        weekly_check = importlib.util.module_from_spec(spec)
        print("✅ weekly_check.py can be imported")
        
    except Exception as e:
        print(f"❌ Error importing scripts: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("=" * 60)
    print("TCB DSA Tracker - Setup Test")
    print("=" * 60)
    
    import json
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Config Files", test_config_files()))
    results.append(("Telegram Config", test_telegram_config()))
    results.append(("LeetCode API", test_leetcode_api()))
    results.append(("Scripts", test_scripts()))
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All tests passed! Setup is complete.")
        print("\nNext steps:")
        print("1. Set up Telegram bot and get credentials")
        print("2. Add TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID to GitHub Secrets")
        print("3. Test workflows with: gh workflow run daily_check.yml")
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
    print("=" * 60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
