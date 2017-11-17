# -*- coding: utf-8 -*-
from . import ZeSpider


class CartaEducacaoSpider(ZeSpider):

    name = 'cartaeducacao'
    allowed_domains = ['cartaeducacao.com.br']
    items_refs = [{
        "spider_name":name,
        "item": "ze.items.creativework.ArticleItem",
        "fields": {
            "name": {
                "selectors": {
                    "css": [
                        "meta[property='og:title']::attr(content)",
                        "meta[name=title]::attr(content)",
                        "[itemprop=name]::text",
                        ".documentFirstHeading::text"
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
            "description": {
                "selectors": {
                    "css": [
                        "meta[property='og:description']::attr(content)",
                        "meta[name=description]::attr(content)",
                        "[itemprop=description]::text",
                        ".documentDescription::text"
                    ]
                }
            },
            "author": {
                "selectors": {
                    "css": [
                        "[itemprop=author]::text",
                        ".documentAuthor a::text",
                        ".documentAuthor::text",
                        ".td-post-author-name::text"
                    ]
                }
            },
            "datePublished": {
                "selectors": {
                    "css": [
                        "[itemprop=datePublished]::attr(content)",
                        ".documentPublished::text"
                    ]
                }
            },
            "dateModified": {
                "selectors": {
                    "css": [
                        "[itemprop=dateModified]::text",
                        '.documentModified::text'
                    ]
                }
            },
            "articleBody": {
                "selectors": {
                    "css": [
                        "[itemprop=articleBody]",
                        "#content-core",
                        ".td-post-content"
                    ]
                },
                "contexts": {
                    "improve_html": [
                        "ze.spiders.cartaeducacao.CartaEducacaoSpider.improve_html"
                    ]
                }
            },
            "keywords": {
                "selectors": {
                    "css": [
                        "[itemprop=keywords]::text",
                        "[property='rnews:keywords']::text",
                        "[rel='tag']::text",
                        "#category .link-category::text"
                    ]
                }
            }
        }
    }]
    @staticmethod
    def improve_html(html, spider_name=None):
        exceptions = []; exceptions_append = exceptions.append

        to_decompose=[]

        try:
            selector = '.image-inline'
            for el in html.select(selector):
                fg = html.new_tag('figure')
                fg.append(html.new_tag('img', src=el.select('img')[0]['data-src']))
                fc = html.new_tag('figcaption')
                fc.string = el.select('.image-caption')[0].string
                fg.append(fc)

                el.replace_with(fg)
        except Exception as e:
            exceptions_append(e)


        try:
            selector = '.tile-rights'
            for i, el in enumerate(html.select(selector)):
                fg = html.new_tag('figure')
                img = html.select('.canvasImg img')[i]
                fg.append(html.new_tag('img', src=img['data-src']))
                fc = html.new_tag('figcaption')
                fc.string = el.select('span')[0].string
                fg.append(fc)

                el.replace_with(fg)
                img.parent.decompose()

        except Exception as e:
            exceptions_append(e)

        try:
            for el in html.select('a'):
                el.replace_with(el.get_text())
        except Exception as e:
            exceptions_append(e)
        try:
            for item in to_decompose:
                for el in html.select(item):
                    el.decompose()
        except Exception as e:
            exceptions_append(e)

        return html, exceptions
