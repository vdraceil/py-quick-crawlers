import scrapy


class FlexibleItem(scrapy.Item):
    def __setitem__(self, key, value):
        if key not in self.fields:
            self.fields[key] = scrapy.Field()
        super(FlexibleItem, self).__setitem__(key, value)
