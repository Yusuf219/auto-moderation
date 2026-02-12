# Reddit Moderation Assistant Bot

A moderator-only automation tool that assists subreddit moderators by:

- Automatically approving safe posts and comments
- Removing content that contains restricted keywords or links
- Leaving transparent bot feedback comments
- Operating only in authorized subreddits

## Proposed Features

- Keyword filtering
- Link filtering
- Transparent bot identity
- No long-term data storage
- Rate-limit compliant
- Moderator permission required

## Compliance & Platform Policy Alignment

This bot is designed to align with Reddit’s API and moderation policies:

- Operates only in subreddits where the bot account has moderator permissions
- Performs automated moderation actions only (approve/remove)
- Does not automate engagement (no voting, no commenting outside moderation context)
- Does not send private messages
- Does not scrape or export Reddit data
- Does not store data long-term
- Processes content in-memory only (no long-term storage)
- Respects Reddit API rate limits
- Clearly identifies itself as a bot in removal comments

The bot is intended as a moderation assistant and does not operate as a growth, marketing, or engagement automation tool.

## Status

- v0.0.2
