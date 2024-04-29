## Feed2Json

Convert RSS feed to JSON Feed

Installation
-----------
`pip install feed2json`

Usage
-----------
```python
from feed2json import feed2json
# ----------- 
feed_url = "https://versun.me/feed"
json_feed:dict = feed2json(feed_url)
# ----------- 
feed_html = '''
   <?xml version="1.0" encoding="utf-8"?>
   <feed xmlns="http://www.w3.org/2005/Atom">

     <title>Example Feed</title>
     <link href="http://example.org/"/>
     <updated>2003-12-13T18:30:02Z</updated>
     <author>
       <name>John Doe</name>
     </author>
     <id>urn:uuid:60a76c80-d399-11d9-b93C-0003939e0af6</id>

     <entry>
       <title>Atom-Powered Robots Run Amok</title>
       <link href="http://example.org/2003/12/13/atom03"/>
       <id>urn:uuid:1225c695-cfb8-4ebb-aaaa-80da344efa6a</id>
       <updated>2003-12-13T18:30:02Z</updated>
       <summary>Some text.</summary>
     </entry>

   </feed>
'''
json_feed:dict = feed2json(feed_html)
# ----------- 
feed_xml_file = 'example_feed.xml'
json_feed:dict = feed2json(feed_xml_file)
```
