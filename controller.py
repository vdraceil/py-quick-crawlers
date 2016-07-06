import re
import os
import logging

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from utils.general import URLUtils
from utils.general import ShellUtils
from constants import Regex, SpiderSettingOverrides
from generic.spiders.pattern_match import Spider as PatternMatchSpider
from generic.spiders.raw_content_download import Spider as RawContentDownloadSpider


LOG = logging.getLogger(__name__)
# disable all Scrapy logs
logging.getLogger('scrapy').propagate = False

class SpiderController(object):
    SETTINGS = get_project_settings()

    def pattern_match_crawl(self, target, pattern_dict,
                            out_file=None):
        def validate_args():
            self._validate_target(target)

            for key,value in pattern_dict.iteritems():
                type_check = isinstance(key, basestring) and \
                    isinstance(value, re._pattern_type)
                if not type_check:
                    raise InvalidArgumentError('Args type check failed. ' \
                        'For "pattern_dict" ' \
                        'Expected - str, regex. Given - "%s"'
                        %(str(type(key)) + ',' + str(type(value))))

        LOG.debug('pattern_match_crawl API Start - Params - '
                  'target=%s ; pattern_dict=%s ; out_file=%s'
                  %(target, pattern_dict, out_file))

        # check args before proceeding
        validate_args()

        # customize settings
        SpiderController.SETTINGS.set('ITEM_PIPELINES',
            SpiderSettingOverrides.PATTERN_MATCH['ITEM_PIPELINES'])
        SpiderController.SETTINGS.set('OUT_FILE', out_file)

        # initiate CrawlerProcess
        process = CrawlerProcess(SpiderController.SETTINGS)

        for item in target:
            spider_args = {
                'domain': URLUtils.get_domain(item[0]),
                'start_url': URLUtils.reform(item[0]),
                'max_depth': item[1],
                'pattern_dict': pattern_dict
            }

            # according to Scrapy the current page is at a depth 0
            # but for this project the current page is at depth 1
            # so, adjust the input depth accordingly
            spider_args['max_depth'] -= 1

            # kick off the scrapy crawler
            LOG.debug('Kicking off Scrapy Spider - %s' %spider_args)
            process.crawl(PatternMatchSpider, **spider_args)
        process.start() # blocks here until all crawling is done


    def content_download_crawl(self, target, pattern_list,
                               out_dir=None):
        def validate_args():
            self._validate_target(target)

            if not isinstance(pattern_list, list) and \
            not isinstance(pattern_list, tuple):
                raise InvalidArgumentError('Arg "pattern_list" should be a '
                                           'list or a tuple')

            for pattern in pattern_list:
                if not isinstance(pattern, re._pattern_type):
                    raise InvalidArgumentError('Each item of "pattern_list" '
                        'should be a valid compiled regex')

        LOG.debug('content_download_crawl API Start - Params - '
                  'target=%s ; pattern_list=%s ; out_dir=%s'
                  %(target, pattern_list, out_dir))

        # check args before proceeding
        validate_args()

        # make out_dir if it does not exist already
        out_dir and ShellUtils.mkdirp(out_dir)

        # customize settings
        SpiderController.SETTINGS.set('ITEM_PIPELINES',
            SpiderSettingOverrides.RAW_CONTENT_DOWNLOAD['ITEM_PIPELINES'])
        SpiderController.SETTINGS.set('OUT_DIR', out_dir)

        # initiate CrawlerProcess
        process = CrawlerProcess(SpiderController.SETTINGS)

        for item in target:
            spider_args = {
                'domain': URLUtils.get_domain(item[0]),
                'start_url': URLUtils.reform(item[0]),
                'max_depth': item[1],
                'pattern_list': pattern_list
            }

            # according to Scrapy the current page is at a depth 0
            # but for this project the current page is at depth 1
            # so, adjust the input depth accordingly
            spider_args['max_depth'] -= 1

            # kick off the scrapy crawler
            LOG.debug('Kicking off Scrapy Spider - %s' %spider_args)
            process.crawl(RawContentDownloadSpider, **spider_args)
        process.start() # blocks here until all crawling is done

    def _validate_target(self, target):
        if not isinstance(target, list):
            raise InvalidArgumentError('Arg "target"' \
                                    ' should be a list of tuples')
        if len(target) == 0:
            raise InvalidArgumentError('Arg "target"' \
                                    ' should have at least one element')

        for item in target:
            # base type check
            if not isinstance(item, tuple) or len(item) != 2:
                raise InvalidArgumentError('All elements of "target"' \
                    ' are expected to be tuples of size 2 - ' \
                    '(<url>, <depth>')
            url, depth = item

            # sub-parameter type checks
            type_check = isinstance(url, basestring) and isinstance(depth, int)
            if not type_check:
                raise InvalidArgumentError('Args type check failed. ' \
                    'For "target" ' \
                    'Expected - str,int. Given - "%s"'
                    %(','.join((str(type(x) for x in item)))))

            # sub-parameter value checks
            match = Regex.PT_DOMAIN_FROM_URL.match(url)
            if not match:
                raise InvalidArgumentError('Invalid URL - "%s"' % url)

            if depth <= 0:
                raise InvalidArgumentError('Depth parameter should ' \
                                        'be strictly greater than 0')


class InvalidArgumentError(Exception): pass
