# -*- coding: utf-8 -*-
from . import ZeSpider


class EstadoDeMinasSpider(ZeSpider):

    name = 'estadodeminas'
    allowed_domains = ['em.com.br','uai.com.br']
    items_refs = [{
        "item": "ze.items.creativework.ArticleItem",
        "fields": {
            "name": {
                "selectors": {
                    "css": [
                        "meta[property='og:title']::attr(content)",
                        "meta[name=title]::attr(content)",
                        '[itemprop=headline]::text',
                        '.title-post::text',
                        '.entry-title::text'
                    ]
                }
            },
            "image": {
                "selectors": {
                    "css": [
                        "meta[property='og:description']::attr(content)",
                        "meta[name=description]::attr(content)",
                        'meta[property="og:image"]::attr(content)',
                        '[itemprop="image"]::attr(src)',
                        '.lazy::attr("data-lazy-src")'
                    ]
                }
            },
            "description": {
                "selectors": {
                    "css": [
                        '[itemprop=description]::attr(content)',
                        '[itemprop=description]::text',
                        '.entry-content h2::text',
                        '.linha-fina::text',
                        '.entry-content blockquote p::text'
                    ]
                }
            },
            "author": {
                "selectors": {
                    "css": [
                        '[itemprop=author]::text',
                        '.author a::text',
                        '[href*="mailto"]::text'
                    ]
                }
            },
            "datePublished": {
                "selectors": {
                    "css": [
                        '[itemprop=datePublished]::attr(content)',
                        '.entry-date::text'
                    ]
                }
            },
            "dateModified": {
                "selectors": {
                    "css": [
                        '[itemprop=dateModified]::attr(content)'
                    ]
                }
            },
            "articleBody": {
                "selectors": {
                    "css": [
                        '[itemprop=articleBody]',
                        '.entry-content'
                    ]
                },
                "contexts": {
                    "improve_html": [
                        "ze.spiders.estadodeminas.EstadoDeMinasSpider.improve_html"
                    ]
                }
            },
            "keywords": {
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

    # def harvest_metadata(self, resp: Response, item, **kargs):
    #     # TODO: Move to DownloadMiddleware
    #     item['meta']['jsonLDSchemas'] = self.jsonLDSchemas(reponse)
    #     item['meta']['otherLinks'] = self.jsonLD

    @staticmethod
    def improve_html(html, spider_name=None):
        exceptions = []; exceptions_append = exceptions.append

        to_decompose=['.read-more-widget',]
        try:
            for item in to_decompose:
                for el in html.select(item):
                    el.decompose()
        except Exception as e:
            exceptions_append(e)
        try:
            for el in html.select('a'):
                # print(el.get_text().strip('\n'))
                el.replace_with(el.get_text().strip('\n'))
        except Exception as e:
            exceptions_append(e)


        return html, exceptions

