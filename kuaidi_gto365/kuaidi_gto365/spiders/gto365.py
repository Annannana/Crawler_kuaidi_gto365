# -*- coding: utf-8 -*-
import re
import json
import scrapy
from kuaidi_gto365.items import KuaidiItem


class Gto365Spider(scrapy.Spider):
    name = 'gto365'
    allowed_domains = ['gto365.com']
    parent_url = 'http://www.gto365.com/WebsiteAPI/SitesInfo/v1/ParentSite'
    son_site_url = 'http://www.gto365.com/WebsiteAPI/SitesInfo/v1/AllSite'
    site_url = 'http://www.gto365.com/WebsiteAPI/SitesInfo/v1/SitesInfo'

    def start_requests(self):
        parent_data = {'ProvinceState': '0'}
        # data = {'ProvinceCode': "110000", 'CityCode': "110100", 'ProvinceState': '1'}
        yield scrapy.Request(url=self.parent_url, callback=self.parent_parse,
                             method='POST', body=json.dumps(parent_data))

    def parent_parse(self, response):
        text = response.text
        site_list = re.findall('<SiteNameInfo>(.*?)</SiteNameInfo>', text)
        for site in site_list:
            get_site_id = re.search(r'<Id>(\d+)</Id>', site)
            if not get_site_id:
                continue
            site_id = get_site_id.group(1)
            site_data = {'Id': site_id}
            yield scrapy.Request(url=self.site_url, callback=self.site_parse,
                                 method='POST', body=json.dumps(site_data))

            if 'AllSite' in response.url:
                continue
            get_son_site_count = re.search(r'<Count>(\d+)</Count>', site)
            if get_son_site_count and get_son_site_count.group(1) not in ['0', '']:
                son_site_data = {'ParentSiteCode': site_id}
                yield scrapy.Request(url=self.son_site_url, callback=self.parent_parse,
                                     method='POST', body=json.dumps(son_site_data))

    def site_parse(self, response):
        item = KuaidiItem()
        text = response.text

        item['province'] = self.handle_detail(re.search('<Province>(.*?)</Province>', text))
        item['city'] = self.handle_detail(re.search('<City>(.*?)</City>', text))
        item['district'] = self.handle_detail(re.search('<District>(.*?)</District>', text))
        item['address'] = self.handle_detail(re.search('<SiteAddress>(.*?)</SiteAddress>', text))

        item['link'] = 'http://www.gto365.com/#/orgsearch'
        item['link_explain'] = 'link中搜索 -->' + item['address']
        item['name'] = '国通快递' + '(' + self.handle_detail(re.search('<SiteName>(.*?)</SiteName>', text)) + ')'
        item['linkman'] = self.handle_detail(re.search('<PrincipalName>(.*?)</PrincipalName>', text))
        item['phone'] = []
        linkman_tel = self.handle_detail(re.search('<PrincipalMobile>(.*?)</PrincipalMobile>', text))
        site_tel = self.handle_detail(re.search('<SiteTel>(.*?)</SiteTel>', text))
        if linkman_tel: item['phone'].append(linkman_tel)
        if linkman_tel: item['phone'].append(site_tel)
        item['serviceitems'] = self.handle_detail(re.search('<ValueAddedService>(.*?)</ValueAddedService>', text))

        item['mainname'] = '国通快递'
        item['tag'] = ['国通快递']
        item['topic'] = ['国通快递']
        item['category'] = ['快递物流']
        item['officialurl'] = 'http://www.gto365.com'
        item['microblog'] = 'https://weibo.com/gtoxll'
        item['MapType'] = '1'
        yield item

    def handle_detail(self, content):
        return content.group(1) if content else ''
