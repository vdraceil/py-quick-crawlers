import os
import json
import logging

from scrapy.exceptions import DropItem
from scrapy.exceptions import CloseSpider

from utils.general import URLUtils
from utils.general import ShellUtils


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
        self.out_file = None

    def _get_out_file(self, settings):
        return settings.get('OUT_FILE') \
            or settings.get('DEFAULT_OUT_FILE') + '.json'

    def process_item(self, item, spider):
        if not self.file:
            self.out_file = self._get_out_file(spider.settings)
            LOG.debug('Write to file initiated: %s' %self.out_file)
            self.file = open(self.out_file, 'w')
            # write array open and first line
            self.file.write('[' + json.dumps(dict(item)))
        else:
            line = ',' + os.linesep + json.dumps(dict(item))
            self.file.write(line)

        # return item to next pipeline, if any
        return item

    def close_spider(self, spider):
        if self.file:
            # write array close
            self.file.write(']')
            LOG.debug('Write to file complete: %s' %self.out_file)


class CSVWriterPipeline(object):
    DELIMITER  = ','

    def __init__(self):
        self.file = None
        self.out_file = None

    def _get_out_file(self, settings):
        return settings.get('OUT_FILE') \
            or settings.get('DEFAULT_OUT_FILE') + '.csv'

    def process_item(self, item, spider):
        if not self.file:
            self.out_file = self._get_out_file(spider.settings)
            LOG.debug('Write to file initiated: %s' %self.out_file)
            self.file = open(self.out_file, 'w')
            # write headers
            self.file.write(CSVWriterPipeline.DELIMITER.join(item.get_keys()))

        line = os.linesep + CSVWriterPipeline.DELIMITER.join(item.get_values())
        self.file.write(line)

        # return item to next pipeline, if any
        return item

    def close_spider(self, spider):
        if self.file:
            LOG.debug('Write to file complete: %s' %self.out_file)
            self.file.close()


class ContentDownloadPipeline(object):
    def __init__(self):
        self.out_dir = None

    def _get_out_dir(self, settings):
        return settings.get('OUT_DIR') or settings.get('DEFAULT_OUT_DIR')

    def process_item(self, item, spider):
        if not self.out_dir:
            self.out_dir = self._get_out_dir(spider.settings)

        file_path = os.path.join(self.out_dir,
                            URLUtils.get_domain(item['url']),
                            URLUtils.get_path(item['url'])[1:])
        dir_path = os.path.dirname(file_path)

        # make dir
        ShellUtils.mkdirp(dir_path)

        # dump content into file
        with open(file_path, 'w+b') as file:
            file.write(item['content'])

        # return item to next pipeline, if any
        return item

    def close_spider(self, spider):
        LOG.debug('Write to dir complete: %s' %self.out_dir)
