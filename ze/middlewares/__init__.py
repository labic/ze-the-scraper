# -*- coding: utf-8 -*-

import re
import random
import base64
import logging

logger = logging.getLogger(__name__)


class Mode:
    RANDOMIZE_EACH_REQUESTS, RANDOMIZE_PROXY_ONCE, SET_CUSTOM_PROXY = range(3)


class RandomProxy(object):

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings, crawler.stats)


    def __init__(self, settings, stats):
        self.mode = settings.get('PROXY_MODE')
        self.proxy_list = settings.get('PROXY_LIST')
        self.chosen_proxy = ''
        
        self.stats = stats
        self.stats.set_value('proxy.mode', self.mode)
        self.stats.set_value('proxy.list.file', self.proxy_list)
        self.stats.set_value('proxies.quantity', 0)
        self.stats.set_value('proxy.log.warning.count', 0)
        self.stats.set_value('proxies.used', 0)
        self.stats.set_value('proxies.removed', 0)
        
        if self.proxy_list is None:
            raise KeyError('PROXY_LIST setting is missing')

        if self.mode == Mode.RANDOMIZE_EACH_REQUESTS or self.mode == Mode.RANDOMIZE_PROXY_ONCE:
            self.proxies = {}
            
            with open(self.proxy_list, 'r') as plf:
                for line in plf.readlines():
                    parts = re.match('(\w+://)(\w+:\w+@)?(.+)', line.strip())
                    if not parts:
                        continue
    
                    # Cut trailing @
                    if parts.group(2):
                        user_pass = parts.group(2)[:-1]
                    else:
                        user_pass = ''
    
                    self.proxies[parts.group(1) + parts.group(3)] = user_pass
                    
                    self.stats.inc_value('proxies.quantity')
                
            if self.mode == Mode.RANDOMIZE_PROXY_ONCE:
                self.chosen_proxy = random.choice(list(self.proxies.keys()))
        elif self.mode == Mode.SET_CUSTOM_PROXY:
            custom_proxy = settings.get('CUSTOM_PROXY')
            self.proxies = {}
            parts = re.match('(\w+://)(\w+:\w+@)?(.+)', custom_proxy.strip())
            
            if not parts:
                raise ValueError('CUSTOM_PROXY is not well formatted')

            if parts.group(2):
                user_pass = parts.group(2)[:-1]
            else:
                user_pass = ''

            self.proxies[parts.group(1) + parts.group(3)] = user_pass
            self.chosen_proxy = parts.group(1) + parts.group(3)


    def process_request(self, request, spider):
        # Don't overwrite with a random one (server-side state for IP)
        if 'proxy' in request.meta:
            if request.meta['exception'] is False:
                return
        
        request.meta['exception'] = False
        
        if len(self.proxies) == 0:
            raise ValueError('All proxies are unusable, cannot proceed')

        if self.mode == Mode.RANDOMIZE_EACH_REQUESTS:
            proxy_address = random.choice(list(self.proxies.keys()))
        else:
            proxy_address = self.chosen_proxy

        proxy_user_pass = self.proxies[proxy_address]

        if proxy_user_pass:
            request.meta['proxy'] = proxy_address
            basic_auth = 'Basic ' + base64.b64encode(proxy_user_pass.encode()).decode()
            request.headers['Proxy-Authorization'] = basic_auth
        else:
            logger.warning('Proxy user pass not found')
            self.stats.inc_value('proxy.log.warning.count')
        
        logger.info('Using proxy <%s>, %d proxies left' % (proxy_address, len(self.proxies)))
        self.stats.inc_value('proxies.used')


    def process_exception(self, request, exception, spider):
        if 'proxy' not in request.meta:
            return
        if self.mode == Mode.RANDOMIZE_EACH_REQUESTS or self.mode == Mode.RANDOMIZE_PROXY_ONCE:
            proxy = request.meta['proxy']
            try:
                del self.proxies[proxy]
            except KeyError:
                pass
            request.meta["exception"] = True
            if self.mode == Mode.RANDOMIZE_PROXY_ONCE:
                self.chosen_proxy = random.choice(list(self.proxies.keys()))
            logger.info('Removing failed proxy <%s>, %d proxies left' % (proxy, len(self.proxies)))
            self.stats.inc_value('proxies.removed')