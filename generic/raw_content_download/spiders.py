import re
import logging

from scrapy.exceptions import CloseSpider
from generic.spiders import BaseSpider
from generic.raw_content_download.items import ContentInfoItem


LOG = logging.getLogger(__name__)

class RawContentDownloadSpider(BaseSpider):
    # overrides
    name = 'raw_content_download'

    def __init__(self, *args, **kwargs):
        super(RawContentDownloadSpider, self).__init__()

        try:
            self.allowed_domains = [ kwargs.get('domain', None) or args[0] ]
            self.start_urls = [ kwargs.get('start_url', None) or args[1] ]
            self.max_depth = kwargs.get('max_depth', None) or args[2]
            self.file_pattern = kwargs.get('file_pattern', None) or args[3]
            self.out_dir = kwargs.get('out_dir', None) or args[4]
        except (KeyError, IndexError):
            raise CloseSpider(reason='Expecting 5 mandatory params - ' \
                '<domain>, <start_url>, <max_depth>, <file_pattern>, <out_dir>')

        LOG.info('START URL: %s ; ALLOWED DOMAIN: %s' \
            %(self.start_urls[0], self.allowed_domains[0]))

    def parse_item(self, response):
        content = self.get_raw_content(response)

        item = ContentInfoItem(url=response.url, content=content)
        yield item
