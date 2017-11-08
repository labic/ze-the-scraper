# -*- coding: utf-8 -*-
from . import ZeSpider


class GloboSpider(ZeSpider):

    name = 'globo'
    allowed_domains = [
                        # 'globo.com'
                        ]
    items_refs = [{
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
                "selectors": {
                    "css": [
                        "[itemprop=author] [itemprop=name]::attr(content)",
                        "[itemprop=author]::text",
                        "[itemprop=creator]::text",
                        "#credito-materia::text",
                        ".autorDataHora strong::text"

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
                        ".autorDataHora::text"

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
                        ".mc-body",
                        ".materia-conteudo",
                        ".entry-content",
                        # ".conteudo",
                        "#texto",
                        'internas-conteudo-primeiro-parag',
                        # '$div > p.internas-conteudo-primeiro-parag'
                        '.col-xs-12.col-md-8.col-md-width-mod'

                    ]
                },
                "contexts": {
                    "improve_html": [
                        "ze.spiders.globo.GloboSpider.improve_html"
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

        to_decompose=['#autor','svg']
        try:
            selector = '.foto'
            for el in html.select(selector):
                fg = html.new_tag('figure')
                fg.append(html.new_tag('img', src=el.select('img')[0]['data-pagespeed-high-res-src']))
                fc = html.new_tag('figcaption')
                fc.string = el.select('figcaption')[0].get_text()
                fg.append(fc)

                el.replace_with(fg)
        except Exception as e:
            exceptions_append(e)


        try:
            selector='.content-media__container'
            for el in html.select(selector):
                fg = html.new_tag('figure')
                fg.append(html.new_tag('img', src=el.select('img')[0]['src']))

                fc = html.new_tag('figcaption')
                fc.string = el.select('.content-media__description span')[0].get_text()
                fg.append(fc)

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

