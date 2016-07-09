import re
import logging

from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider

from py_quick_crawlers.utils.general import URLUtils
from py_quick_crawlers.generic.items import FileDownloadItem
from py_quick_crawlers.generic.spiders.base import Spider as BaseSpider


LOG = logging.getLogger(__name__)

class Spider(BaseSpider):
    # overrides
    name = 'content_download'
    rules = (Rule(LinkExtractor(deny_extensions=()), callback='parse_item', follow=True),)

    def __init__(self, *args, **kwargs):
        super(Spider, self).__init__()

        try:
            self.allowed_domains = [ kwargs.get('domain', None) or args[0] ]
            self.start_urls = [ kwargs.get('start_url', None) or args[1] ]
            self.max_depth = kwargs.get('max_depth', None) or args[2]
            self.pattern_list = kwargs.get('pattern_list', None) or args[3]
        except (KeyError, IndexError):
            raise CloseSpider(reason='Expecting 4 mandatory params - ' \
                '<domain>, <start_url>, <max_depth>, <pattern_list>')

        LOG.info('START URL: %s ; ALLOWED DOMAIN: %s' \
            %(self.start_urls[0], self.allowed_domains[0]))

    def parse_item(self, response):
        item = None

        # yield the item only if it passes through the pattern_list filter
        for pattern in self.pattern_list:
            if re.match(pattern, URLUtils.get_file_name(response.url)):
                item = FileDownloadItem(file_urls=[response.url])
                break

        if item:
            LOG.debug('URL Pattern Match: %s' %response.url)
            yield item
        else:
            LOG.debug('URL Skip: %s' %response.url)

