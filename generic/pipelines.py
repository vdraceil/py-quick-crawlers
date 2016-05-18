import os
import json
import logging

from scrapy.exceptions import DropItem


LOG = logging.getLogger(__name__)

class DuplicatesFilterPipeline(object):
    def __init__(self):
        self.visited = set()

    def process_item(self, item, spider):
        value = json.dumps(dict(item))
        if value in self.visited:
            raise DropItem('Duplicate Item Found: %s' %item)
        self.visited.add(value)
        return item


class JSONWriterPipeline(object):
    def __init__(self):
        self.file = None

    def process_item(self, item, spider):
        if not self.file:
            LOG.debug('Write to file initiated')
            self.file = open(spider.out_file, 'a')
        self.file.write(json.dumps(dict(item)) + os.linesep)
        return item

    def close_spider(self, spider):
        if self.file:
            LOG.debug('Write to file complete: %s' %spider.out_file)
            self.file.close()
