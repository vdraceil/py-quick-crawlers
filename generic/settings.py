# scrapy - code related settings
BOT_NAME = 'generic'
SPIDER_MODULES = ['generic.spiders']
NEWSPIDER_MODULE = 'generic.spiders'
LOG_ENABLED = True
LOG_LEVEL = 'DEBUG'

# pipelines
ITEM_PIPELINES = {
    'generic.pipelines.FileWriterPipeline': 900
}

# middlewares
SPIDER_MIDDLEWARES = {
    'generic.middlewares.DomainDepthMiddleware': 100,
    'scrapy.contrib.spidermiddleware.depth.DepthMiddleware': None
}

DOWNLOADER_MIDDLEWARES = {
    'generic.middlewares.CustomDownloaderMiddleware': 650,
    'scrapy.contrib.downloadermiddleware.downloadtimeout.DownloadTimeoutMiddleware': 350
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
DOWNLOAD_TIMEOUT = 120  # seconds

# custom
