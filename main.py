import requests, time, feedparser
from flask import Flask
from threading import Thread

TELEGRAM_TOKEN = '7970022703:AAEFU0v_402lujK3-FHkP6xW0NXKeteco3U'
TELEGRAM_CHAT_ID = '-1001875640464'
TWITTER_USERS = ['elonmusk', 'cz_binance', 'VitalikButerin', 'JnP6900erc']

last_tweets = {}

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    requests.post(url, data={'chat_id': TELEGRAM_CHAT_ID, 'text': message})

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
            feed = feedparser.parse(f'https://nitter.privacydev.net/{user}/rss')
            if feed.entries:
                latest = feed.entries[0]
                if last_tweets.get(user) != latest.id:
                    last_tweets[user] = latest.id
                    send_telegram_message(f"🧠 {user} vừa tweet:\n\n{latest.title}\n\n🔗 {latest.link}")
        time.sleep(30)

if __name__ == '__main__':
    keep_alive()
    Thread(target=check_tweets).start()
