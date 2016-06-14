import re
import logging

from constants import Regex
from controller import SpiderController


logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# create an instance of the Controller
controller = SpiderController()

# define a scraping job (website_list)
website_list = [
    # (<site>, <max_depth>)
    ('http://www.uniquemetalworks.net', 2),
]

# define patterns
pattern_dict = {
    'email': Regex.PT_EMAIL
}

# define custom pipelines
pipelineOverrides = {
    'generic.pipelines.DuplicatesFilterPipeline': 100,
    'generic.pipelines.CSVWriterPipeline': 800,
    'generic.pipelines.JSONWriterPipeline': 900
}

# invoke the Crawl API
# it will block till it completes
controller.pattern_match_crawl(website_list, pattern_dict,
                               pipelineOverrides=pipelineOverrides)
print "CRAWL COMPLETE!!"

# file_pattern = re.compile(r'.*\.html')
# out_dir = 'output'
# controller.content_download_crawl(website_list, file_pattern, out_dir)
# print "CRAWL COMPLETE!!"
