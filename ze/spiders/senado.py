# -*- coding: utf-8 -*-
from . import ZeSpider


class SenadoSpider(ZeSpider):
    name = 'senado'
    allowed_domains = ['senado.leg.br']
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
                        "#tituloNoticia h2::text",
                        ".tituloVerNoticia::text"
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
            "audio": {
                "item": "ze.items.creativework.AudioObjectItem",
                "fields": {
                    "url": {
                        "selectors": {
                            "css": [
                                '#downloadAudio a ::attr(href)',
                                '.Control--download ::attr(href)'
                            ]
                        }
                    }
                }
            },
            "author": {
                "selectors": {
                    "css": [
                        '[itemprop=author]::text',
                        '[class*=autor]::text',
                        '#materia > p small::text',
                        '.ByLine-autor a::text',
                        # '.editoriaVerNoticia b::text'
                    ]
                }
            },
            "datePublished": {
                "selectors": {
                    "css": [
                        '[itemprop=datePublished]::attr(content)',
                        '.datahoraNoticia::text',
                        '#materia span.text-muted::text',
                        '.ByLine-data::text',
                        '.editoriaVerNoticia::text',
                        '#materia span.text-muted::text'
                    ]
                }
            },
            "dateModified": {
                "selectors": {
                    "css": [
                        '[itemprop=dateModified]::attr(content)',
                        '#materia span.text-muted::text',
                    ]
                }
            },
            "articleBody": {
                "selectors": {
                    "css": [
                        '[itemprop=articleBody]',
                        '[property=articleBody]',
                        '#textoMateria',
                        '#content',
                        '.textoNovo'
                    ]
                },
                "contexts": {
                    "improve_html": [
                        "ze.spiders.senado.SenadoSpider.improve_html"
                    ]
                }
            },
            "keywords": {
                "selectors": {
                    "css": [
                        '[itemprop=keywords] a::text',
                        '[rel=tag]::text',
                        '[name=keywords]::attr(content)'
                    ]
                }
            },
        }
    }]
    @staticmethod
    def improve_html(html, spider_name=None):
        exceptions = []; exceptions_append = exceptions.append

        to_decompose=[  'h1',
                        '#viewlet-below-content-title',
                        '#viewlet-above-content-body',
                        '.ByLine'
                    ]

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

