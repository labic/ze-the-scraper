from ze.spiders import ZeSpider

class ATarde(ZeSpider):

    name = 'atarde'
    allowed_domains = ['atarde.uol.com.br']
    parses = [{
        "ze.items.creativework.ArticleItem": {
            "fields": {
                "name": [
                    "meta[property='og:title']::attr(content)",
                    "meta[name=title]::attr(content)",
                    '[itemprop=headline]::text',
                    '.materia h1::text',
                    'h3.tituloMateria::text',
                    '.page-title::text'
                ],
                "image": [
                    'meta[property="og:image"]::attr(content)',
                    '[itemprop="image"] img::attr(src)',
                    '.conteudoMateria figure img::attr(src)',
                ],
                "description": [
                    "meta[property='og:description']::attr(content)",
                    "meta[name=description]::attr(content)",
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
                    '.post-date::text',
                    '.data::text'

                ],
                "dateModified": [
                    '[itemprop=dateModified]::attr(content)',
                    '.node-body p em::text',
                    '.post-date::text',
                    '.data::text'

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

