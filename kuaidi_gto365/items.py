# -*- coding: utf-8 -*-
import scrapy


class KuaidiItem(scrapy.Item):
    province = scrapy.Field()
    city = scrapy.Field()
    district = scrapy.Field()
    address = scrapy.Field()

    link = scrapy.Field()
    link_explain = scrapy.Field()
    name = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    lat = scrapy.Field()
    lng = scrapy.Field()
    serviceitems = scrapy.Field()

    mainname = scrapy.Field()
    tag = scrapy.Field()
    topic = scrapy.Field()
    category = scrapy.Field()
    officialurl = scrapy.Field()  # 官网
    microblog = scrapy.Field()  # 新浪微博主页
    MapType = scrapy.Field()
