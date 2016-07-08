# scrapy - code related settings
BOT_NAME = 'scrapy_generic_spiders'
SPIDER_MODULES = ['generic.spiders.pattern_match',
                  'generic.spiders.raw_content_download']
NEWSPIDER_MODULE = 'generic.spiders'
LOG_LEVEL = 'DEBUG'
LOG_ENABLED = False

# pipelines
ITEM_PIPELINES = {
    # customized/overridden in APIs which invoke respective spiders
}

# extensions
EXTENSIONS = {
    'scrapy.extensions.logstats.LogStats': None,
    'scrapy.extensions.telnet.TelnetConsole': None,
    'scrapy.extensions.corestats.CoreStats': None,
}

# middlewares
SPIDER_MIDDLEWARES = {
    'generic.middlewares.DomainDepthMiddleware': 100,
    'scrapy.spidermiddlewares.depth.DepthMiddleware': None
}

DOWNLOADER_MIDDLEWARES = {
    'generic.middlewares.CustomDownloaderMiddleware': 650,
    'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,
    'scrapy.downloadermiddlewares.stats.DownloaderStats': None
}

# how we identify ourselves to the target domains
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) ' \
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36'

# how much deep in the graph should we go for a domain
DEPTH_LIMIT = 1

# enable breadth first search
DEPTH_PRIORITY = 1

# delay between subsequent requests to the same domain
DOWNLOAD_DELAY = 0.2   # 200 milli-seconds

# the amount of time that the downloader will wait before timing out
DOWNLOAD_TIMEOUT = 1800  # 1800 seconds = 30 mins

# disable max size file download limitation
DOWNLOAD_WARNSIZE = 0

# custom
DEFAULT_OUT_DIR = '.'
DEFAULT_OUT_FILE = 'default'
DEFAULT_FEED_TYPE = 'JSON'
