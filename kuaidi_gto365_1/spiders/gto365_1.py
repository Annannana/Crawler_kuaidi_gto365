
# -*- coding: utf-8 -*-
import re
import json
import scrapy
from kuaidi_gto365_1.items import KuaidiGto3651Item


class Gto365Spider(scrapy.Spider):
    name = 'gto365_1'
    allowed_domains = ['gto365.com']
    parent_url = 'http://www.gto365.com/WebSiteAPI/ZTDService/v1/OfficialNameGroup'
    son_site_url = 'http://www.gto365.com/WebSiteAPI/ZTDService/v1/OfficialNameGroup?querytype=0&provinceCode='
    site_url = 'http://www.gto365.com/WebSiteAPI/ZTDService/v1/DispatchAreaInfo?officialCode='

    def start_requests(self):
        yield scrapy.Request(url=self.parent_url, callback=self.parent_parse,
                             method='Get')
    # get all province codes
    def parent_parse(self, response):
        json_text = json.loads(response.text)['List']
        province = set()
        count = 0
        for city in json_text:
            count += city['Count']
            province.add(city['NameList'][0]['ProvinceCode'])
        for ProvinceCode in province:
            yield scrapy.Request(url=self.son_site_url+ProvinceCode, callback=self.son_parse,
                                 method='Get')
    # get all stores' codes in a province
    def son_parse(self, response):
        json_text = json.loads(response.text)['List']
        for city in json_text:
            for store in city['NameList']:
                item = KuaidiGto3651Item()
                item['city'] = store['CityName']
                item['province'] = store['ProvinceName']
                item['name'] = store['OfficialName']
                OfficialCode = store['OfficialCode']
                yield scrapy.Request(url=self.site_url + str(OfficialCode), callback=self.site_parse,
                                     method='Get', meta={'item':item})
    # get a store's information
    def site_parse(self, response):
        data = json.loads(response.text)['Data']
        item = response.meta.get('item')
        phone = [data['AdminPhone'], data['SitePhone']]
        item['phone'] = [p for p in phone if p]
        item['linkman'] = data['AdminMan']
        item['officialurl'] = data['Website']
        item['address'] = data['Address']
        item['qq'] = data['SiteImoQQ']
        item['fax'] = data['SiteFax']
        item['distribution'] = data['DispatchRange']
        item['nodistribution'] = data['NotDispatchAddress']
        item['registrationtime'] = data['RegisterDate']
        item['mainname'] = '国通快递'
        item['tag'] = ['国通快递']
        item['topic'] = ['国通快递']
        item['category'] = ['快递物流']
        item['officialurl'] = 'http://www.gto365.com'
        item['microblog'] = 'https://weibo.com/gtoxll'
        item['MapType'] = '1'
        item['link'] = 'http://www.gto365.com/#/orgsearch'
        yield item

