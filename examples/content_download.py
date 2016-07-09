import re
import logging

from py_quick_crawlers import Controller


# configure logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# create an instance of the Controller
controller = Controller()

# define target - list of URLs to crawl with max crawl depth for each URL
target = [
    # (<site>, <max_depth>)
    ('http://afcorfmc.org/2009.html', 2),
]

# define pattern list
pattern_list = [
    re.compile(r'.*\.pdf'),
    re.compile(r'.*\.ppt')
]

# definte output dir
out_dir = 'output'

# define output dir structure
enable_dir_structure = True

# invoke the Crawl API - it will block until completion
controller.content_download_crawl(target, pattern_list, out_dir, enable_dir_structure)
print "CRAWL COMPLETE!! Output Dir: %s" %out_dir
