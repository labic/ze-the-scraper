# -*- coding: utf-8 -*-
from . import ZeSpider

__all__ = ['G1Spider']


class G1Spider(ZeSpider):

    name = 'g1'
    allowed_domains = ['g1.globo.com']
    items_refs = [{
        "item": "ze.items.creativework.ArticleItem",
        "fields": {
            "name": {
                "selectors": {
                    "css": [
                        "meta[property='og:title']::attr(content)",
                        "meta[name=title]::attr(content)",
                        "[itemprop=name]::text",
                        ".content-head__title::text",
                        ".materia-titulo h1::text",
                        ".entry-title::text"
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
                        ".content-head__subtitle::text",
                        ".materia-titulo h2::text"
                    ]
                }
            },
            "author": {
                "selectors": {
                    "css": [
                        "[itemprop=author] [itemprop=name]::attr(content)",
                        "[itemprop=author]::text",
                        "[itemprop=creator]::text",
                        ".anunciante-publieditorial::text",
                        "#credito-materia::text",
                    ]
                }
            },
            "datePublished": {
                "selectors": {
                    "css": [
                        "[itemprop=datePublished]::attr(datetime)",
                        "[itemprop=datePublished]::text",
                        "time[datetime]::text",
                        "time::attr(datetime)" ,
                        ".data::text"
                    ]
                }
            },
            "dateModified": {
                "selectors": {
                    "css": [
                        "[itemprop=dateModified]::attr(datetime)" ,
                        "[itemprop=dateModified]::text",
                        ".updated"
                    ]
                }
            },
            "articleBody": {
                "selectors": {
                    "css": [
                        "[itemprop=articleBody]",
                        ".materia-conteudo",
                        ".entry-content",
                        ".post-content"
                    ]
                },
                "contexts": {
                    "improve_html": [
                        "ze.spiders.g1.G1Spider.improve_html"
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
    
    # def harvest_metadata(self, resp: Response, item, **kargs):
    #     # TODO: Move to DownloadMiddleware
    #     item['meta']['jsonLDSchemas'] = self.jsonLDSchemas(reponse)
    #     item['meta']['otherLinks'] = self.jsonLD
    
    @staticmethod
    def improve_html(html, spider_name=None):
        exceptions = []; exceptions_append = exceptions.append
        
        try:
            selector = '[data-block-type="backstage-photo"]'
            for el in html.select(selector):
                fg = html.new_tag('figure')
                img_src = el.select_one('img.content-media__image').get('data-src')
                fg.append(html.new_tag('img', src=img_src))
                fc = html.new_tag('figcaption')
                fc.string = el.select_one('.content-media__description__caption').get_text()
                fg.append(fc)
                
                el.replace_with(fg)
        except Exception as e:
            exceptions_append(e)
        
        try:
            selector = '[data-block-type="backstage-video"]'
            for el in html.select(selector):
                video_id = el.select('.content-video__placeholder')[0]['data-video-id']
                
                fg = html.new_tag('figure')
                fg.append(html.new_tag('img', src='https://s02.video.glbimg.com/x720/%s.jpg' % video_id))
                fc = html.new_tag('figcaption')
                fc.string = el.select('[itemprop="description"]')[0].get_text() #antes tava itemprop='caption'
                fg.append(fc)
                a = html.new_tag('a', href='https://globoplay.globo.com/v/%s/' % video_id)
                a.append(fg)
                
                el.replace_with(a)
        except Exception as e:
            exceptions_append(e)
        try:
            for el in html.select('a'):
                el.replace_with(el.get_text())
        except Exception as e:
            exceptions_append(e)
        
        return html, exceptions
