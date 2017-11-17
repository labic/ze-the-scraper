# -*- coding: utf-8 -*-=
from . import ZeSpider

class MundoEducacaoSpider(ZeSpider):

    name = 'mundoeducacao'
    allowed_domains = ['mundoeducacao.bol.uol.com.br',
                        'vestibular.mundoeducacao.bol.uol.com.br']
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
                        '.node-author-inner strong::text',
                        '.publicado b::text',
                    ]
                }
            },
            "datePublished": {
                "selectors": {
                    "css": [
                        '[itemprop=datePublished]::attr(content)',
                        '[itemprop="datePublished"]::attr(content)',
                        '.data::text',
                        'p.meta::text',
                        # '.publicado p',
                        '.publicado::text'
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
                        '.entry',
                        '.post'
                    ]
                },
                "contexts": {
                    "improve_html": [
                        "ze.spiders.mundoeducacao.MundoEducacaoSpider.improve_html"
                    ]
                }
            },
            "keywords": {
                "selectors": {
                    "css": [
                        '[name="news_keywords"]::attr(content)',
                        '[itemprop=keywords] a::text',
                        '[rel=tag]::text',
                        '[onclick*=montaURL]::text',
                        '.publicado a::text'
                    ]
                }
            }
        }
    }]

    @staticmethod
    def improve_html(html, spider_name=None):
        exceptions = []; exceptions_append = exceptions.append

        # try:
        #     selector = '[data-block-type="backstage-photo"]'
        #     for el in html.select(selector):
        #         fg = html.new_tag('figure')
        #         img_src = el.select_one('img.content-media__image').get('data-src')
        #         fg.append(html.new_tag('img', src=img_src))
        #         fc = html.new_tag('figcaption')
        #         fc.string = el.select_one('.content-media__description__caption').get_text()
        #         fg.append(fc)

        #         el.replace_with(fg)
        # except Exception as e:
        #     exceptions_append(e)

        # try:
        #     selector = '[data-block-type="backstage-video"]'
        #     for el in html.select(selector):
        #         video_id = el.select('.content-video__placeholder')[0]['data-video-id']

        #         fg = html.new_tag('figure')
        #         fg.append(html.new_tag('img', src='https://s02.video.glbimg.com/x720/%s.jpg' % video_id))
        #         fc = html.new_tag('figcaption')
        #         fc.string = el.select('[itemprop="description"]')[0].get_text() #antes tava itemprop='caption'
        #         fg.append(fc)
        #         a = html.new_tag('a', href='https://globoplay.globo.com/v/%s/' % video_id)
        #         a.append(fg)

        #         el.replace_with(a)
        # except Exception as e:
        #     exceptions_append(e)
        try:
            for el in html.select('a'):
                el.replace_with(el.get_text())
        except Exception as e:
            exceptions_append(e)

        return html, exceptions
