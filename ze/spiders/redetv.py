# -*- coding: utf-8 -*-
from . import ZeSpider


class RedeTVSpider(ZeSpider):

    name = 'redetv'
    allowed_domains = ['redetv.uol.com.br']
    items_refs = [{
        "spider_name":name,
        "item": "ze.items.creativework.ArticleItem",
        "fields": {
            "name":{
                "selectors": {
                    "css": [
                        "meta[property='og:title']::attr(content)",
                        "meta[name=title]::attr(content)",
                        "[itemprop=name]::text",
                        ".content-head__title::text"
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
                        "[itemprop=alternativeHeadline]::text",
                        ".content-head__subtitle::text"
                    ]
                }
            },
            "author": {
                "default": "RedeTV!",
                "selectors": {
                    "css": [
                        "[itemprop=author] [itemprop=name]::attr(content)",
                        "[itemprop=author]::text",
                        "[itemprop=creator]::text",
                        ".author::text",
                        ".blog-post-date::text",
                        ".credit::text",
                        ".home-item .date-item:nth-child(2) strong::text"
                    ]
                }
            },
            "datePublished": {
                "selectors": {
                    "css": [
                        "[itemprop=datePublished]::attr(datetime)",
                        "[itemprop=datePublished]::text",
                        "meta[name='article:published_time']::attr(content)",
                        "meta[name=dtnoticia]::attr(content)",
                        "#info-edicao-acervo b::text",
                        ".data::text",
                        ".published::text",
                        ".blog-post-time::text",
                        "[property='article:published_time']::attr(content)",
                        ".date-item::text"
                    ]
                }
            },
            "dateModified": {
                "selectors": {
                    "css": [
                        "[itemprop=dateModified]::attr(datetime)" ,
                        "[itemprop=dateModified]::text",
                        "meta[name='article:modified_time']::attr(content)",
                        "updated::text"
                    ]
                }
            },
            "articleBody": {
                "selectors": {
                    "css": [
                        "[itemprop=articleBody]",
                        '[property="na:ArticleBody"]',
                        ".mc-body",
                        ".materia-conteudo",
                        ".entry-content",
                        ".conteudo",
                        ".story",
                        "#content",
                        ".text"
                    ]
                },
                "contexts": {
                    "improve_html": [
                        "ze.spiders.redetv.RedeTVSpider.improve_html"
                    ]
                }
            },
            "keywords": {
                "selectors": {
                    "css": [
                        "meta[name=keywords]::attr(content)",
                        "[itemprop=keywords]::text",
                        ".entities__list-itemLink::text"
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
            selector = 'img'
            for el in html.select(selector):
                fg = html.new_tag('figure')
                fg.append(html.new_tag('img', src=el['src']))
                fc = html.new_tag('figcaption')
                fc.string = el.parent.select('em')[0].string
                fg.append(fc)
                el.parent.select('em')[0].decompose()

                el.replace_with(fg)
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

