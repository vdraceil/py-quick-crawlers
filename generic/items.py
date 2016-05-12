import scrapy


class ContactInfoItem(scrapy.Item):
    phone = scrapy.Field()
    email = scrapy.Field()
    url = scrapy.Field()
    domain = scrapy.Field()
    depth = scrapy.Field()
