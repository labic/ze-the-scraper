# -*- coding: utf-8 -*-

#TODO articleBody

from ze.spiders import ZeSpider

class JCOnlineSpider(ZeSpider):

    name = "jconline"
    allowed_domains = ["jconline.ne10.uol.com.br"]
    parses = [{
        "ze.items.creativework.ArticleItem": {
            "fields": {
                "name": [
                    "meta[property='og:title']::attr(content)",
                    "meta[name=title]::attr(content)",
                    ".titulo-materia::text",
                    ".titulo-noticia a::attr(title)",
                    "[itemprop=headline]::text",
                    "title::text",
                ],
                "image": [
                    'meta[property="og:image"]::attr(content)',
                    "[itemprop=image]::attr(src)",
                    "#noticia img.bordaimg::attr(src)",
                    "[class*='wp-image]::attr(src)"
                ],
                "description": [
                    "meta[property='og:description']::attr(content)",
                    "meta[name=description]::attr(content)",
                    "[itemprop=description]::attr(content)",
                    "[itemprop=description]::text",
                    "meta[name=description]::attr(content)",
                    "p.mg_sutia::text"
                ],
                "author": [
                    "[itemprop=author]::text",
                    ".author a::text",#não tem autor da matéria no site
                    "[id*=post] header strong::text",#"pra blog"

                ],
                "datePublished": [
                    "[itemprop=datePublished]::attr(content)",
                    ".data-materia::text",
                    ".data-post div::text"
                ],
                "dateModified": [
                    "[itemprop=dateModified]::attr(content)"
                ],
                "articleBody": [
                    "[itemprop=articleBody]",
                    "#noticia_corpodanoticia"#pegar o que ta entre <p></p>,
                    "#texto-noticia"#fazer negocio de pegar xhr
                ],
                "keywords": [
                    "[itemprop=keywords] a::text",
                    "meta[name=keymwords]::attr(content)",
                    "li.keywords a::text",
                ]
            }
        }
    }]
