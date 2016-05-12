import logging

from controller import SpiderController


logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# create an instance of the Controller
controller = SpiderController()

# define a scraping job (website_list)
website_list = [
    # (<site>, <max_depth>)
    ('http://www.google.com', 2),
    ('http://mnmlist.com/', 2),
]

# invoke the Crawl API
# it will block till it completes
controller.contact_info_crawl(website_list)
print "CRAWL COMPLETE!!"
