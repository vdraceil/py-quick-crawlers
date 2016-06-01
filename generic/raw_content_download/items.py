import scrapy


class ContentInfoItem(scrapy.Item):
    url = scrapy.Field()
    content = scrapy.Field()
