from scrapy import Item, Field


class FlexibleItem(Item):
    def __setitem__(self, key, value):
        if key not in self.fields:
            self.fields[key] = Field()
        super(FlexibleItem, self).__setitem__(key, value)


class ContentInfoItem(Item):
    url = Field()
    content = Field()
