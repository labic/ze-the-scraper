# -*- coding: utf-8 -*-
from . import ZeSpider


class HuffPostBrasilSpider(ZeSpider):

    name = 'huffpostbrasil'
    allowed_domains = ['huffpostbrasil.com']
    items_refs = [{
        "item": "ze.items.creativework.ArticleItem",
        "fields": {
            "name": {
                "selectors": {
                    "css": [
                        "meta[property='og:title']::attr(content)",
                        "meta[property='twitter:title']::attr(content)",
                        "meta[name=title]::attr(content)",
                        "[itemprop=name]::text",
                        ".headline__title::text"
                    ]
                }
            },
            "image": {
                "selectors": {
                    "css": [
                        'meta[property="og:image"]::attr(content)',
                        'meta[property="twitter:image"]::attr(content)',
                        "[itemprop=image]::attr(content)"
                    ]
                }
            },
            "description": {
                "selectors": {
                    "css": [
                        "meta[property='og:description']::attr(content)",
                        "meta[property='twitter:description']::attr(content)",
                        "meta[name='description']::attr(content)",
                        "meta[name=description]::attr(content)",
                        "[property=description]::attr(content)"
                    ]
                }
            },
            "author": {
                "selectors": {
                    "css": [
                        "[itemprop=author]::text",
                        "[itemprop=creator] [itemprop=name]::text",
                        ".author-card__details__name::text"
                    ]
                }
            },
            "datePublished": {
                "selectors": {
                    "css": [
                        "[itemprop=datePublished]::text",
                        ".timestamp__date--published::text"
                    ]
                }
            },
            "dateModified": {
                "selectors": {
                    "css": [
                        "[itemprop=dateModified]::text",
                        ".timestamp__date--modified::text"
                    ]
                }
            },
            "articleBody": {
                "selectors": {
                    "css": [
                        '[data-part="contents"]',
                        "[itemprop=articleBody]",
                        ".entry__body",
                        ".post-contents"
                    ]
                },
                "contexts": {
                    "improve_html": [
                        "ze.spiders.huffpostbrasil.HuffPostBrasilSpider.improve_html"
                    ]
                }
            },
            "keywords": {
                "selectors": {
                    "css": [
                        "meta[property='keywords']::attr(content)",
                        "[itemprop=keywords]::text"
                    ]
                }
            },
        }
    }]
    @staticmethod
    def improve_html(html, spider_name=None):
        exceptions = []; exceptions_append = exceptions.append

        to_decompose = ['blockquote',
                        '.related-entries',
                        '#suggest-corrections']
        try:
            for item in to_decompose:
                for el in html.select(item):
                    el.decompose()
        except Exception as e:
            exceptions_append(e)


        # try:
        #     for el in html.select('a'):
        #         el.replace_with(el.get_text())
        # except Exception as e:
        #     exceptions_append(e)

        return html, exceptions

