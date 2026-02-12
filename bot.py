import time
from reddit_client import get_reddit_instance
from config import TARGET_SUBREDDITS
from moderation import process_item

def run():
    reddit = get_reddit_instance()
    
    for subreddit_name in TARGET_SUBREDDITS:
        subreddit = reddit.subreddit(subreddit_name.strip())
        print(f"Monitoring subreddit: {subreddit.display_name}")
        
        for submission in subreddit.stream.submissions(skip_existing=True):
            process_item(submission)
        
        for comment in subreddit.stream.comments(skip_existing=True):
            process_item(comment)

if __name__ == "__main__":
    while True:
        try:
            run()
        except Exception as e:
            print(f"Error occurred: {e}")
            time.sleep(10)
