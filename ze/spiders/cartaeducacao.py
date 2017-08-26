# -*- coding: utf-8 -*-

from ze.spiders import ZeSpider

class CartaEducacaoSpider(ZeSpider):

    name = 'cartaeducacao'
    allowed_domains = ['cartaeducacao.com.br']
    parses = [{
        "ze.items.creativework.ArticleItem": {
            "fields": {
                "name": [
                    "meta[property='og:title']::attr(content)",
                    "meta[name=title]::attr(content)",
                    "[itemprop=name]::text",
                    ".documentFirstHeading::text"
                ],
                "image": [
                    'meta[property="og:image"]::attr(content)',
                    "[itemprop=image]::attr(content)",
                    "[property='og:image']::attr(content)"
                ],
                "description": [
                    "meta[property='og:description']::attr(content)",
                    "meta[name=description]::attr(content)",
                    "[itemprop=description]::text",
                    ".documentDescription::text"
                ],
                "author": [
                    "[itemprop=author]::text",
                    ".documentAuthor a::text",
                    ".documentAuthor::text",
                    ".td-post-author-name::text"
                ],
                "datePublished": [
                    "[itemprop=datePublished]::attr(content)",
                    ".documentPublished::text"
                ],
                "dateModified": [
                    "[itemprop=dateModified]::text",
                    '.documentModified::text'
                ],
                "articleBody": [
                    "[itemprop=articleBody]",
                    "#content-core",
                    ".td-post-content",
                ],
                "keywords": [
                    "[itemprop=keywords]::text",
                    "[property='rnews:keywords']::text",
                    "[rel='tag']::text",
                    "#category .link-category::text"
                ]
            }
        }
    }]
