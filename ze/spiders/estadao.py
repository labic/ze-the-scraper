# -*- coding: utf-8 -*-
from . import ZeSpider


class EstadaoSpider(ZeSpider):

    name = 'estadao'
    allowed_domains = ['estadao.com.br']
    items_refs = [{
        "spider_name":name,
        "item": "ze.items.creativework.ArticleItem",
        "fields": {
            "name": {
                "selectors": {
                    "css": [
                        "meta[property='og:title']::attr(content)",
                        "meta[name=title]::attr(content)",
                        "[itemprop=name]::text",
                        ".titulo-principal::text",
                        ".titulo::text",
                        ".n--noticia__title::text",
                        "article h1::text",
                    ]
                }
            },
            "image": {
                "selectors": {
                    "css": [
                        "meta[property='og:description']::attr(content)",
                        "meta[name=description]::attr(content)",
                        'meta[property="og:image"]::attr(content)',
                        "[itemprop=image]::attr(content)",
                        "[property='og:image']::attr(content)"
                    ]
                }
            },
            "description": {
                "selectors": {
                    "css": [
                        "[itemprop=description]::text",
                        ".linha-fina::text",
                        ".n--noticia__subtitle::text",
                        "article p::text",
                    ]
                }
            },
            "author": {
                "selectors": {
                    "css": [
                        "[itemprop=author]::text",
                        ".autor::text",
                        ".author::text",
                        ".n--noticia__state span::text",
                    ]
                }
            },
            "datePublished": {
                "selectors": {
                    "css": [
                        "[itemprop=datePublished]::text",
                        ".data::text",
                        '.n--noticia__state p:nth-child(2)::text'
                    ]
                }
            },
            "dateModified": {
                "selectors": {
                    "css": [
                        "[itemprop=dateModified]::text"
                    ]
                }
            },
            "articleBody": {
                "selectors": {
                    "css": [
                        "[itemprop=articleBody]",
                        ".main-news .content",
                        ".conteudo-materia",
                        ".content",
                        ".main-news .content",
                        ".conteudo-materia",
                        ".entry"
                    ]
                },
                "contexts": {
                    "improve_html": [
                        "ze.spiders.estadao.EstadaoSpider.improve_html"
                    ]
                }
            },
            "keywords": {
                "selectors": {
                    "css": [
                        "[itemprop=keywords] a::text",
                        ".tags a::text",
                        ".tags a span::text",
                        "[itemprop=keywords] a::text",
                        ".tags a::text",
                        ".tags a span::text",
                        "[itemprop=keywords] a::text",
                        ".tags a::text",
                        ".tags a span::text"
                    ]
                }
            }
        }
    }]
    @staticmethod
    def improve_html(html, spider_name=None):
        exceptions = []; exceptions_append = exceptions.append

        to_decompose=[ 'div section p','.documento']
        estadao_media_url = 'http://mdw-mm.estadao.com.br/middlewareAgile/rest/conteudo?tipo_midia={tipo}&idAgile={id}&produto=estadao'

        try:
            selector = '[data-config]'
            for el in html.select(selector):
                media_doc = json.loads(el['data-config'])
                media_url =  self.estadao_media_url if not loader_context.get('media_img_url') else loader_context.get('media_img_url')
                media_url = media_url.format(**media_doc)
                results = requests.get(media_url).json()['resultadoConteudo']['conteudos']

                img_src = ''
                for presset in results[0]['pressets']:
                    if presset['class'] == 'full':
                        img_src = presset['file']
                        break

                fg = html.new_tag('figure')
                fg.append(html.new_tag('img', src=img_src))
                fc = html.new_tag('figcaption')
                fc.string = '{} '.format(results[0]['titulo'])
                s = html.new_tag('small', rel='credits')
                s.string = results[0]['credito']
                fc.append(s)
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

