import scrapy


class ContactInfoItem(scrapy.Item):
    url = scrapy.Field()
    domain = scrapy.Field()
    depth = scrapy.Field()
    email = scrapy.Field()
