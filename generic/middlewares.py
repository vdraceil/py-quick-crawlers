import logging

from twisted.internet.error import TimeoutError as ServerTimeoutError, \
    DNSLookupError, ConnectionRefusedError, ConnectionDone, ConnectError, \
    ConnectionLost, TCPTimedOutError
from twisted.internet.defer import TimeoutError as UserTimeoutError
from scrapy.exceptions import IgnoreRequest
from scrapy.contrib.spidermiddleware.depth import DepthMiddleware

from utils.general import URLUtils


LOG = logging.getLogger(__name__)

class DomainDepthMiddleware(DepthMiddleware):
    def process_spider_output(self, response, result, spider):
        # just re-set the maxdepth variable that the actual DepthMiddleware
        # refers too, and let it do its job
        self.maxdepth = spider.max_depth;

        return super(DomainDepthMiddleware, self) \
            .process_spider_output(response, result, spider);


class CustomDownloaderMiddleware(object):
    EXCEPTIONS_TO_IGNORE = (ServerTimeoutError, UserTimeoutError, DNSLookupError,
                        ConnectionRefusedError, ConnectionDone, ConnectError,
                        ConnectionLost, TCPTimedOutError, IOError)

    def __init__(self):
        self.visited_urls = set()
        self.cur_domain = ''

    def process_response(self, request, response, spider):
        if self.is_invalid(request, spider):
            return IgnoreRequest()

        if self.is_duplicate(request):
            LOG.debug('Duplicate URL: %s' %request.url)
            return IgnoreRequest()

        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_IGNORE):
            LOG.debug('Skipping URL "%s" due to Exception "%s"'
                      %(request.url, exception.__class__.__name__))
            return IgnoreRequest()
        return request

    def is_duplicate(self, request):
        url = URLUtils.simplify(request.url)
        if url in self.visited_urls:
            return True
        self.visited_urls.add(url)

    def is_invalid(self, request, spider):
        # a request is valid only if the request URL falls within the allowed
        # domains of the corresponding spider instance
        domain = URLUtils.get_domain(request.url)

        if domain == self.cur_domain:
            # don't even bother looking at spider's allowed domains
            return False

        if domain in spider.allowed_domains:
            # reset the domain and empty the visited_urls set
            # this saves memory in case of big jobs
            self.cur_domain = domain
            self.visited_urls.clear()
            return False
        LOG.debug('Skipping URL "%s" as it falls out of the allowed domain "%s"'
                  %(request.url, self.cur_domain))
        return True
