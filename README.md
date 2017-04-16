
## Using

### Spider
```shell
scrapy crawl [SPIDER] -a search="-a search='{ \
  "engine": "google", \
  "query": "educação", \
  "last_update": "24H",\
  "results_per_page": 50,\
  "pages": 2 \
}'" 

[SPIDER]
 g1
 ig 
 veja
 g1
```

## References

 - http://xpo6.com/list-of-english-stop-words/
 - [Scrapy - Docs | Jobs: pausing and resuming crawls](https://doc.scrapy.org/en/latest/topics/jobs.html?highlight=scheduler)
 - [scrapy.extensions.memusage][https://github.com/scrapy/scrapy/blob/master/scrapy/extensions/memusage.py]
   It's a good code to extend, overide `_send_report_` function to send to another services than only mail