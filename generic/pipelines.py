import os
import json
import logging

from scrapy import signals
from scrapy.exporters import CsvItemExporter, JsonLinesItemExporter
from scrapy.exporters import XmlItemExporter, PprintItemExporter
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


class ExportPipeline(object):
    @staticmethod
    def _get_exporter(feed_type):
        if feed_type == 'JSON':
            return JsonLinesItemExporter
        elif feed_type == 'CSV':
            return CsvItemExporter
        elif feed_type == 'XML':
            return XmlItemExporter
        else:
            return PprintItemExporter

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        feed_type = settings.get('FEED_TYPE', settings.get('DEFAULT_FEED_TYPE'))
        out_file = settings.get('OUT_FILE', settings.get('DEFAULT_OUT_FILE'))
        pipeline = cls(feed_type, out_file)
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def __init__(self, feed_type, out_file):
        self.feed_type = feed_type
        self.out_file = out_file

    def spider_opened(self, spider):
        self.file = open(self.out_file, 'w')
        self.exporter = ExportPipeline._get_exporter(self.feed_type)(self.file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


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
