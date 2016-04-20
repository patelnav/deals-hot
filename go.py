import json
from datetime import datetime
from math import log
from os import path, remove


from scrapy.crawler import CrawlerProcess
from rfd.spiders.hot_spider import HotSpider

JSON_FILE = 'result.json'
HTML_FILE = 'result.html'

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'FEED_FORMAT': 'json',
    'FEED_URI': JSON_FILE
})

if path.isfile(JSON_FILE):
    print 'DELETING OLD JSON FILE'
    remove(JSON_FILE)


process.crawl(HotSpider)
process.start()

# from pprint import pprint

with open(JSON_FILE) as data_file:
    data = json.load(data_file)

# pprint(data)

for d in data:
    # 2016-04-19 21:53:00
    dt = datetime.strptime(d['started'], '%Y-%m-%d %H:%M:%S')
    seconds = (datetime.now() - dt).total_seconds()
    d['seconds'] = seconds
    hits = d['views'] + (d['replies'] * 100)

    log_score = log(max(abs(hits), 1), 10)
    d['score'] = round(log_score - (seconds / 45000), 7)
    # d['score'] = round(log_score - (seconds / 100000), 7)
    # print "Score:", d['score'], "Hits:", hits, "Seconds:", seconds, d['title']


if path.isfile(HTML_FILE):
    print 'DELETING OLD HTML FILE'
    remove(HTML_FILE)

with open(HTML_FILE, 'w') as f:
    f.write('<html><head></head><body><ol>\n')

    for d in sorted(data, key=lambda d: -d['score']):
        f.write('<li>Views: {}, Replies: {} <a href="http://forums.redflagdeals.com/{}">{}</a></li>\n'.format(d['views'], d['replies'], d['link'], d['title'].encode('ascii', 'ignore')))
        # print "Score:", d['score'], "Hits:", (d['views'] + (d['replies'] * 100)), "Seconds:", d['seconds'], d['title']

    f.write('</ol></body></html>')
