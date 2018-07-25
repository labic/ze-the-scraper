# -*- coding: utf-8 -*-
import re
import json
import datetime
import sys
from ...items.creativework import SocialMediaPosting

import scrapy
from scrapy import Selector
from scrapy.http.request import Request
from scrapy.http.request.form import FormRequest
from scrapy.spiders.init import InitSpider
from scrapy.exceptions import CloseSpider
import scrapy_splash

__all__ = ['FacebookSpider']


class FacebookSpider(InitSpider):
    name = 'social.facebook'
    allowed_domains = ['facebook.com']
    start_urls = ['https://m.facebook.com/login']

    def parse(self, resp):
        return FormRequest.from_response(
            resp,
            formxpath='//form[contains(@action, "login")]',
            formdata={
                'email': self.user,
                'pass': self.password,
            },
            callback=self.parse_home,
        )

    def parse_home(self, resp):
        if resp.css('#approvals_code'):
            # Handle 'Approvals Code' checkpoint (ask user to enter code).
            if not self.code:
                # Show facebook messages via logs
                # and request user for approval code.
                message = resp.css('._50f4::text').extract()[0]
                self.log(process_string(message))
                message = resp.css('._3-8y._50f4').xpath('string()').extract()[0]
                self.log(process_string(message))
                self.code = input('Enter the code: ')
            self.code = str(self.code)
            
            if not (self.code and self.code.isdigit()):
                self.logger.error('Bad approvals code detected.')
                return
            
            return FormRequest.from_response(
                resp,
                formdata={'approvals_code': self.code},
                callback=self.parse_home,
            )
        # elif resp.css('input[name="email"]'):
        #     # Handle 'Save Browser' checkpoint.
        #     return FormRequest.from_response(
        #         resp,
        #         formdata={'name_action_selected': 'dont_save'},
        #         callback=self.parse_shares,
        #         dont_filter=True,
        #     )
        # elif resp.css('button#checkpointSubmitButton'):
        #     # Handle `Someone tried to log into your account` warning.
        #     return FormRequest.from_response(
        #         resp, callback=self.parse_home, dont_filter=True,)
        
        shares_href = 'https://m.facebook.com/browse/shares?id=1936718436380232'
        meta = {
            # 'splash': {
            #     'args': {
            #         'html': 1,
            #         'png': 0,
            #         'jpg': 0,
            #         'gif': 0,
            #         'css': 0,
            #     },
            #     'splash_headers': resp.headers,
            # }
        }
        yield scrapy.Request(shares_href, 
                             self.parse_shares, 
                             headers=resp.headers,
                             meta=meta)

    def parse_shares(self, resp):
        print(resp.body)