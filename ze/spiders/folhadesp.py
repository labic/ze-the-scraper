# -*- coding: utf-8 -*-

from ze.spiders import ZeSpider

class FolhaDeSaoPauloSpider(ZeSpider):

    name = 'folhadesp'
    allowed_domains = ['folha.uol.com.br']
    parses = [{
        "ze.items.creativework.ArticleItem": {
            "fields": { 
                "name": [
                    ".news header h1::text", 
                    "[itemprop=name]::text", 
                    "[itemprop=alternativeHeadline]::attr(content)"
                ], 
                "image": [
                    "[itemprop=image]::attr(content)", 
                    "[property='og:image']::attr(content)"
                ], 
                "description": [
                    ".documentDescription::text", 
                    "[itemprop=description]::text"
                ], 
                "author": [
                    ".news .author p", 
                    "[itemprop=author]::text"
                ], 
                "datePublished": [
                    ".news time::attr(datetime)", 
                    "[itemprop=datePublished]::text"
                ], 
                "dateModified": [
                    "[itemprop=dateModified]::text"
                ], 
                "articleBody": [
                    ".news .content", 
                    "[itemprop=articleBody]"
                ], 
                "keywords": [
                    "[itemprop=keywords]::text", 
                    "[itemprop=keywords]::attr(content)"
                ]
            }
        }
    }]
