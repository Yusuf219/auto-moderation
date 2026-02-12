from __future__ import annotations

import logging
import time
from threading import Thread

from praw.models import Comment, Submission

from .config import load_settings
from .reddit_client import create_reddit
from .moderation import (
    decide_for_comment,
    decide_for_submission,
    take_action,
)
from .logging_utils import setup_logging

log = logging.getLogger("mod-assistant")

BOT_REPLY_TEMPLATE = (
    "Hi — I’m an automated moderation bot used by this subreddit’s moderators.\n\n"
    "Your post/comment was removed because it matched a configured filter ({reason}). "
    "Please review the subreddit rules and try again.\n\n"
    "*If you believe this was a mistake, please contact the moderators.*"
)

def handle_submission(sub: Submission, filtered_keywords: list[str], filtered_domains: list[str]) -> None:
    decision = decide_for_submission(sub, filtered_keywords, filtered_domains)
    if decision.action == "remove":
        take_action(sub, decision, BOT_REPLY_TEMPLATE.format(reason=decision.reason), settings.dry_run)
        log.info("Removed submission %s in r/%s (%s)", sub.id, sub.subreddit.display_name, decision.reason)
    else:
        sub.mod.approve()
        log.info("Approved submission %s in r/%s", sub.id, sub.subreddit.display_name)

def handle_comment(c: Comment, filtered_keywords: list[str], filtered_domains: list[str]) -> None:
    decision = decide_for_comment(c, filtered_keywords, filtered_domains)
    if decision.action == "remove":
        take_action(c, decision, BOT_REPLY_TEMPLATE.format(reason=decision.reason), settings.dry_run)
        log.info("Removed comment %s in r/%s (%s)", c.id, c.subreddit.display_name, decision.reason)
    else:
        c.mod.approve()
        log.info("Approved comment %s in r/%s", c.id, c.subreddit.display_name)

def run_streams():
    setup_logging()
    settings = load_settings()
    reddit = create_reddit(settings)

    subreddit_str = "+".join([s.strip() for s in settings.target_subreddits if s.strip()])
    subreddit = reddit.subreddit(subreddit_str)

    log.info("Logged in as u/%s", reddit.user.me())
    log.info("Monitoring: %s", subreddit_str)

    def submissions_worker():
        while True:
            try:
                for sub in subreddit.stream.submissions(skip_existing=True):
                    handle_submission(sub, settings.filtered_keywords, settings.filtered_domains)
            except Exception as e:
                log.warning("Submission stream error: %s (retrying soon)", e)
                time.sleep(5)

    def comments_worker():
        while True:
            try:
                for c in subreddit.stream.comments(skip_existing=True):
                    handle_comment(c, settings.filtered_keywords, settings.filtered_domains)
            except Exception as e:
                log.warning("Comment stream error: %s (retrying soon)", e)
                time.sleep(5)

    t1 = Thread(target=submissions_worker, daemon=True)
    t2 = Thread(target=comments_worker, daemon=True)
    t1.start()
    t2.start()

    # keep main thread alive
    while True:
        time.sleep(60)

if __name__ == "__main__":
    run_streams()
