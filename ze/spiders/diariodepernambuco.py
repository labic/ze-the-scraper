# -*- coding: utf-8 -*-
from . import ZeSpider


class DiarioDePernambucoSpider(ZeSpider):

    name = 'diariodepernambuco'
    allowed_domains = ['diariodepernambuco.com.br']
    items_refs = [{
        "spider_name":name,
        "item": "ze.items.creativework.ArticleItem",
        "fields": {
            "name": {
                "selectors": {
                    "css": [
                        #pra blog
                        # '.entry-title a::text',
                        #pra principal
                        "meta[property='og:title']::attr(content)",
                        "meta[name=title]::attr(content)",
                        '[itemprop=headline]::text',
                        '.h1::text',
                        'div.et_pb_text_align_center::text',
                        #para blog
                        '.entry-title::text',
                        '.entry-heading a::text',

                    ]
                }
            },
            "image": {
                "selectors": {
                    "css": [
                        'meta[property="og:image"]::attr(content)',
                        '[itemprop="image"] img::attr(src)',
                        'table.image tbody tr td img::attr(src)',
                        # '.image img::attr(src)'
                        #blog
                        '.entry-content img::attr(src)'
                    ]
                }
            },
            "description": {
                "selectors": {
                    "css": [
                        "meta[property='og:description']::attr(content)",
                        "meta[name=description]::attr(content)",
                        '[itemprop=description]::attr(content)',
                        '[itemprop=description]::text'
                    ]
                }
            },
            "author": {
                "selectors": {
                    "css": [
                        '[itemprop=author]::text',
                        '.yellowlight::text',
                        #blog
                        '.author a::text',
                        '.post-meta > a::text',
                        # '.author a::attr(title)',

                    ]
                }
            },
            "datePublished": {
                "selectors": {
                    "css": [
                        '[itemprop=datePublished]::attr(content)',
                        '.data::text',
                        '[property="article:published_time"]::attr(content)',
                        #para blog
                        '.entry-date::attr(datetime)',
                        '.date::text',
                        '.published::text',
                        '[name="DC.date.created"]::attr(content)'
                    ]
                }
            },
            "dateModified": {
                "selectors": {
                    "css": [
                        '[itemprop=dateModified]::attr(content)',
                        '[property="article:modified_time"]::attr(content)',
                    ]
                }
            },
            "articleBody": {
                "selectors": {
                    "css": [
                        '[itemprop=articleBody]',
                        '[id = abanoticia] ',
                        #blog
                        '.entry-text',
                        '.entry-content'
                    ]
                },
                "contexts": {
                    "improve_html": [
                        "ze.spiders.diariodepernambuco.DiarioDePernambucoSpider.improve_html"
                    ]
                }
            },
            "keywords": {
                "selectors": {
                    "css": [
                        '[itemprop=keywords] a::text',
                        '[rel=tag]::text',
                        '[onclick*=montaURL]::text',
                        '.tags_noticias a::text',
                        #blog
                        '.entry-meta a::text'
                    ]
                }
            }
        }
    }]
    @staticmethod
    def improve_html(html, spider_name=None):
        exceptions = []; exceptions_append = exceptions.append

        to_decompose=['a',]

        try:
            selector = 'table'
            for el in html.select(selector):
                fg = html.new_tag('figure')
                images = el.select('img')
                if not(len(images) ==0):
                    for img in images:
                        fg.append(html.new_tag('img', src=img['src']))
                    el.replace_with(fg)
                # el.replace_with(src)

            selector = 'div'
            for el in html.select(selector):
                el.unwrap()

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

