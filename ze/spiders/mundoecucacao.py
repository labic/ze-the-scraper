# -*- coding: utf-8 -*-=
from . import ZeSpider

class MundoEducacaoSpider(ZeSpider):

    name = 'mundoeducacao'
    allowed_domains = ['mundoeducacao.bol.uol.com.br']
    items_refs = [{
        "item": "ze.items.creativework.ArticleItem",
        "fields": { 
            "name": {
                "selectors": {
                    "css": [
                        "meta[property='og:title']::attr(content)",
                        "meta[name=title]::attr(content)",
                        '[itemprop=headline]::text',
                        'h2.post a::text'
                    ]
                }
            },
            "image": {
                "selectors": {
                    "css": [
                        'meta[property="og:image"]::attr(content)',
                        '[itemprop="image"] img::attr(src)',                        
                        '[class*= "wp-image"]::attr(src)',
                        '.main-single::attr(src)'
                    ]
                }
            },
            "description": {
                "selectors": {
                    "css": [
                        "meta[property='og:description']::attr(content)",
                        "meta[name=description]::attr(content)",
                        '[itemprop=description]::attr(content)',
                        '.entry p i::text'
                    ]
                }
            },
            "author": {
                "selectors": {
                    "css": [
                        '[itemprop=author]::text',
                        '.autor-nome::text',
                        '.node-author-inner strong::text',
                        '.publicado b::text',
                    ]
                }
            },
            "datePublished": {
                "selectors": {
                    "css": [
                        '[itemprop=datePublished]::attr(content)',
                        '.data::text',
                        'p.meta::text',
                        '.publicado p',
                        '.publicado::text'
                    ]
                }
            },
            "dateModified": {
                "selectors": {
                    "css": [
                        '[itemprop=dateModified]::attr(content)',
                        '.node-body p em::text'
                    ]
                }
            },
            "articleBody": {
                "selectors": {
                    "css": [
                        '[itemprop=articleBody]',
                        '.entry',
                        '.post'
                    ]
                }
            },
            "keywords": {
                "selectors": {
                    "css": [
                        '[itemprop=keywords] a::text',
                        '[rel=tag]::text',
                        '[onclick*=montaURL]::text',                        
                        '.publicado a::text'
                    ]
                }
            }
        }        
    }]