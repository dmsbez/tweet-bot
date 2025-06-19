import time, subprocess, json, requests
from flask import Flask
from threading import Thread

# ===== CẤU HÌNH BOT TELEGRAM =====
TELEGRAM_TOKEN = '7970022703:AAEFU0v_402lujK3-FHkP6xW0NXKeteco3U'
TELEGRAM_CHAT_ID = '-1001875640464'

# Danh sách người cần theo dõi
TWITTER_USERS = ['elonmusk', 'cz_binance', 'JnP6900erc', 'VitalikButerin']
last_tweet_ids = {}

# ===== GỬI TIN NHẮN TELEGRAM =====
def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    try:
        requests.post(url, data={'chat_id': TELEGRAM_CHAT_ID, 'text': message})
    except Exception as e:
        print("❌ Lỗi gửi Telegram:", e)

# ===== SCRAPE TWEET MỚI NHẤT =====
def scrape_latest_tweet(user):
    try:
        cmd = f"snscrape --jsonl --max-results 1 twitter-user {user}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        lines = result.stdout.strip().splitlines()
        if not lines:
            return None, None, None
        tweet = json.loads(lines[0])
        return tweet['id'], tweet['content'], tweet['url']
    except Exception as e:
        print(f"❌ Lỗi scrape {user}:", e)
        return None, None, None

# ===== THEO DÕI TWEET =====
def monitor():
    while True:
        for user in TWITTER_USERS:
            tweet_id, content, link = scrape_latest_tweet(user)
            if tweet_id and last_tweet_ids.get(user) != tweet_id:
                last_tweet_ids[user] = tweet_id
                msg = f"🧠 @{user} vừa tweet:\n\n{content}\n\n🔗 {link}"
                send_telegram_message(msg)
        time.sleep(60)

# ===== KEEP ALIVE (Render cần) =====
app = Flask('')

@app.route('/')
def home():
    return "✅ Bot đang chạy bằng snscrape!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    Thread(target=run).start()

# ===== CHẠY BOT =====
if __name__ == '__main__':
    keep_alive()
    Thread(target=monitor).start()
