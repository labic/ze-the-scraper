# -*- coding: utf-8 -*-

from ze.spiders import ZeSpider

class G1Spider(ZeSpider):

    name = 'g1'
    allowed_domains = ['g1.com.br']
    parses = [{
        "ze.items.creativework.ArticleItem": {
            "fields": { 
                "name": [ 
                    "[itemprop=name]::text", 
                    ".content-head__title::text", 
                    ".materia-titulo h1::text", 
                    ".entry-title::text" 
                ], 
                "image": [ 
                    "[itemprop=image]::attr(content)", 
                    "[property='og:image']::attr(content)"
                ], 
                "description": [ 
                    "[itemprop=description]::text", 
                    "[itemprop=alternativeHeadline]::text", 
                    ".content-head__subtitle::text", 
                    ".materia-titulo h2::text"  
                ], 
                "author": [
                    "[itemprop=author]::text", 
                    "[itemprop=creator]::text", 
                    ".anunciante-publieditorial::text"
                ], 
                "datePublished": [
                    "[itemprop=datePublished]::attr(datetime)", 
                    "[itemprop=datePublished]::text", 
                    "time[datetime]::text" 
                ], 
                "dateModified": [
                    "[itemprop=dateModified]::attr(datetime)" , 
                    "[itemprop=dateModified]::text", 
                    ".updated"
                ], 
                "articleBody": [
                    "[itemprop=articleBody]",
                    ".materia-conteudo", 
                    ".entry-content" 
                ], 
                "keywords": [
                    "[itemprop=keywords]::text", 
                    ".entities,_list-itemLink::text"
                ]
            }
        }
    }]
