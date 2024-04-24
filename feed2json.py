import json
import feedparser


def feed2json(feed_file_path: str = None, feed_url: str = None, feed_string: str = None) -> dict:
    if feed_file_path or feed_url or feed_string is None:
        raise ValueError("Must provide one of feed_file_path, feed_url, or feed_string")

    feed = None
    if feed_file_path:
        feed = feedparser.parse(feed_file_path)
    elif feed_url:
        feed = feedparser.parse(feed_url)
    elif feed_string:
        feed = feedparser.parse(feed_string)

    if not feed:
        raise ValueError("No feed provided")

    json_feed = {
        "version": "https://jsonfeed.org/version/1.1",
        "title": feed.feed.title,
        "feed_url": feed.feed.id,
        "home_page_url": feed.feed.get("link", None)
    }

    if hasattr(feed.feed, "subtitle"):
        json_feed["description"] = feed.feed.subtitle
    if hasattr(feed.feed, "updated"):
        json_feed["updated"] = feed.feed.updated

    json_feed["items"] = []
    for entry in feed.entries:
        item = {
            "id": entry.id,
            "url": entry.link,
            "title": entry.title,
        }
        if hasattr(entry, "summary"):
            item["content_html"] = entry.summary
        if hasattr(entry, "published"):
            item["date_published"] = entry.published
        if hasattr(entry, "updated"):
            item["date_modified"] = entry.updated
        if hasattr(entry, "author"):
            authors = entry.author
            if not isinstance(authors, list):
                authors = [authors]
            item["authors"] = [{"name": author} for author in authors]
        if hasattr(entry, "content"):
            item["content_html"] = ""
            for content in entry.content:
                if content["type"] == "text/html":
                    item["content_html"] += content["value"]
                elif content["type"] == "text/plain":
                    item["content_text"] = content["value"]

        if hasattr(entry, "categories"):
            item["tags"] = [{"name": category} for category in entry.categories]

        if hasattr(entry, "enclosures"):
            item["attachments"] = [{"url": enclosure["href"], 'length': enclosure["length"], 'type': enclosure["type"]}
                                   for enclosure in entry.enclosures]

        if hasattr(entry, "summary"):
            item["summary"] = entry.summary

        json_feed["items"].append(item)

    return json_feed
