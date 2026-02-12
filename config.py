import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

def _csv(name: str) -> list[str]:
    raw = os.getenv(name, "").strip()
    if not raw:
        return []
    return [x.strip() for x in raw.split(",") if x.strip()]

@dataclass(frozen=True)
class Settings:
    client_id: str
    client_secret: str
    username: str
    password: str
    user_agent: str

    target_subreddits: list[str]
    filtered_keywords: list[str]
    filtered_domains: list[str]

def load_settings() -> Settings:
    required = ["REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET", "REDDIT_USERNAME", "REDDIT_PASSWORD", "REDDIT_USER_AGENT"]
    missing = [k for k in required if not os.getenv(k)]
    if missing:
        raise RuntimeError(f"Missing required env vars: {', '.join(missing)}")

    subs = _csv("TARGET_SUBREDDITS")
    if not subs:
        raise RuntimeError("TARGET_SUBREDDITS must include at least one subreddit (comma-separated).")

    return Settings(
        client_id=os.environ["REDDIT_CLIENT_ID"],
        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        username=os.environ["REDDIT_USERNAME"],
        password=os.environ["REDDIT_PASSWORD"],
        user_agent=os.environ["REDDIT_USER_AGENT"],
        target_subreddits=subs,
        filtered_keywords=[k.lower() for k in _csv("FILTERED_KEYWORDS")],
        filtered_domains=[d.lower() for d in _csv("FILTERED_DOMAINS")],
    )
