# -*- coding: utf-8 -*-
import re
import json
import datetime
import dateparser


from urllib.parse import urlparse
import urllib

from scrapy import Spider
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector

from ze.spiders import ZeSpider

from ..items.creativework import NewsArticleItem


class GestaoEscolarImpresso(ZeSpider):
	name = 'gestaoescolarimpresso'

	def start_requests(self):
		if hasattr(self, 'keywords'):
			query = getattr(self, 'keywords') # ['enem', 'inep', ...]

		self.search_params['q']=query
		yield Request(self.search_url+'?'+urllib.parse.urlencode(self.search_params), callback=self.get_export_urls)
