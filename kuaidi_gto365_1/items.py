
import scrapy


class KuaidiGto3651Item(scrapy.Item):
    province = scrapy.Field()
    city = scrapy.Field()
    address = scrapy.Field()

    link = scrapy.Field()
    name = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    qq = scrapy.Field()
    fax = scrapy.Field()
    registrationtime = scrapy.Field()
    distribution = scrapy.Field()
    nodistribution = scrapy.Field()

    mainname = scrapy.Field()
    tag = scrapy.Field()
    topic = scrapy.Field()
    category = scrapy.Field()
    officialurl = scrapy.Field()  # 官网
    microblog = scrapy.Field()  # 新浪微博主页
    MapType = scrapy.Field()
