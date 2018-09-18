# -*- coding: utf-8 -*-
import json

import scrapy

from kuaidi100_courier.items import Kuaidi100CourierItem


class CourierSpider(scrapy.Spider):
    name = 'courier'
    start_url = "https://m.kuaidi100.com/apicenter/kdmkt.do"

    def start_requests(self):

        with open('baidu.json', 'r', encoding="utf-8") as lines:
            for idx, line in enumerate(lines):
                lat, lng = line.strip().split(",")

                form_data = {
                    "method": "queryMyMkt",
                    "latitude": lat,
                    "longitude": lng,
                }
                yield scrapy.FormRequest(self.start_url, formdata=form_data, callback=self.parse)

    def parse(self, response):
        contents = json.loads(response.text)
        if len(contents):
            couriers = contents.get('data', [])
            for courier in couriers:
                item = Kuaidi100CourierItem()
                item['linkman'] = courier.get('name', '').split('-')[0]
                shop_names = courier.get('comlist', '')
                name = []
                for shop_name in shop_names:
                    name.append(shop_name.get('name', ''))
                name = "/".join(name)
                item['name'] = name
                item['phone'] = [courier.get('phone', '')]
                item['address'] = courier.get('address', '')
                item['lat'] = str(courier.get('lat', ''))
                item['lng'] = str(courier.get('lon', ''))
                item['city'] = courier.get('city', '')
                item['scores'] = courier.get('score', '')
                item['deliverytime'] = courier.get('serviceTime', '')
                item['district'] = courier.get('county', '')
                item['serviceintro'] = courier.get('name', '').split('-')[-1]
                item['MapType'] = '1'
                item['category'] = ['bk物流快递']
                item['link'] = response.url
                yield item


