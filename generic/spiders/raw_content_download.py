import re
import logging

from scrapy.exceptions import CloseSpider
from generic.items import FileDownloadItem
from generic.spiders.base import Spider as BaseSpider

from utils.general import URLUtils


LOG = logging.getLogger(__name__)

class Spider(BaseSpider):
    # overrides
    name = 'raw_content_download'

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
        # yield the item only if it passes through the pattern_list filter
        for pattern in self.pattern_list:
            if re.match(pattern, URLUtils.get_file_name(response.url)):
                item = FileDownloadItem(file_urls=[response.url])
                yield item
