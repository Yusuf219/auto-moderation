from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import praw
from praw.models import Submission, Comment

@dataclass(frozen=True)
class Decision:
    action: str  # "approve" | "remove"
    reason: Optional[str] = None

def _contains_keyword(text: str, keywords: list[str]) -> Optional[str]:
    t = (text or "").lower()
    for kw in keywords:
        if kw and kw in t:
            return kw
    return None

def _contains_domain(text: str, domains: list[str]) -> Optional[str]:
    t = (text or "").lower()
    for d in domains:
        if not d:
            continue
        # simple domain match (improve later)
        if d in t:
            return d
    return None

def decide_for_submission(sub: Submission, filtered_keywords: list[str], filtered_domains: list[str]) -> Decision:
    blob = f"{sub.title or ''}\n{sub.selftext or ''}"
    hit_kw = _contains_keyword(blob, filtered_keywords)
    if hit_kw:
        return Decision("remove", f"filtered keyword: '{hit_kw}'")

    hit_dom = _contains_domain(blob, filtered_domains)
    if hit_dom:
        return Decision("remove", f"filtered domain/link: '{hit_dom}'")

    return Decision("approve")

def decide_for_comment(c: Comment, filtered_keywords: list[str], filtered_domains: list[str]) -> Decision:
    blob = c.body or ""
    hit_kw = _contains_keyword(blob, filtered_keywords)
    if hit_kw:
        return Decision("remove", f"filtered keyword: '{hit_kw}'")

    hit_dom = _contains_domain(blob, filtered_domains)
    if hit_dom:
        return Decision("remove", f"filtered domain/link: '{hit_dom}'")

    return Decision("approve")

def take_action(item, decision: Decision, bot_reply: str) -> None:
    # item.mod.approve/remove require mod permissions in that subreddit.
    if decision.action == "approve":
        item.mod.approve()
        return

    # remove + leave transparent comment
    item.mod.remove()
    try:
        item.reply(bot_reply)
    except Exception:
        # Reply may fail (locked threads, perms, rate limits). Removal still stands.
        pass
