import requests, time, feedparser
from flask import Flask
from threading import Thread

TELEGRAM_TOKEN = '7970022703:AAEFU0v_402lujK3-FHkP6xW0NXKeteco3U'
TELEGRAM_CHAT_ID = '6921514427'  # ✅ test bằng cá nhân trước

TWITTER_USERS = ['elonmusk', 'cz_binance', 'VitalikButerin', 'JnP6900erc']

last_tweets = {}

def send_telegram_message(message):
    print("🛫 Gửi đến Telegram:", message)
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    try:
        r = requests.post(url, data={'chat_id': TELEGRAM_CHAT_ID, 'text': message})
        print("📬 Kết quả gửi:", r.status_code, r.text)
    except Exception as e:
        print("❌ Gửi lỗi:", e)

app = Flask('')

@app.route('/')
def home():
    return "Bot đang hoạt động!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    Thread(target=run).start()

def check_tweets():
    while True:
        for user in TWITTER_USERS:
            print(f"🔍 Đang check {user}...")
            try:
                feed = feedparser.parse(f'https://nitter.privacydev.net/{user}/rss')
                if not feed.entries:
                    print(f"⚠️ Không lấy được tweet từ {user}")
                    continue
                latest = feed.entries[0]
                if last_tweets.get(user) != latest.id:
                    last_tweets[user] = latest.id
                    message = f"🧠 {user} vừa tweet:\n\n{latest.title}\n\n🔗 {latest.link}"
                    send_telegram_message(message)
                    print(f"✅ Đã gửi tweet mới từ {user}")
            except Exception as e:
                print(f"❌ Lỗi khi check {user}: {e}")
        time.sleep(30)

if __name__ == '__main__':
    keep_alive()
    Thread(target=check_tweets).start()
