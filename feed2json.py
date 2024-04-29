import feedparser
import time
from datetime import datetime
# https://feedparser.readthedocs.io/en/latest/reference-feed-author_detail.html
# https://www.jsonfeed.org/version/1.1/

def struct_time_to_rfc3339(struct_time):
    try:
        dt = datetime.fromtimestamp(time.mktime(struct_time)) 
        rfc3339 = dt.isoformat()
        if dt.tzinfo is None:
            rfc3339 += "Z"
    except Exception:
        rfc3339 = None
    return rfc3339

def gfnn(feed, *keys): #get first non none
    return next((feed.get(key) for key in keys if feed.get(key)), None)

def feed2json(feed_file_path: str = None, feed_url: str = None, feed_string: str = None) -> dict:
    feed_args = [feed_file_path, feed_url, feed_string]
    if not any(feed_args):
        raise ValueError("Must provide one of feed_file_path, feed_url, or feed_string")

    feed_arg = next((arg for arg in feed_args if arg), None)
    feed = feedparser.parse(feed_arg) if feed_arg else None

    if not feed.get('feed'):
        raise ValueError("No feed found")

    feed_info = feed.feed

    json_feed = {
        "version": "https://jsonfeed.org/version/1.1", #string
        "title": gfnn(feed_info, 'title', 'subtitle'), #string
        "feed_url": gfnn(feed_info, 'link', 'id'), #string
        "home_page_url": gfnn(feed_info, 'id', 'link'), #string
        "description": gfnn(feed_info, 'subtitle','info'), #string
        "icon": gfnn(feed_info, 'icon','logo'), #string
        "favicon": gfnn(feed_info, 'logo','icon'), #string
        "authors": [ #array of objects
                    {"name": feed_info.get('author_detail', {}).get('name'), #string
                     "url": gfnn(feed_info.get('author_detail', {}),'href','email'), #string
                     "avatar": None, #string
                    },
                   ],
        "language": gfnn(feed_info, 'language'), #string
        "expired": None, #boolean
        "hub": None, #array of objects
        "items": [], #array
    }

    for entry in feed.entries:
        item = {
            "id": entry.get('id'), #string
            "url": entry.get('link'), #string
            "external_url": None, #string
            "title": entry.get('title'), #string
            "content_text": None, #string
            "content_html": None, #string
            "summary": entry.get('summary'), #string
            "image": None, #url string
            "banner_image": None, #url string
            "date_published": struct_time_to_rfc3339(entry.get('published_parsed')),#string RFC 3339 format: 2010-02-07T14:04:00-05:00.
            "date_modified": struct_time_to_rfc3339(entry.get('updated_parsed')),#string RFC 3339 format: 2010-02-07T14:04:00-05:00.
            "authors": [entry.get('author'),], #array of objects
            "tags": [tag['label'] for tag in entry.get('tags', []) if tag], #array of objects
            "language": None, #string
            "attachments": [ #array of objects
                            '''
                            {"url": string, 
                            'mime_type': string, 
                            'title': strinrg,
                            'size_in_bytes': int,
                            'duration_in_seconds': int
                            '''
                           ],
            }

        if len(entry.get('content',[])) > 0:
            item["content_html"] = ""
            item["content_text"] = ""
            for content in entry['content']:
                if content["type"] == "text/plain":
                    item["content_text"] += content["value"]
                else:
                    item["content_html"] += content["value"]

        if hasattr(entry, "enclosures"):
            item["attachments"] = [{"url": enclosure["href"], 
                                    'size_in_bytes': int(enclosure["length"]), 
                                    'mime_type': enclosure["type"]}
                                   for enclosure in entry.enclosures]

        json_feed["items"].append(item)

    return json_feed