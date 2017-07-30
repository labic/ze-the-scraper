# -*- coding: utf-8 -*-

from ze.spiders import ZeSpider

class FolhaDeSaoPauloSpider(ZeSpider):

    name = 'folhadesp'
    allowed_domains = ['folha.uol.com.br']
    parses = [{
        "ze.items.creativework.ArticleItem": {
            "fields": { 
                "name": [
                    "meta[property='og:title']::attr(content)",
                    "meta[name=title]::attr(content)",
                    ".news header h1::text", 
                    "[itemprop=name]::text", 
                    "[itemprop='headline']::text", 
                    "[itemprop=alternativeHeadline]::attr(content)"
                ], 
                "image": [
                    "meta[property='og:description']::attr(content)",
                    "meta[name=description]::attr(content)",
                    'meta[property="og:image"]::attr(content)',
                    "[itemprop=image]::attr(content)", 
                    "[property='og:image']::attr(content)"
                ], 
                "description": [
                    ".documentDescription::text", 
                    "[itemprop=description]::text"
                ], 
                "author": [
                    ".news .author p b", 
                    "[itemprop=author] b::text",
                    ".news__byline p strong::text" 
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
                    "meta[name=keywords]::attr(content)", 
                    "[itemprop=keywords]::text", 
                    "[itemprop=keywords]::attr(content)"
                ]
            }
        }
    }]
