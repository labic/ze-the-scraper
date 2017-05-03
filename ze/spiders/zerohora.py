from ze.spiders import ZeSpider

class ValorEconomicoSpider(ZeSpider):

    name = 'zh'
    allowed_domains = ['zh.clicrbs.com.br/']
    parses = [{
        "ze.items.creativework.ArticleItem": {
            "fields": {
                "name": [
                    '[itemprop=headline]::text',
                    '.materia-manchete::text',

                ],
                "image": [
                    '[itemprop="image"] img::attr(src)',
                    '.materia-foto img::attr(src)'
                ],
                "description": [
                    '[itemprop=description]::attr(content)',
                    '.materia-subtitulo::text'
                ],
                "author": [
                    '[itemprop=author]::text',
                    '.meta__tool::text'
                ],
                "datePublished": [
                    '[itemprop=datePublished]::attr(content)',
                    '.meta__date::text',

                ],
                "dateModified": [
                    '[itemprop=dateModified]::attr(content)',
                    '.node-body p em::text'

                ],
                "articleBody": [
                    '[itemprop=articleBody]',
                    '.materia-corpo'
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
