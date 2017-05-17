from ze.spiders import ZeSpider

class ATarde(ZeSpider):

    name = 'atarde'
    allowed_domains = ['atarde.uol.com.br']
    parses = [{
        "ze.items.creativework.ArticleItem": {
            "fields": {
                "name": [
                    '[itemprop=headline]::text',
                    '.materia h1::text',
                    'h3.tituloMateria::text',
                    '.page-title::text'
                ],
                "image": [
                    '[itemprop="image"] img::attr(src)',
                    '.conteudoMateria figure img::attr(src)',
                ],
                "description": [
                    '[itemprop=description]::attr(content)',
                    '[itemprop=description]::text',
                    '.conteudoMateria figure figcaption::text'
                ],
                "author": [
                    '[itemprop=author]::text',
                    '.autor-nome::text',
                    'p.credito::text'
                ],
                "datePublished": [
                    '[itemprop=datePublished]::attr(content)',
                    '.data::text',
                    'p.data::text',
                    '.post-date::text'

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

