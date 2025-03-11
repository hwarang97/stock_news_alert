import os
from datetime import date
from datetime import timedelta
from dotenv import load_dotenv
from newsapi import NewsApiClient
from smtplib import SMTP
from email.message import EmailMessage
import requests
import sys


load_dotenv()

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
THRESHOLD = 0.05

# DATE AUTO
yesterday = date.today() - timedelta(days=2)
while yesterday.weekday() not in (0, 1, 2, 3, 4):
    yesterday -= timedelta(days=1)
YESTERDAY = str(yesterday)

before_yesterday = yesterday - timedelta(days=1)
while before_yesterday.weekday() not in (0, 1, 2, 3, 4):
    before_yesterday -= timedelta(days=1)
BEFORE_YESTERDAY = str(before_yesterday)

newsapi = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))

POLYGON_APIKEY = os.getenv("POLYGON_API_KEY")
PARAMS = {
    "apiKey": POLYGON_APIKEY,
    "adjusted": True,
}

GOOGLE_SENDER = os.getenv("GOOGLE_SENDER")
GOOGLE_PASSWORD = os.getenv("GOOGLE_SENDER_PASSWORD")
GOOGLE_RECEIVER = os.getenv("GOOGLE_RECEIVER")

NUM_ARTICLE = 3

# price
yesterday_price = (
    requests.get(
        url=f"https://api.polygon.io/v1/open-close/{STOCK}/{YESTERDAY}", params=PARAMS
    )
    .json()
    .get("close")
)
before_yesterday_price = (
    requests.get(
        url=f"https://api.polygon.io/v1/open-close/{STOCK}/{BEFORE_YESTERDAY}",
        params=PARAMS,
    )
    .json()
    .get("close")
)

try:
    difference = round(
        (yesterday_price - before_yesterday_price) / before_yesterday_price * 100, 2
    )
except TypeError as e:
    print(
        f"Something is wrong with price - yesterday: {yesterday_price}, before_yesterday: {before_yesterday_price}",
        e,
    )
    sys.exit(1)

# bound
if abs(difference) >= THRESHOLD:
    all_articles = newsapi.get_everything(
        q="tesla", language="en", page_size=NUM_ARTICLE, page=1
    )

    # contents
    if difference >= 0:
        up_down_percent = f"🔺{difference}%"
    else:
        up_down_percent = f"🔻{difference}%"

    contents = f"{STOCK}: {up_down_percent}"
    for article in all_articles.get("articles"):
        title = article.get("title")
        description = article.get("description")
        contents += f"\nHeadline: {title}\nBrief: {description}\n\n"

    # transfer
    message = EmailMessage()
    message.set_content(contents)
    connection = SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(GOOGLE_SENDER, GOOGLE_PASSWORD)
    connection.send_message(
        from_addr=GOOGLE_SENDER, to_addrs=GOOGLE_RECEIVER, msg=message
    )
    connection.quit()
