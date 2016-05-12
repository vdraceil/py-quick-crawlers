import os
import logging

from scrapy.exceptions import DropItem


LOG = logging.getLogger(__name__)

class FileWriterPipeline(object):
    def __init__(self):
        LOG.debug('Write to file initiated')
        self.file = open('output.txt', 'w')

    def process_item(self, item, spider):
        self.file.write(item['email'] + os.linesep)

    def close_spider(self, spider):
        if self.file:
            LOG.debug('Write to file complete')
            self.file.close()
