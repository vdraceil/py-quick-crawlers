import re
import logging

from scrapy.exceptions import CloseSpider

from py_quick_crawlers.generic.items import FlexibleItem
from py_quick_crawlers.generic.spiders.base import Spider as BaseSpider


LOG = logging.getLogger(__name__)

class Spider(BaseSpider):
    # overrides
    name = 'pattern_match'

    def __init__(self, *args, **kwargs):
        super(Spider, self).__init__()

        try:
            self.allowed_domains = [ kwargs.get('domain', None) or args[0] ]
            self.start_urls = [ kwargs.get('start_url', None) or args[1] ]
            self.max_depth = kwargs.get('max_depth', None) or args[2]
            self.pattern_dict = kwargs.get('pattern_dict', None) or args[3]
        except (KeyError, IndexError):
            raise CloseSpider(reason='Expecting 4 mandatory params - ' \
                '<domain>, <start_url>, <max_depth>, <pattern_dict>')

        LOG.info('START URL: %s ; ALLOWED DOMAIN: %s' \
            %(self.start_urls[0], self.allowed_domains[0]))

    def parse_item(self, response):
        content = self.get_content(response)

        item = FlexibleItem()
        item['url'] = response.url

        # try to match up for the given pattern_dict
        hasMatch = False
        for fieldName, pattern in self.pattern_dict.iteritems():
            item[fieldName] = re.findall(pattern, content)
            if not hasMatch and len(item[fieldName]):
                hasMatch = True

        # yield the item only if we have atleast one field match
        if hasMatch:
            yield item
