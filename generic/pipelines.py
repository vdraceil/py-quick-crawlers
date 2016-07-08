import os
import json
import logging

from scrapy.exceptions import DropItem
from scrapy.pipelines.files import FilesPipeline

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
        # validate item
        if not hasattr(item, 'get_keys') or not hasattr(item, 'get_values'):
            error = 'Skipping Item - missing CSV methods "get_keys"/"get_values"'
            LOG.debug('%s' %error)
            return item

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


class ContentDownloadPipeline(FilesPipeline):
    @classmethod
    def from_settings(cls, settings):
        base_dir = settings.get('FILES_STORE', settings.get('DEFAULT_OUT_DIR'))
        enable_dir_structure = settings.get('FILES_STORE_ENABLE_DIR_STRUCTURE', 0)
        return cls(base_dir, enable_dir_structure)

    def __init__(self, base_dir, enable_dir_structure):
        super(ContentDownloadPipeline, self).__init__(base_dir)
        self.enable_dir_structure = enable_dir_structure

    def file_path(self, request, response=None, info=None):
        path = super(ContentDownloadPipeline, self).file_path(request, response, info)
        if self.enable_dir_structure:
            url = request.url
            path = os.path.join(URLUtils.get_domain(url), URLUtils.get_path(url)[1:])
