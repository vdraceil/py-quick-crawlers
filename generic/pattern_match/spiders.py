import re
import logging

from constants import Regex
from generic.spiders import BaseSpider
from generic.items import FlexibleItem


LOG = logging.getLogger(__name__)

class PatternMatchSpider(BaseSpider):
    # overrides
    name = 'pattern_match'

    def __init__(self, *args, **kwargs):
        super(PatternMatchSpider, self).__init__()

        try:
            self.allowed_domains = [ kwargs.get('domain', None) or args[0] ]
            self.start_urls = [ kwargs.get('start_url', None) or args[1] ]
            self.max_depth = kwargs.get('max_depth', None) or args[2]
            self.pattern_dict = kwargs.get('pattern_dict', None) or args[3]
            self.out_file = kwargs.get('out_file', None) or args[4]
        except (KeyError, IndexError):
            raise CloseSpider(reason='Expecting 5 mandatory params - ' \
                '<domain>, <start_url>, <max_depth>, <pattern_dict>, <out_file>')

        LOG.info('START URL: %s ; ALLOWED DOMAIN: %s' \
            %(self.start_urls[0], self.allowed_domains[0]))

    def parse_item(self, response):
        content = self.get_content(response)

        # try to match up for the given pattern_dict
        hasMatch = False
        item = FlexibleItem()
        for fieldName, pattern in self.pattern_dict.iteritems():
            item[fieldName] = re.findall(pattern, content)
            if not hasMatch and len(item[fieldName]):
                hasMatch = True

        # yield the item only if we have atleast one field match
        if hasMatch:
            yield item
