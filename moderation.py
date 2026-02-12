from config import FILTERED_KEYWORDS

def contains_filtered_content(text: str) -> bool:
    if not text:
        return False
    
    lower_text = text.lower()
    for keyword in FILTERED_KEYWORDS:
        if keyword.lower() in lower_text:
            return True
    
    return False


def process_item(item):
    content = ""
    
    if hasattr(item, "title"):
        content += item.title + " "
    if hasattr(item, "selftext"):
        content += item.selftext
    if hasattr(item, "body"):
        content += item.body

    if contains_filtered_content(content):
        item.mod.remove()
        item.reply(
            "Hello, I am a moderator bot. Your submission was removed because it "
            "contains restricted keywords or links. Please review the subreddit rules."
        )
        print(f"Removed item: {item.id}")
    else:
        item.mod.approve()
        print(f"Approved item: {item.id}")
