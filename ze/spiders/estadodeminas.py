# -*- coding: utf-8 -*-
from ze.spiders import ZeSpider


class EstadodeMinasSpider(ZeSpider):

    name = 'em'
    allowed_domains = ['em.com.br','uai.com.br']
    parses = [{
        "ze.items.creativework.ArticleItem": {
            "fields": {
                "name":[
                    '[itemprop=headline]::text',
                    '.title-post::text',
                    '.entry-title::text'
                ],
                "image":[
                    '[itemprop="image"]::attr(src)',
                    '.lazy::attr("data-lazy-src")'
                ],
                "description":[
                    '[itemprop=description]::attr(content)',
                    '[itemprop=description]::text',
                    '.entry-content h2::text',
                    '.linha-fina::text',
                    '.entry-content blockquote p::text'
                ],
                "author":[
                    '[itemprop=author]::text',
                    '.author a::text',
                    '[href*="mailto"]::text'
                ],
                "datePublished":[
                    '[itemprop=datePublished]::attr(content)',
                    '.entry-date::text'

                ],
                "dateModified":[
                    '[itemprop=dateModified]::attr(content)'
                ],
                "articleBody":[
                    '[itemprop=articleBody]',
                    '.entry-content'

                ],
                "keywords":[
                    '[itemprop=keywords] a::text',
                    '[rel=tag]::text',
                    '[onclick*=montaURL]::text'
                ]
            }
        }
    }]



