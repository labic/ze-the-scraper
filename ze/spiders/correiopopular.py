# -*- coding: utf-8 -*-
from . import ZeSpider


class CorreioPopularSpider(ZeSpider):

    name = 'correiopopular'
    allowed_domains = ['correio.rac.com.br']
    items_refs = [{
        "spider_name":name,
        "item": "ze.items.creativework.ArticleItem",
        "fields": {
            "name": {
                "selectors": {
                    "css": [
                        "meta[property='og:title']::attr(content)",
                        "meta[name=title]::attr(content)",
                        '[itemprop=headline]::text',
                        '.news-title::text'
                    ]
                }
            },
            "image": {
                "selectors": {
                    "css": [
                        "meta[property='og:image']::attr(content)",
                        '[itemprop="image"] img::attr(src)',
                        '#foto_auto img::attr(src)',
                        '.news-box-picture img::attr(src)',
                    ]
                }
            },
            "description": {
                "selectors": {
                    "css": [
                        "meta[property='og:description']::attr(content)",
                        "meta[name=description]::attr(content)",
                        '[itemprop=description]::attr(content)',
                        '[itemprop=description]::text',
                        '.resumo h2::text'
                    ]
                }
            },
            "author": {
                "selectors": {
                    "css": [
                        '[itemprop=author]::text',
                        '.publish-by b::text'
                    ]
                }
            },
            "datePublished": {
                "selectors": {
                    "css": [
                        '[itemprop=datePublished]::attr(content)',
                        "meta[name='DC.date.created']::attr(content)",
                        '.publish-time::text',#dateModified ta junto

                    ]
                }
            },
            "dateModified": {
                "selectors": {
                    "css": [
                        '[itemprop=dateModified]::attr(content)',
                        '.publish-time::text',#datePublished ta junto
                    ]
                }
            },
            "articleBody": {
                "selectors": {
                    "css": [
                        '[itemprop=articleBody]',
                        '.article-container'
                    ]
                },
                "contexts": {
                    "improve_html": [
                        "ze.spiders.correiopopular.CorreioPopularSpider.improve_html"
                    ]
                }
            },
            "keywords": {
                "selectors": {
                    "css": [
                        '[itemprop=keywords] a::text',
                        '.tags-container a::text',
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
            selector = '#foto_auto'
            for el in html.select(selector):
                fg = html.new_tag('figure')
                images = el.select('img')
                if not(len(images) ==0):
                    for img in images:
                        fg.append(html.new_tag('img', src=img['src']))
                    el.replace_with(fg)

            selector = '.fe-content'
            for el in html.select(selector):
                text=el.get_text()
                el.replace_with(text)
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


