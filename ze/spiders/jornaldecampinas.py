# -*- coding: utf-8 -*-
from . import ZeSpider


class JornaldeCampinasSpider(ZeSpider):

    name = 'jornaldecampinas'
    allowed_domains = ['jornaldecampinas.com.br']
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
                        # '.wp-image-5984::attr(src)',
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
                        '.node-author-inner strong::text'
                    ]
                }
            },
            "datePublished": {
                "selectors": {
                    "css": [
                        '[itemprop=datePublished]::attr(content)',
                        '.data::text',
                        'p.meta::text',
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
                        '.entry'
                    ]
                },
                "contexts": {
                    "improve_html": [
                        "ze.spiders.jornaldecampinas.JornaldeCampinasSpider.improve_html"
                    ]
                }
            },
            "keywords": {
                "selectors": {
                    "css": [
                        '[itemprop=keywords] a::text',
                        '[rel=tag]::text',
                        '[onclick*=montaURL]::text',
                        '.tags a::text'
                    ]
                }
            }
        }
    }]
    @staticmethod
    def improve_html(html, spider_name=None):
        exceptions = []; exceptions_append = exceptions.append

        to_decompose=["i",'ul','h2','h3']


        try:
            selector = 'u'
            for el in html.select(selector):
                el.unwrap()

            selector = 'img'
            for el in html.select(selector):
                fg = html.new_tag('figure')
                fg.append(html.new_tag('img', src=img['src']))
                img_src = el['src']
                el.replace_with(fg)

            selector = 'span'
            for el in html.select(selector):
                text = el.get_text()
                if text=='':
                    el.decompose()
                else:
                    el.replace_with(text)

            selector = 'p'
            for el in html.select(selector):
                text = el.get_text()
                if text=='':
                    el.decompose()
                # else:
                #     el.replace_with(text)

            selector = 'table'
            for el in html.select(selector):
                ems=el.select('em')
                text=''
                for em in ems:
                    text=text+em.get_text()
                el.replace_with(text)

        except Exception as e:
            exceptions_append(e)

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


