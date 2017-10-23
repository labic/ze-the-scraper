# -*- coding: utf-8 -*-
from . import ZeSpider


class CorreioBrasilienseSpider(ZeSpider):

    name = 'correiobraziliense'
    allowed_domains = ['correiobraziliense.com.br']
    items_refs = [{
        "item": "ze.items.creativework.ArticleItem",
        "fields": {
            "name":  {
                "selectors": {
                    "css": [
                        "meta[property='og:title']::attr(content)",
                        "meta[name=title]::attr(content)",
                        '[itemprop=headline]::text',
                        '.title-post::text',
                        '.news-tit::text'

                    ]
                }
            },
            "image":  {
                "selectors": {
                    "css": [
                        'meta[property="og:image"]::attr(content)',
                        '[itemprop="image"] img::attr(src)',
                        '.lazy::attr("data-lazy-src")'
                    ]
                }
            },
            "description":  {
                "selectors": {
                    "css": [
                        "meta[property='og:description']::attr(content)",
                        "meta[name=description]::attr(content)",
                        '[itemprop=description]::attr(content)',
                        '[itemprop=description]::text'
                    ]
                }
            },
            "author":  {
                "selectors": {
                    "css": [
                        # '[itemprop=author]::text',
                        # '[class*=autor]::text',
                        '.autor_casa::text',
                        '.autor_agencia::text',
                        '.author a::text',
                        '[onclick*=malito] span::text'
                    ]
                }
            },
            "datePublished":  {
                "selectors": {
                    "css": [
                        '[itemprop=datePublished]::attr(content)',
                        '.entry-date::text',
                        '[name="DC.date.created"]::attr(content)'
                    ]
                }
            },
            "dateModified":  {
                "selectors": {
                    "css": [
                        '[itemprop=dateModified]::attr(content)'
                    ]
                }
            },
            "articleBody":  {
                "selectors": {
                    "css": [
                        '[itemprop=articleBody]',
                        '.entry-content'
                    ]
                },
                "contexts": {
                    "improve_html": [
                        "ze.spiders.correiobraziliense.CorreioBrasilienseSpider.improve_html"
                    ]
                }
            },
            "keywords":  {
                "selectors": {
                    "css": [
                        '[itemprop=keywords] a::text',
                        '[rel=tag]::text',
                        '[onclick*=montaURL]::text'
                    ]
                }
            }
        }
    }]
    @staticmethod
    def improve_html(html, spider_name=None):
        exceptions = []; exceptions_append = exceptions.append
        try:
            selector = 'section'
            for el in html.select(selector):
                fg = html.new_tag('figure')
                images = el.select('img')

                if not(len(images) ==0):
                    for img in images:
                        fg.append(html.new_tag('img', src=img['src']))
                    el.replace_with(fg)

            selector = 'div'
            for el in html.select(selector):
                el.name = 'p'

            selector = 'br'
            for el in html.select(selector):
                el.decompose()

            selector = 'h3'
            for el in html.select(selector):
                el.name = 'h2'
            selector = 'p'
            for el in html.select(selector):
                if el.get_text() == '':
                    el.decompose()
        except Exception as e:
            exceptions_append(e)


        try:
            for el in html.select('a'):
                el.replace_with(el.get_text())
        except Exception as e:
            exceptions_append(e)

        return html, exceptions
