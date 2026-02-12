import praw
from config import CLIENT_ID, CLIENT_SECRET, USERNAME, PASSWORD, USER_AGENT

def get_reddit_instance():
    return praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        username=USERNAME,
        password=PASSWORD,
        user_agent=USER_AGENT,
    )
