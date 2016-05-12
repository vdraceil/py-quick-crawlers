import os
import logging

from billiard import Process
from twisted.internet import reactor
from scrapy import log
from scrapy import signals
from scrapy.crawler import Crawler
from scrapy.utils.project import get_project_settings

from constants import Regex
from utils.general import URLUtils


LOG = logging.getLogger(__name__)

class SpiderController(object):
    def contact_info_crawl(self, website_list, out_file):
        from generic.contacts.spiders import ContactInfoSpider

        # set env variable so that scrapy knows what custom settings to load
        os.environ['SCRAPY_SETTINGS_MODULE'] = 'generic.contacts.settings'

        class ScrapyCrawler(Process):
            def __init__(self, spider):
                super(ScrapyCrawler, self).__init__()
                self.crawler = Crawler(settings)
                self.crawler.configure()
                self.crawler.signals.connect(reactor.stop,
                                             signal=signals.spider_closed)
                self.spider = spider

            def run(self):
                self.crawler.crawl(self.spider)
                self.crawler.start()
                # blocks till the spider finishes execution
                reactor.run()

        def run_spider(domain, start_url, max_depth):
            spider = ContactInfoSpider(domain, start_url, max_depth, out_file)
            crawler = ScrapyCrawler(spider)
            crawler.start()
            crawler.join()

        def validate_args():
            settings = get_project_settings()

            # overall parameter check - basic
            if not isinstance(website_list, list):
                raise InvalidArgumentError('Args "website_list"' \
                                        ' should be a list of tuples')
            if len(website_list) == 0:
                raise InvalidArgumentError('Args "website_list"' \
                                        ' should have at least one element')

            for item in website_list:
                # base type check
                if not isinstance(item, tuple) or len(item) != 2:
                    raise InvalidArgumentError('All elements of "website_list"' \
                        ' are expected to be tuples of size 2 - ' \
                        '(<url>, <depth>')
                url, depth = item

                # sub-parameter type checks
                type_check = isinstance(url, basestring) and isinstance(depth, int)
                if not type_check:
                    raise InvalidArgumentError('Args type check failed. ' \
                        'Expected - str,int. Given - "%s"'
                        %(','.join((str(type(x) for x in item)))))

                # sub-parameter value checks
                match = Regex.PT_DOMAIN_FROM_URL.match(url)
                if not match:
                    raise InvalidArgumentError('Invalid URL - "%s"' % url)

                if depth <= 0:
                    raise InvalidArgumentError('Depth parameter should ' \
                                            'be strictly greater than 0')

        LOG.debug('crawl API Start - Params - website_list=%s' %(website_list))
        validate_args()
        parent = self
        settings = get_project_settings()

        for item in website_list:
            spider_args = {
                'domain': URLUtils.get_domain_from_url(item[0]),
                'start_url': URLUtils.get_complete_url(item[0]),
                'max_depth': item[1],
            }

            # according to Scrapy the current page is at a depth 0
            # but for this project the current page is at depth 1
            # so, adjust the input depth accordingly
            spider_args['max_depth'] -= 1

            # kick off the scrapy crawler
            LOG.debug('Kicking off Scrapy Spider - %s' %spider_args)
            run_spider(**spider_args)


class InvalidArgumentError(Exception): pass
