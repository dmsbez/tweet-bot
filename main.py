import time, os
import snscrape.modules.twitter as sntwitter
import requests
from flask import Flask
from threading import Thread

TELEGRAM_TOKEN = '7970022703:AAEFU0v_402lujK3-FHkP6xW0NXKeteco3U'
TELEGRAM_CHAT_ID = '-1001875640464'
TWITTER_USERS = ['elonmusk', 'cz_binance', 'JnP6900erc', 'VitalikButerin']
last_tweet_ids = {}

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    try:
        requests.post(url, data={'chat_id': TELEGRAM_CHAT_ID, 'text': message})
    except Exception as e:
        print("❌ Lỗi gửi Telegram:", e)

def get_latest_tweet(user):
    try:
        for tweet in sntwitter.TwitterUserScraper(user).get_items():
            return tweet.id, tweet.content, tweet.url
    except Exception as e:
        print(f"❌ Lỗi lấy tweet từ @{user}: {e}")
    return None, None, None

def monitor():
    while True:
        for user in TWITTER_USERS:
            tweet_id, content, url = get_latest_tweet(user)
            if tweet_id and last_tweet_ids.get(user) != tweet_id:
                last_tweet_ids[user] = tweet_id
                msg = f"🧠 @{user} vừa tweet:\n\n{content}\n\n🔗 {url}"
                send_telegram_message(msg)
                print(f"✅ Gửi tweet từ @{user}")
        time.sleep(30)

# Flask keep-alive
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Bot Twitter Telegram đang chạy!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    Thread(target=run).start()

if __name__ == '__main__':
    keep_alive()
    Thread(target=monitor).start()
