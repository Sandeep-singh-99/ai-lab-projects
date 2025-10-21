import feedparser

def get_news(feed_url, limit=5):
    feeds = feedparser.parse(feed_url)
    new_items = []
    for entry in feeds.entries[:limit]:
        new_items.append({
            'title': entry.title,
            'link': entry.link,
            'summary': entry.summary
        })
    return new_items

if __name__ == "__main__":
    feed_url = "https://news.google.com/rss"
    news_items = get_news(feed_url)
    for item in news_items:
        print(f"Title: {item['title']}")
        print(f"Link: {item['link']}")
        print(f"Summary: {item['summary']}\n")