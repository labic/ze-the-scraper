# -*- coding: utf-8 -*-
from . import ZeSpider


class CamaraSpider(ZeSpider):

    name = 'camara'
    allowed_domains = ['camara.leg.br']
    items_refs = [{
        "spider_name":name,
        "item": "ze.items.creativework.ArticleItem",
        "fields": {
            "name": {
                "selectors": {
                    "css": [
                        "meta[property='og:title']::attr(content)",
                        "meta[name=title]::attr(content)",
                        "[itemprop=headline]::text",
                        "#tituloNoticia h2::text"
                    ]
                }
            },
            "image": {
                "selectors": {
                    "css": [
                        'meta[property="og:image"]::attr(content)',
                        '[itemprop="image"] img::attr(src)',
                        '.imagem img::attr("src")',

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
                        '[class*=autor]::text',
                        '#creditosMateria span:first-child::text'
                    ]
                }
            },
            "datePublished": {
                "selectors": {
                    "css": [
                        '[itemprop=datePublished]::attr(content)',
                        '.datahoraNoticia::text'
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
                '[property=articleBody]',
                '#conteudoNoticia'
                    ]
                },
                "contexts": {
                    "improve_html": [
                        "ze.spiders.camara.CamaraSpider.improve_html"
                    ]
                }
            },
            "keywords": {
                "selectors": {
                    "css": [
                        '[itemprop=keywords] a::text',
                        '[rel=tag]::text',
                        '[name=agenciapalavraschave]::attr(content)'
                    ]
                }
            },
        }
    }]

    @staticmethod
    def improve_html(html, spider_name=None):
        exceptions = []; exceptions_append = exceptions.append

        to_decompose=[]

        try:
            selector = '.js-pageplayer'
            for el in html.select(selector):
                # transcricao =el.select('.Songs-transcricao p')[0].get_text()
                # print(transcricao)
                transc_tag=html.new_tag('div')
                transc_tag.append(el.select('.Songs-transcricao p')[0].get_text())
                transc_tag['id']='transcricao'
                el.clear()
                # print('\nel \n', transc_tag, '\n fim el \n')
                # el.append(transcricao)
                el.replace_with(transc_tag)

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

