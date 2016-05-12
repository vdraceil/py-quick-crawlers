import scrapy


class ContactInfoItem(scrapy.Item):
    email = scrapy.Field()
