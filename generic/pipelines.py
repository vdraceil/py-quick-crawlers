import os
import json
import logging

from scrapy.exceptions import DropItem

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
        self.is_first_line = True

    def _get_out_file(self, settings):
        return settings.get('OUT_FILE') \
            or settings.get('DEFAULT_OUT_FILE') + '.json'

    def process_item(self, item, spider):
        out_file = self._get_out_file(spider.settings)
        if not self.file:
            LOG.debug('Write to file initiated')
            self.file = open(out_file, 'w')
            # write array open
            self.file.write('[')

        # write line
        line = json.dumps(dict(item))
        if self.is_first_line:
            self.is_first_line = False
        else:
            line = ',' + os.linesep + line
        self.file.write(line)

        return item

    def close_spider(self, spider):
        out_file = self._get_out_file(spider.settings)
        if self.file:
            # write array close
            self.file.write(']')
            LOG.debug('Write to file complete: %s' %out_file)
            self.file.close()


class ContentDownloadPipeline(object):
    def _get_out_dir(self, settings):
        return settings.get('OUT_DIR') or settings.get('DEFAULT_OUT_DIR')

    def process_item(self, item, spider):
        out_dir = self._get_out_dir(spider.settings)
        file_path = os.path.join(out_dir,
                            URLUtils.get_domain(item['url']),
                            URLUtils.get_path(item['url'])[1:])
        dir_path = os.path.dirname(file_path)

        # make dir
        ShellUtils.mkdirp(dir_path)

        # dump content into file
        with open(file_path, 'w+b') as file:
            file.write(item['content'])
