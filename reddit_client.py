import praw
from .config import Settings

def create_reddit(settings: Settings) -> praw.Reddit:
    reddit = praw.Reddit(
        client_id=settings.client_id,
        client_secret=settings.client_secret,
        username=settings.username,
        password=settings.password,
        user_agent=settings.user_agent,
    )
    # Touch an endpoint to validate creds early
    _ = reddit.user.me()
    return reddit
