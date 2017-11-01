# -*- coding: utf-8 -*-
from . import ZeSpider


class BandSpider(ZeSpider):

    name = 'band'
    allowed_domains = ['band.uol.com.br']
    items_refs = [{
        "item": "ze.items.creativework.ArticleItem",
        "fields": {
            "name": {
                "selectors": {
                    "css": [
                        '.titMat::text',
                        "meta[property='og:title']::attr(content)",
                        "meta[name=title]::attr(content)",
                        "[itemprop=name]::text",
                        "#materia_interna h1::text",
                    ]
                }
            },
            "image": {
                "selectors": {
                    "css": [
                        'meta[property="og:image"]::attr(content)',
                        "[itemprop=image]::attr(content)",
                        "[property='og:image']::attr(content)"
                    ]
                }
            },
            "description":  {
                "selectors": {
                    "css": [
                        "meta[property='og:description']::attr(content)",
                        "meta[name=description]::attr(content)",
                        "[itemprop=description]::text",
                        "[itemprop=alternativeHeadline]::text",
                        "#materia_interna h2::text"
                    ]
                }
            },
            "author": {
                "selectors": {
                    "css": [
                        # "[itemprop=author]::text",
                        "[itemprop=creator]::text",
                        "#mat_autor_nome::text"
                    ]
                }
            },
            "datePublished": {
                "selectors": {
                    "css": [
                        "[itemprop=datePublished]::attr(datetime)",
                        "[itemprop=datePublished]::attr(content)",
                        "[itemprop=datePublished]::text",
                        "time[datetime]::text",
                        "time::attr(datetime)",
                        ".datahora::text"
                    ]
                }
            },
            "dateModified": {
                "selectors": {
                    "css": [
                        "[itemprop=dateModified]::attr(datetime)" ,
                        "[itemprop=dateModified]::text",
                        ".updated"
                    ]
                }
            },
            "articleBody": {
                "selectors": {
                    "css": [
                       "[itemprop=articleBody]",
                        "#materia_interna"
                    ]
                },
                "contexts": {
                    "improve_html": [
                        "ze.spiders.band.BandSpider.improve_html"
                    ]
                }
            },
            "keywords": {
                "selectors": {
                    "css": [
                        "meta[name=keywords]::attr(content)",
                        "[itemprop=keywords]::text",
                        "[itemprop=keywords]::attr(content)"
                    ]
                }
            }
        }
    }]


    @staticmethod
    def improve_html(html, spider_name=None):
        exceptions = []; exceptions_append = exceptions.append
        to_decompose=['.cp-share-list-entry-share',
                        '.alert-warning',
                        '.cp-content-list-links']

        try:
            for item in to_decompose:
                for el in html.select(item):
                    el.decompose()
        except Exception as e:
            exceptions_append(e)

        try:
            for el in html.select('a'):
                el.replace_with(el.get_text())
        except Exception as e:
            exceptions_append(e)


        return html, exceptions

