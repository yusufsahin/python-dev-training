import scrapy


class PostalCodeItem(scrapy.Item):
    il = scrapy.Field()
    ilce = scrapy.Field()
    mahalle = scrapy.Field()
    sokak = scrapy.Field()
    posta_kodu = scrapy.Field()
