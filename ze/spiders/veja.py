# -*- coding: utf-8 -*-
from . import ZeSpider


class VejaSpider(ZeSpider):

    name = 'veja'
    allowed_domains = ['veja.abril.com.br']
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
                        "[property=og:image]::attr(content)"
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
                        "[itemprop=author]::text",
                        ".article-author span strong::text",
                        ".article-author span::text"
                    ]
                }
            },
            "datePublished": {
                "selectors": {
                    "css": [
                        "[itemprop=datePublished]::text",
                        ".article-date span::text",
                        ".entry-date::text",

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
                        ".article-content"
                    ]
                },
                "contexts": {
                    "improve_html": [
                        "ze.spiders.veja.VejaSpider.improve_html"
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

        try:
            selector = '.featured-image'
            for el in html.select(selector):
                fg = html.new_tag('figure')
                fg.append(html.new_tag('img', src=el.select('img')[0]['data-src']))
                fc = html.new_tag('figcaption')
                fc.string = el.select('p')[0].string
                fg.append(fc)

                el.replace_with(fg)
        except Exception as e:
            exceptions_append(e)

        try:
            selector = 'p span iframe[src*="https://www.youtubel.com/embed"]'
            for el in html.select(selector):
                video_id = el['data-lazy-src'].split('/')[4]
                fm = html.new_tag('iframe', src='https://www.youtubel.com/embed/%s?rel=0' % video_id,
                    width='1280', height='720', frameborder='0', allowfullscreen='true')
        except Exception as e:
            exceptions_append(e)

        try:
            for el in html.select('a'):
                el.replace_with(el.get_text())
        except Exception as e:
            exceptions_append(e)

        return html, exceptions

