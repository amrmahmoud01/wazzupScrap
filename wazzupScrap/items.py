# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QuotescrapItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    price = scrapy.Field()
    type = scrapy.Field()
    productLink = scrapy.Field()
    storeId = scrapy.Field()    
    imageLink = scrapy.Field()
    image_urls = scrapy.Field()  # URLs to fetch
    images = scrapy.Field()      # Results after download
    pass
