import re
import logging

from constants import Regex
from controller import SpiderController


logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# create an instance of the Controller
controller = SpiderController()

# define a scraping job (target)
target = [
    # (<site>, <max_depth>)
    ('http://www.uniquemetalworks.net', 2),
]

# define patterns
pattern_dict = {
    'email': Regex.PT_EMAIL
}

# invoke the Crawl API
# it will block till it completes
out_file = 'output.json'
controller.pattern_match_crawl(target, pattern_dict,out_file)
print "CRAWL COMPLETE!!"

# pattern_list = [re.compile(r'.*\.html')]
# out_dir = 'output'
# controller.content_download_crawl(target, pattern_list, out_dir)
# print "CRAWL COMPLETE!!"
