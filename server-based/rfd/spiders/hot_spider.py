# -*- coding: utf-8 -*-
import scrapy, locale, re
from rfd.items import RfdItem
from datetime import datetime

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

urls_default = [
    'http://forums.redflagdeals.com/hot-deals-f9/',
    'http://forums.redflagdeals.com/hot-deals-f9/2/',
    'http://forums.redflagdeals.com/hot-deals-f9/3/',
    'http://forums.redflagdeals.com/hot-deals-f9/4/',
    'http://forums.redflagdeals.com/hot-deals-f9/5/',
    'http://forums.redflagdeals.com/hot-deals-f9/6/',
    'http://forums.redflagdeals.com/hot-deals-f9/7/',
    'http://forums.redflagdeals.com/hot-deals-f9/8/',
    'http://forums.redflagdeals.com/hot-deals-f9/9/',
    'http://forums.redflagdeals.com/hot-deals-f9/10/',
]


class HotSpider(scrapy.Spider):
    name = "hot"
    # http://forums.redflagdeals.com/hot-deals-f9/
    allowed_domains = ["forums.redflagdeals.com"]
    start_urls = urls_default

    def parse(self, response):
        for sel in response.xpath('//ol[@class="threads"]').xpath('li'):
            try:
                item = RfdItem()
                title = sel.xpath('.//a[@class="title"]')
                item['title'] = title.xpath('text()').extract()[0]
                item['link'] = title.xpath('@href').extract()[0]

                nums = sel.xpath('div/div[contains(@class, "threadstats")]')
                replies = nums[0].xpath('.//a/text()')[0].extract()
                # replies = "0" if "-" else replies
                try:
                    item['replies'] = locale.atoi(replies)
                except:
                    item['replies'] = 0

                views = nums[1].xpath('.//text()')[0].extract().strip()
                # views = "0" if "-" else views
                try:
                    item['views'] = locale.atoi(views)
                except:
                    item['views'] = 0

                if item['views'] == 0 and item['replies'] == 0:
                    continue

                str_time = sel.xpath('.//div[@class="author"]').xpath('.//a/@title').extract()[0].split("on ")[1]
                str_time = re.sub(r"(st|nd|rd|th),", ",", str_time)
                item['started'] = datetime.strptime(str_time, '%b %d, %Y %I:%M %p')
                yield item
            except:
                print "Failed Parsing:", sel.extract()
