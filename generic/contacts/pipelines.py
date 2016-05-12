import os
import logging

from scrapy.exceptions import DropItem


LOG = logging.getLogger(__name__)

class DuplicatesFilterPipeline(object):
    def __init__(self):
        self.emails = set()

    def process_item(self, item, spider):
        if item['email'] in self.emails:
            raise DropItem('Duplicate Item Found: %s' %item)
        self.emails.add(item['email'])
        return item


class FileWriterPipeline(object):
    def __init__(self):
        self.file = None

    def process_item(self, item, spider):
        if not self.file:
            LOG.debug('Write to file initiated')
            self.file = open(spider.out_file, 'a')
        self.file.write(item['email'] + os.linesep)

    def close_spider(self, spider):
        if self.file:
            LOG.debug('Write to file complete: %s' %spider.out_file)
            self.file.close()
