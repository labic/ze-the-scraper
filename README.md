
## Using

### Estadão Spider

Basic use:
```sh
scrapy crawl estadao -a query=$ESTADAO_QUERY -a topic=$ESTADAO_TOPIC
```

| Argmument | Description |
**query** (opt) | Texto usado para filtrar as publicações diretamente site do Estadão
**topic** (opt) | Coletar publicações em tópico expecifico

- Esportes
- Economia
- Internacional
- Not%C3%ADcias
- Geral
- Cultura
- Pol%C3%ADtica
- Politica
- Opini%C3%A3o
- Brasil
- Eldorado%2FESPN
- S%C3%A3o+Paulo
- Link
- Educa%C3%A7%C3%A3o
- Vida+%26+Estilo
- Sa%C3%BAde
- Paladar
- Ci%C3%AAncia
- Viagem
- M%C3%BAsica

## References

 - http://xpo6.com/list-of-english-stop-words/
 - [Scrapy - Docs | Jobs: pausing and resuming crawls](https://doc.scrapy.org/en/latest/topics/jobs.html?highlight=scheduler)