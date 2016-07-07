import logging

from twisted.internet.error import TimeoutError as ServerTimeoutError, \
    DNSLookupError, ConnectionRefusedError, ConnectionDone, ConnectError, \
    ConnectionLost, TCPTimedOutError
from twisted.internet.defer import TimeoutError as UserTimeoutError
from scrapy.spidermiddlewares.depth import DepthMiddleware


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

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_IGNORE):
            LOG.debug('Skipping URL "%s" due to Exception "%s"'
                      %(request.url, exception.__class__.__name__))
            return None
        return request
