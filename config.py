import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
USERNAME = os.getenv("REDDIT_USERNAME")
PASSWORD = os.getenv("REDDIT_PASSWORD")
USER_AGENT = os.getenv("REDDIT_USER_AGENT")

TARGET_SUBREDDITS = os.getenv("TARGET_SUBREDDITS", "test").split(",")

FILTERED_KEYWORDS = [
    "spamlink.com",
    "buy now",
    "promo code",
    "http",
    "https"
]
