from ze.spiders import ZeSpider

#TODO: articleBody

class DiariodePernambuco(ZeSpider):

    name = 'diariodepernambuco'
    allowed_domains = ['diariodepernambuco.com.br']
    parses = [{
        "ze.items.creativework.ArticleItem": {
            "fields": {
                "name": [
                    "meta[property='og:title']::attr(content)",
                    "meta[name=title]::attr(content)",
                    '[itemprop=headline]::text',
                    '.h1::text',
                    'div.et_pb_text_align_center::text',
                    #para blog
                    '.entry-title::text',
                    '.entry-heading a::text'
                ],
                "image": [
                    'meta[property="og:image"]::attr(content)',
                    '[itemprop="image"] img::attr(src)',
                    'table.image tbody tr td img::attr(src)',
                    # '.image img::attr(src)'
                    #blog
                    '.entry-content img::attr(src)'
                ],
                "description": [
                    "meta[property='og:description']::attr(content)",
                    "meta[name=description]::attr(content)",
                    '[itemprop=description]::attr(content)',
                    '[itemprop=description]::text'
                ],
                "author": [
                    '[itemprop=author]::text',
                    '.yellowlight::text',
                    #blog
                    '.author a::text',
                    '.post-meta > a::text'
                ],
                "datePublished": [
                    '[itemprop=datePublished]::attr(content)',
                    '.data::text',
                    '[property="article:published_time"]::attr(content)',
                    #para blog
                    '.entry-date::attr(datetime)',
                    '.date::text'
                ],
                "dateModified": [
                    '[itemprop=dateModified]::attr(content)',
                    '[property="article:modified_time"]::attr(content)',
                ],
                "articleBody": [
                    '[itemprop=articleBody]',
                    '[id = abanoticia] ',
                    #blog
                    '.entry-text',
                    '.entry-content'
                ],
                "keywords": [
                    '[itemprop=keywords] a::text',
                    '[rel=tag]::text',
                    '[onclick*=montaURL]::text',
                    '.tags_noticias a::text',
                    #blog
                    '.entry-meta a::text'
                ]
            }
        }
    }]
