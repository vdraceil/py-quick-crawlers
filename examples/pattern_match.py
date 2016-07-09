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
    ('http://www.uniquemetalworks.net', 2),
]

# define pattern dictionary
pattern_dict = {
    # '<name>': <regex>
    'email': re.compile(r'[a-zA-Z0-9_\.+\-]+@[a-zA-Z0-9\-]+\.[a-zA-Z0-9\-\.]+')
}

# definte output file ; optional ; default - 'default.<feed_type>'
out_file = 'output.json'

# define feed type - JSON/CSV/XML ; optional ; default - JSON
feed_type = 'JSON'

# invoke the Crawl API - it will block until completion
controller.pattern_match_crawl(target, pattern_dict, out_file, feed_type)
print "CRAWL COMPLETE!! Output File: %s" %out_file
