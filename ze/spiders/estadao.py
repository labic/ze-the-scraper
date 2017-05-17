# -*- coding: utf-8 -*-

from ze.spiders import ZeSpider

class EstadaoSpider(ZeSpider):

    name = 'estadao'
    allowed_domains = ['estadao.com.br']
    parses = [{
        "ze.items.creativework.ArticleItem": {
<<<<<<< 6528394ffb2b78739a5e3621d0a42298e2c4be17
            "fields": { 
                "name": [ 
                    "[itemprop=name]::text", 
                    ".titulo-principal::text", 
                    ".titulo::text", 
                    ".n--noticia__title::text", 
                    "article h1::text", 
                ], 
                "image": [ 
                    "[itemprop=image]::attr(content)", 
                    "[property='og:image']::attr(content)" 
                ], 
                "description": [ 
                    "[itemprop=description]::text", 
                    ".linha-fina::text", 
                    ".n--noticia__subtitle::text", 
                    "article p::text", 
                ], 
||||||| merged common ancestors
            "fields": { 
                "name": [ 
                    "[itemprop=name]::text", 
                    ".titulo-principal::text" 
                ], 
                "image": [ 
                    "[itemprop=image]::attr(content)", 
                    "[property='og:image']::attr(content)" 
                ], 
                "description": [ 
                    "[itemprop=description]::text", 
                    ".linha-fina::text" 
                ], 
=======
            "fields": {
                "name": [
                    "[itemprop=name]::text",
                    ".titulo-principal::text"
                ],
                "image": [
                    "[itemprop=image]::attr(content)",
                    "[property='og:image']::attr(content)"
                ],
                "description": [
                    "[itemprop=description]::text",
                    ".linha-fina::text"
                ],
>>>>>>> revisao de codigos
                "author": [
<<<<<<< 6528394ffb2b78739a5e3621d0a42298e2c4be17
                    "[itemprop=author]::text", 
                    ".autor::text", 
                    ".author::text", 
                ], 
||||||| merged common ancestors
                    "[itemprop=author]::text", 
                    ".autor::text"
                ], 
=======
                    "[itemprop=author]::text",
                    ".autor::text"
                ],
>>>>>>> revisao de codigos
                "datePublished": [
                    "[itemprop=datePublished]::text",
                    ".data::text", 
                ],
                "dateModified": [
                    "[itemprop=dateModified]::text"
                ],
                "articleBody": [
                    "[itemprop=articleBody]",
<<<<<<< 6528394ffb2b78739a5e3621d0a42298e2c4be17
                    ".main-news .content",
                    ".conteudo-materia",
                    ".content", 
                ], 
||||||| merged common ancestors
                    ".main-news .content",
                    ".conteudo-materia",
                ], 
=======
                    ".entry"
                ],
>>>>>>> revisao de codigos
                "keywords": [
<<<<<<< 6528394ffb2b78739a5e3621d0a42298e2c4be17
                    "[itemprop=keywords] a::text", 
                    ".tags a::text", 
                    ".tags a span::text", 
||||||| merged common ancestors
                    "[itemprop=keywords] a::text", 
                    ".tags a::text", 
                    ".tags a span::text" 
=======
                    "[itemprop=keywords] a::text",
                    ".tags a::text",
                    ".tags a span::text"
>>>>>>> revisao de codigos
                ]
            }
        }
    }]
