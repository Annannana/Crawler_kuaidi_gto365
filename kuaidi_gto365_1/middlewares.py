# -*- coding: utf-8 -*-
import time
import random
import hashlib


class RandomUserAgentMiddleware(object):
    def __init__(self, user_agent):
        self.user_agent = user_agent

    @classmethod
    def from_crawler(cls, crawler):
        return cls(user_agent=crawler.settings.get('PC_USER_AGENT'))

    def process_request(self, request, spider):
        ua = random.choice(self.user_agent)
        request.headers.setdefault("User-Agent", ua)
        request.headers.setdefault('Accept', 'application/json, text/plain, */*')
        request.headers.setdefault("Content-Type", 'application/json')


class RandomProxyMiddleware(object):
    def __init__(self, proxies):
        self.proxies = proxies

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(proxies=settings.get('PROXIES'))

    def process_request(self, request, spider):
        request.meta['proxy'] = self.proxies


class MaYiProxyMiddleware(object):
