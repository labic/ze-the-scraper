# -*- coding: utf-8 -*-
from . import ZeSpider


class IstoESpider(ZeSpider):

    name = 'istoe'
    allowed_domains = ['istoe.com.br']
    items_refs = [{
        "item": "ze.items.creativework.ArticleItem",
        "fields": {
            "name": {
                "selectors": {
                    "css": [
                        "meta[property='og:title']::attr(content)",
                        "meta[name=title]::attr(content)",
                        "[itemprop=name]::text",
                        ".article-title::text"
                    ]
                }
            },
            "image": {
                "selectors": {
                    "css": [
                        'meta[property="og:image"]::attr(content)',
                        "[itemprop=image]::attr(content)",
                        "[property=og:image]::attr(content)",
                        '.teaser img::attr(src)'
                    ]
                }
            },
            "description": {
                "selectors": {
                    "css": [
                        "meta[property='og:description']::attr(content)",
                        "meta[name=description]::attr(content)",
                        "[itemprop=description]::text",
                        ".article-subtitle::text"
                    ]
                }
            },
            "author": {
                "selectors": {
                    "css": [
                        # "[itemprop=author]::text",
                        # ".article-author span strong::text",
                        # '.author:not(figcaption)::text',
                        "[rel=author] a::text",
                        "[rel=author]::text",
                    ]
                }
            },
            "datePublished": {
                "selectors": {
                    "css": [
                        "[itemprop=datePublished]::text",
                        ".article-date span::text",
                        ".entry-date::text",
                        '.content-section time::attr(datetime)'
                    ]
                }
            },
            "dateModified": {
                "selectors": {
                    "css": [
                        "[itemprop=dateModified]::text",
                        ".article-date span::text"
                    ]
                }
            },
            "articleBody": {
                "selectors": {
                    "css": [
                        "[itemprop=articleBody]",
                        '.content-section.content',
                        ".article-content"
                    ]
                },
                "contexts": {
                    "improve_html": [
                        "ze.spiders.istoe.IstoESpider.improve_html"
                    ]
                }
            },
            "keywords": {
                "selectors": {
                    "css": [
                        "[itemprop=keywords]::text",
                        ".article-tags a::text"
                    ]
                }
            }
        }
    }]
    @staticmethod
    def improve_html(html, spider_name=None):
        exceptions = []; exceptions_append = exceptions.append

        to_decompose=[]

        # try:
        #     for el in html.select('a'):
        #         el.replace_with(el.get_text())
        # except Exception as e:
        #     exceptions_append(e)
        try:
            for item in to_decompose:
                for el in html.select(item):
                    el.decompose()
        except Exception as e:
            exceptions_append(e)

        return html, exceptions

