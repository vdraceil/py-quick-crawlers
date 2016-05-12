import os
import logging

from scrapy.exceptions import DropItem


LOG = logging.getLogger(__name__)

class FileWriterPipeline(object):
    def __init__(self):
        LOG.debug('Write to file initiated')
        self.file = open('output.txt', 'w')

    def process_item(self, item, spider):
        LOG.debug('herererere')
        self.file.write(','.join(item['emails']) + os.linesep)

    def close_spider(self, spider):
        if self.file:
            LOG.debug('Write to file complete')
            self.file.close()
