# -*- coding: utf-8 -*-

from ze.spiders import ZeSpider

class GestaoEscolarSpider(ZeSpider):

    name = 'gestaoescolar'
    allowed_domains = ['gestaoescolar.org.br']
    parses = [{
        "ze.items.creativework.ArticleItem": {
            "fields": {
                "name":[
                    '[itemprop=headline]::text',
                    '.materia h1::text'
                ],
                "image":[
                    # '[itemprop="image" img::attr(src)]',
                    '.wp-caption img::attr(src)'
                ],
                "description":[
                    '[itemprop=description]::attr(content)',
                    '[itemprop=description]::text',
                    '.resumo h2::text'
                ],
                "author":[
                    '[itemprop=author]::text',
                    '.autor-nome::text'
                ],
                "datePublished":[
                    '[itemprop=datePublished]::attr(content)',
                    '.data::text'
                ],
                "dateModified":[
                    '[itemprop=dateModified]::attr(content)'
                ],
                "articleBody":[
                    '[itemprop=articleBody]',
                    '.texto'

                ],
                "keywords":[
                    '[itemprop=keywords] a::text',
                    '[rel=tag]::text',
                    '[onclick*=montaURL]::text'
                ]
            }
        }
    }]

        # l.add_css('name', '[itemprop=headline]::text')
        # l.add_fallback_css('name', '.materia h1::text')
        # l.add_css('authors', '[itemprop=author]::text')
        # l.add_fallback_css('authors', '.autor-nome::text')

        # l.add_css('description', '[itemprop=description]::attr(content)')
        # l.add_css('description', '[itemprop=description]::text')

        # l.add_fallback_css('description', '.resumo h2::text')
        # l.add_css('date_published', '[itemprop=datePublished]::attr(content)')
        # l.add_fallback_css('date_published', '.data::text')
        # l.add_css('date_modified', '[itemprop=dateModified]::attr(content)')
        # # l.add__fallback_css('date_modified', '[itemprop=dateModified]::text')
        # l.add_css('keywords', '[itemprop=keywords] a::text')
        # l.add_fallback_css('keywords', '[rel=tag]::text')
        # l.add_fallback_css('keywords', '[onclick*=montaURL]::text')
        # l.add_css('text', '[itemprop=articleBody]')
        # l.add_fallback_css('text', '.texto')
        # l.add_value('url', response.url)

        # if 'blog' in response.url:
        #     l.add_value('sources_types', ('portal', 'blog'))
        # else:
        #     l.add_value('sources_types', ('portal'))

        # yield l.load_item()

