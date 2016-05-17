import re
import logging
import lxml.etree
import xml.sax.saxutils as SAXUtils

from scrapy.exceptions import CloseSpider
from scrapy.contrib.spiders import Rule
from scrapy.contrib.spiders import CrawlSpider
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http.response.html import HtmlResponse

from constants import Regex
from generic.contacts.items import FlexibleItem


LOG = logging.getLogger(__name__)

class ContactInfoSpider(CrawlSpider):
    # constants
    UNWANTED_HTML_ELEMENTS = ['script', 'noscript', 'style', 'link', 'head']
    UTF8_HTML_PARSER = lxml.etree.HTMLParser(encoding='utf-8')

    # overrides
    name = 'contacts'
    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
        Rule(SgmlLinkExtractor(), callback='parse_item', follow=True)
    )

    def __init__(self, *args, **kwargs):
        super(ContactInfoSpider, self).__init__()

        try:
            self.allowed_domains = [ kwargs.get('domain', None) or args[0] ]
            self.start_urls = [ kwargs.get('start_url', None) or args[1] ]
            self.max_depth = kwargs.get('max_depth', None) or args[2]
            self.out_file = kwargs.get('out_file', None) or args[3]
        except (KeyError, IndexError):
            raise CloseSpider(reason='Expecting 4 mandatory params - ' \
                '<domain>, <start_url>, <max_depth>, <out_file>')

        LOG.info('START URL: %s ; ALLOWED DOMAIN: %s' \
            %(self.start_urls[0], self.allowed_domains[0]))

    def parse_start_url(self, response):
        return self.parse_item(response);

    def parse_item(self, response):
        # adjust depth for this project which starts at 1
        current_page_depth = response.meta.get('depth', 0) + 1

        LOG.debug('DEPTH:%s - URL:%s - Status:%s - ResponseType:%s'
                  %(current_page_depth, response.url,
                    response.status, response.__class__.__name__))

        # skip pages which do not yield proper HTML responses
        if response.status >= 400 and not isinstance(response, HtmlResponse):
            return

        # HACK: depth=0 in Scrapy implies an infinite crawl
        # since we will not be interested in infinite crawls, this quick dirty
        # hack enables us to crawl just the current page contents
        # TODO: Find an alternate way in which we do not even crawl all pages at
        # depth=1
        if self.max_depth == 0 and current_page_depth > 1:
            return

        # remove any non-printable characters
        # messes up the HTML parsing sometimes (when tags have unicode chars)
        content = response.body_as_unicode()
        content = Regex.PT_NON_PRINTABLE_CHARS.sub('', content)
        content = content.encode('utf-8')

        # extract plain text from the response body/html
        # make a tree from the page's html content and strip irrelevant tags
        try:
            root = lxml.etree.fromstring(content,
                                         parser=ContactInfoSpider.UTF8_HTML_PARSER)
            lxml.etree.strip_elements(root, lxml.etree.Comment,
                                    *ContactInfoSpider.UNWANTED_HTML_ELEMENTS)
        except lxml.etree.XMLSyntaxError:
            return

        # method="text" works okay, but it fails to add whitespaces between
        # consecutive div tags, br tags etc., thereby making some words
        # unrecogonizable - we need exact individual words
        try:
            content = lxml.etree.tostring(root, method="html",
                                         encoding="unicode")
        except lxml.etree.SerialisationError:
            # there is no point in proceeding further without a proper content
            # skip processing this page
            return

        # convert the unicode object to a string
        content = content.encode('utf-8')

        # remove all html tags
        content = Regex.PT_HTML_TAGS.sub(' ', content)

        # strip out unnecessary white spaces
        # split and join is about 3x faster than using compiled regexes
        content = ' '.join(content.split())

        # unescape HTML entities
        content = SAXUtils.unescape(content)

        # try to match up for the contacts info
        emails = re.findall(Regex.PT_EMAIL, content)
        # TODO: add patterns for phone & fax and try to match them too

        item = FlexibleItem()
        for email in emails:
            item['email'] = email
            yield item
