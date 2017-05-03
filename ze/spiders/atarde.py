from ze.spiders import ZeSpider

class ValorEconomicoSpider(ZeSpider):

    name = 'atarde'
    allowed_domains = ['atarde.uol.com.br']
    parses = [{
        "ze.items.creativework.ArticleItem": {
            "fields": {
                "name": [
                    '[itemprop=headline]::text',
                    '.materia h1::text',
                    'h3.tituloMateria::text'
                ],
                "image": [
                    '[itemprop="image"] img::attr(src)',
                    '.image img::attr(src)'
                ],
                "description": [
                    '[itemprop=description]::attr(content)',
                    '[itemprop=description]::text',
                    '.conteudoMateria figure figcaption::text'
                ],
                "author": [
                    '[itemprop=author]::text',
                    '.autor-nome::text',
                    'span.credito::text'
                ],
                "datePublished": [
                    '[itemprop=datePublished]::attr(content)',
                    '.data::text',
                    'span.date::text',

                ],
                "dateModified": [
                    '[itemprop=dateModified]::attr(content)',
                    '.node-body p em::text'

                ],
                "articleBody": [
                    '[itemprop=articleBody]',
                    '.conteudoMateria'
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

