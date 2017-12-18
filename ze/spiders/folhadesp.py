# -*- coding: utf-8 -*-
from . import ZeSpider


class FolhaDeSaoPauloSpider(ZeSpider):

    name = 'folhadesp'
    allowed_domains = ['folha.uol.com.br']
    items_refs = [{
        "spider_name":name,
        "item": "ze.items.creativework.ArticleItem",
        "fields": {
            "name": {
                "selectors": {
                    "css": [
                        "meta[property='og:title']::attr(content)",
                        "meta[name=title]::attr(content)",
                        ".news header h1::text",
                        "[itemprop=name]::text",
                        "[itemprop='headline']::text",
                        "[itemprop=alternativeHeadline]::attr(content)",
                        # MOBILE
                        "h1::text",
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
                        "[property='og:image']::attr(content)",
                        # MOBILE
                        ".gallery img::attr(src)"
                    ]
                }
            },
            "description": {
                "selectors": {
                    "css": [
                        ".documentDescription::text",
                        "[itemprop=description]::text",
                        '[property="og:description"]::attr(content)'
                    ]
                }
            },
            "author": {
                "selectors": {
                    "css": [
                        ".news .author p b",
                        "[itemprop=author] b::text",
                        ".news__byline p strong::text",
                        '.post-autor::text',
                        # MOBILE
                        '.meta .credits p b::text'

                    ]
                }
            },
            "datePublished": {
                "selectors": {
                    "css": [
                        ".news time::attr(datetime)",
                        "[itemprop=datePublished]::text",
                        '[property="article:published_time"]::attr(content)',
                        'article time::attr(datetime)',
                        '.post-date',
                        '.news header time::attr(datetime)',
                        # MOBILE
                        '.meta .date::text'
                    ]
                }
            },
            "dateModified": {
                "selectors": {
                    "css": [
                        "[itemprop=dateModified]::text",
                        '[property="article:modified_time"]::attr(content)'
                    ]
                }
            },
            "articleBody": {
                "selectors": {
                    "css": [
                        ".news .content",
                        "[itemprop=articleBody]",
                        ".single-post-content",
                        ".text--container",
                        # MOBILE
                        ".content-type-news"
                    ]
                },
                "contexts": {
                    "improve_html": [
                        "ze.spiders.folhadesp.FolhaDeSaoPauloSpider.improve_html"
                    ]
                }
            },
            "keywords": {
                "selectors": {
                    "css": [
                        "meta[name=keywords]::attr(content)",
                        "[itemprop=keywords]::text",
                        "[itemprop=keywords]::attr(content)",
                        # MOBILE
                        ".tags-related-box a::text"
                    ]
                }
            }
        }
    }]

    @staticmethod
    def improve_html(html, spider_name=None):
        exceptions = []; exceptions_append = exceptions.append

        to_decompose=[ 'h5']
        try:

            selector = '.gallery'
            for el in html.select(selector):
                href = el.select_one('a')['href'].rsplit('#')[0]
                result = requests.get(''.join((href, '.json'))).json()

                section = html.new_tag('section')
                h1 = html.new_tag('h1')
                h1.string = result['gallery']['title']
                section.append(h1)
                h2 = html.new_tag('h2')
                h2.string = result['gallery']['description']
                section.append(h2)

                for image in result['images']:
                    fg = html.new_tag('figure')

                    img = html.new_tag('img', src=image['image_gallery'])
                    fg.append(img)
                    fc = html.new_tag('figcaption')
                    fc.string = image['legend']
                    small = html.new_tag('small')
                    small.string = image['author']
                    fc.insert(1, small)
                    fg.append(fc)

                    section.append(fg)

                el.replace_with(section)

        except Exception as e:
            exceptions_append(e)

        try:
            print(html)
            for el in html.select('.video'):

                section=html.new_tag('section')
                if len(html.select('img'))>0:
                    fg = html.new_tag('figure')

                    img = html.new_tag('img', src=html.select('img')[0]['src'])
                    fg.append(img)

                    section.append(fg)
                if len(html.select('iframe'))>0:
                    link = html.new_tag('a',href = html.select('iframe')[0]['src'])
                    section.append()


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

