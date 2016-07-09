from scrapy import Item, Field


class FlexibleItem(Item):
    def __setitem__(self, key, value):
        if key not in self.fields:
            self.fields[key] = Field()
        super(FlexibleItem, self).__setitem__(key, value)

    def get_keys(self):
        return tuple('"%s"' %key for key in self.fields)

    def get_values(self):
        return tuple('"%s"' %(str(self.get(key)).replace('"', '""'))
                     for key in self.fields)


class FileDownloadItem(Item):
    file_urls = Field()
    files = Field()
