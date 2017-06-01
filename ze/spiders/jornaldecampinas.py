#TODO articleBody limpar, pegar o que está entre <p></p>
from ze.spiders import ZeSpider

class JornaldeCampinasSpider(ZeSpider):


    name = 'jornaldecampinas'
    allowed_domains = ['jornaldecampinas.com.br']
    parses = [{
        "ze.items.creativework.ArticleItem": {
            "fields": {
                "name": [
                    '[itemprop=headline]::text',
                    'h2.post a::text'
                ],
                "image": [
                    '[itemprop="image"] img::attr(src)',
                    # '.wp-image-5984::attr(src)',
                    '[class*= "wp-image"]::attr(src)',
                    '.main-single::attr(src)'
                ],
                "description": [
                    '[itemprop=description]::attr(content)',
                    '.entry p i::text'
                ],
                "author": [
                    '[itemprop=author]::text',
                    '.autor-nome::text',
                    '.node-author-inner strong::text'
                ],
                "datePublished": [
                    '[itemprop=datePublished]::attr(content)',
                    '.data::text',
                    'p.meta::text',

                ],
                "dateModified": [
                    '[itemprop=dateModified]::attr(content)',
                    '.node-body p em::text'

                ],
                "articleBody": [
                    '[itemprop=articleBody]',
                    '.entry'

                ],
                "keywords": [
                    '[itemprop=keywords] a::text',
                    '[rel=tag]::text',
                    '[onclick*=montaURL]::text',
                    '.tags a::text'
                ]
            }
        }
    }]
#.wp-image-5984