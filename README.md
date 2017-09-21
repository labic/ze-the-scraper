# Zé The Scraper
[![Build Status](https://travis-ci.org/labic/ze-the-scraper.svg?branch=develop)](https://travis-ci.org/labic/ze-the-scraper)

## Install

- [Install Berkeley DB](http://www.linuxfromscratch.org/blfs/view/7.9/server/db.html)



## Limitações

 - Os artigos `article` são listados por ordem da data de coleta `dateCreated` porem os artigos podem ser considerados com atualizados e serem coletados novamente causado que a data de coleta e data de publicação `datePublished` divirjam 
 

## Usage

### Crawlling using a single spider an single url
```shell
scrapy crawl <spider_name> -a url=http(s):someurl.com?query1=a&query2=b
```

### Crawlling using a single spider with urls extrected from Google
```shell
scrapy crawl <spider_name> -a search='{ \
  "query": "Enem OR \"Exame Nacional * Ensino Médio\"", \
  "regex": "(?i)Enem|Exame.{0,}Nacional.{0,}Ensino.{0,}Mé?e?dio" \
  "engine": "google", \
  "dateRestrict": "d1",\
  "results_per_page": 50,\
  "pages": 2 \
}' 
```

### Crawlling using all spiders with urls extrected from Google
```shell
scrapy crawl all -a search='{ \
  "query": "Enem OR \"Exame Nacional * Ensino Médio\"", \
  "regex": "(?i)Enem|Exame.{0,}Nacional.{0,}Ensino.{0,}Mé?e?dio"
  "engine": "google", \
  "dateRestrict": "d1", \
  "results_per_page": 50, \
  "pages": 2 \
}'

scrapy crawl all \
-a search=google \
-a query="Enem OR \"Exame Nacional * Ensino Médio\"" \
-a regex="(?i)Enem|Exame.{0,}Nacional.{0,}Ensino.{0,}Mé?e?dio" \
-a dateRestrict=d1

```

## References

 - http://xpo6.com/list-of-english-stop-words/
 - [Scrapy - Docs | Jobs: pausing and resuming crawls](https://doc.scrapy.org/en/latest/topics/jobs.html?highlight=scheduler)
 - [scrapy.extensions.memusage][https://github.com/scrapy/scrapy/blob/master/scrapy/extensions/memusage.py]
   It's a good code to extend, overide `_send_report_` function to send to another services than only mail


## TODO:

- [ ] Implement DeltaFetch midleware
- [ ] decompose class `.n--noticia__newsletter` to spider estadao
- [ ] Use https://github.com/codelucas/newspaper

## Ideas

### Relation DB Schema

https://cloud.google.com/bigtable/docs/schema-design

| Row key | Column data |
| INEP | NEWS:EDUCACAO (V1 03/01/15):558.40 | 

Use this:
- TinyDB CodernityDB
- https://blog.scrapinghub.com/2016/04/20/scrapy-tips-from-the-pros-april-2016-edition/
- https://helpdesk.scrapinghub.com/support/solutions/articles/22000200401-dotscrapy-persistence-addon
- https://helpdesk.scrapinghub.com/support/solutions/articles/22000200418-magic-fields-addon
- https://helpdesk.scrapinghub.com/support/solutions/articles/22000200411-delta-fetch-addon
- 
### lambda

```python

class AVRO_FIELD_TYPE(Enum):
    str = 'STRING'
    list = 'RECORD'
    int = 'INTERGE'
    bool = 'BOOLEAN'

f_avro = lambda ft, md='NULLABLE', fd=[]: { 'avro': { 
    # 'field_type': ft.uppe() if ft else AVRO_FIELD_TYPE[type(ft)], 
    'field_type': ft.uppe(), 
    'mode': md, 
    'fields': fd } }

@property
def identifier(self):
    self['output_processor'] = self.get('output_processor') if self.get('output_processor') \
                                else TakeFirst()
    if not hasattr(self, 'schemas'):
        self['schemas'] = self.f_avro('STRING', 'NULLABLE', [])
    
    return self 

@identifier.setter
def identifier(self, value):
    self['output_processor'] if self.get('output_processor') else TakeFirst()
    return self 
```