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


scrapy crawl dentalmesul -a category=equipamentos,cirurgia-e-perio,perifericos-e-peca-de-mao,kit-academico,anestesicos,moldagem,instrumentais,protese,radiologia,cimentos,higiene-oral,ortodontia,biosseguranca,implantodontia,endodontia,uso-e-consumo,prevencao-e-profilaxia,brocas,higiene-e-limpeza -o dentalmesul-2018-03-10T15-50.csv


scrapy crawl dentalgutierre -a category=anestesicos,endodontia,odontopediatria,biosseguranca-e-esterilizacao,equipamentos,ortodontia,brocas,estetica-e-dentistica,papelaria,cimentos,harmonizacao-orofacial,protese,cirurgia-e-implante,instrumentais,radiologia,consultorio,livros,saude-bucal,cursos-e-palestras,materiais-de-consumo,vestuario,decoracao,medicamentos,descartaveis,moldagem,vencimento-proximo -o dentalgutierre-2018-03-10T14H11.csv


scrapy crawl neodente -a brand=B%3a2000000,B%3a2000001 -o neodente-2017-03-13-16T26.csv

scrapy crawl suryadental -a category=equipamentos-perifericos-e-pe/acessorios,equipamentos-perifericos-e-pe/equipamentos,equipamentos-perifericos-e-pe/pecas-de-mao,equipamentos-perifericos-e-pe/perifericos,protese-clinica-e-implantodont/b-34-acabamento-e-polimento,protese-clinica-e-implantodont/acessorios,protese-clinica-e-implantodont/acidos,protese-clinica-e-implantodont/afastamento-gengival,protese-clinica-e-implantodont/articulacao,protese-clinica-e-implantodont/articuladores-e-acessorios,protese-clinica-e-implantodont/attachment,protese-clinica-e-implantodont/cimentos-resinosos,protese-clinica-e-implantodont/cimentos-temporarios,protese-clinica-e-implantodont/cimentos-zinco,protese-clinica-e-implantodont/facetas-de-resina,protese-clinica-e-implantodont/fibra-de-vidro-reforco,protese-clinica-e-implantodont/hemostaticos,protese-clinica-e-implantodont/implantodontia,protese-clinica-e-implantodont/instrumentais,protese-clinica-e-implantodont/ionomeros-de-cimentacao,protese-clinica-e-implantodont/lamparinas,protese-clinica-e-implantodont/lupas,protese-clinica-e-implantodont/b-33-modelos,protese-clinica-e-implantodont/moldagem,protese-clinica-e-implantodont/b-35-moldeiras,protese-clinica-e-implantodont/obturadores-provisorios,protese-clinica-e-implantodont/perifericos,protese-clinica-e-implantodont/pinos,protese-clinica-e-implantodont/reembasadores,protese-clinica-e-implantodont/registros-de-mordida,protese-clinica-e-implantodont/b-32-resina-acrilica-para-moldeiras,protese-clinica-e-implantodont/resinas-acrilicas-auto,protese-clinica-e-implantodont/resinas-acrilicas-provisorias,protese-clinica-e-implantodont/resinas-acrilicas-vermelhas,protese-clinica-e-implantodont/resinas-bisacrilicas,protese-clinica-e-implantodont/silano,protese-clinica-e-implantodont/vaselinas-solidas,protese-laboratorial/acabamento-e-polimento,protese-laboratorial/acessorios,protese-laboratorial/antibolhas,protese-laboratorial/articuladores,protese-laboratorial/attachment,protese-laboratorial/binders,protese-laboratorial/bloco-cad-cam-fgm,protese-laboratorial/brocas,protese-laboratorial/ceras,protese-laboratorial/dentes,protese-laboratorial/discos-diamantados,protese-laboratorial/duplicadores,protese-laboratorial/e-max,protese-laboratorial/gengivas-artificiais,protese-laboratorial/gessos,protese-laboratorial/instrumentais,protese-laboratorial/isolantes,protese-laboratorial/metais,protese-laboratorial/muflas,protese-laboratorial/muralhas,protese-laboratorial/perifericos,protese-laboratorial/pinceis,protese-laboratorial/c-42-pincel,protese-laboratorial/placas-soft-e-placas-rigidas,protese-laboratorial/poliquim,protese-laboratorial/porcelanas,protese-laboratorial/porcelanas-pastilha-injecao,protese-laboratorial/prensas,protese-laboratorial/c-41-resina-acrilica-para-moldeiras,protese-laboratorial/resinas-acrilicas-auto,protese-laboratorial/resinas-acrilicas-caracterizacao,protese-laboratorial/resinas-acrilicas-microondas,protese-laboratorial/resinas-acrilicas-orto,protese-laboratorial/resinas-acrilicas-provisorio,protese-laboratorial/resinas-acrilicas-termo,protese-laboratorial/resinas-acrilicas-vermelho,protese-laboratorial/resinas-foto,protese-laboratorial/revestimentos,protese-laboratorial/soldas,protese-laboratorial/solucoes-eletroliticas,protese-laboratorial/sr-chromasit,protese-laboratorial/sr-ivocron,protese-laboratorial/telas-para-protese-total,endodontia-novo/acessorios,endodontia-novo/arcos-para-isolamento,endodontia-novo/brocas,endodontia-novo/cimentos,endodontia-novo/clareadores-intra-canais,endodontia-novo/d-34-clorhexidina,endodontia-novo/condensadores-de-guta-mcspad,endodontia-novo/cones-de-guta,endodontia-novo/cones-de-papel,endodontia-novo/diques-de-borracha,endodontia-novo/edta,endodontia-novo/espacadores-digitais,endodontia-novo/eugenol,endodontia-novo/extirpa-nervo,endodontia-novo/filmes,endodontia-novo/formocresol,endodontia-novo/grampos,endodontia-novo/hidroxido-de-calcio,endodontia-novo/irrigacao,endodontia-novo/lentulos,endodontia-novo/limas,endodontia-novo/lubrificantes-para-lima-endo-ptc,endodontia-novo/obturadores-restauradores-pr,endodontia-novo/paramonoclorofenol,endodontia-novo/pastas-de-hodroxido-de-calcio,endodontia-novo/perifericos-e-pecas-de-mao,endodontia-novo/posicionadores-de-filme,endodontia-novo/reguas-milimetradas,endodontia-novo/solventes-de-guta-percha,endodontia-novo/sonda-exploradora-dupla-reta-4,endodontia-novo/stop-para-lima,endodontia-novo/teste-de-vitalidade,endodontia-novo/tricresol-formalina,ortodontia-180/abzil,ortodontia-180/acabamento-e-polimento,ortodontia-180/acessorios-e-compartimentos,ortodontia-180/acidos,ortodontia-180/resinas-colagem,ortodontia-180/alicates,ortodontia-180/brocas-multilaminadas,ortodontia-180/eurodonto,ortodontia-180/instrumentais,ortodontia-180/ionomeros-para-banda,ortodontia-180/macaricos,ortodontia-180/morelli,ortodontia-180/orthometric,ortodontia-180/oxidos-de-aluminio,ortodontia-180/perifericos,ortodontia-180/resinas-acrilicas-orto,ortodontia-180/tecnident,dentistica-e-estetica-180/acabamento-e-polimento,dentistica-e-estetica-180/acessorios,dentistica-e-estetica-180/acidos,dentistica-e-estetica-180/adesivos,dentistica-e-estetica-180/afastadores-e-abridores,dentistica-e-estetica-180/amalgama,dentistica-e-estetica-180/articulacoes,dentistica-e-estetica-180/clareadores,dentistica-e-estetica-180/clorhexidina,dentistica-e-estetica-180/coroas-poliester,dentistica-e-estetica-180/cunhas,dentistica-e-estetica-180/dessensibilizantes,dentistica-e-estetica-180/diques-de-borracha,dentistica-e-estetica-180/espatulas,dentistica-e-estetica-180/facetas-de-resina,dentistica-e-estetica-180/fita-para-isolamento-isotape,dentistica-e-estetica-180/f-42-gel-bloqueador-de-oxigenio,dentistica-e-estetica-180/grampos,dentistica-e-estetica-180/hemostaticos,dentistica-e-estetica-180/hidroxido-de-calcio,dentistica-e-estetica-180/ionomeros,dentistica-e-estetica-180/kit-dentistica,dentistica-e-estetica-180/laminas-de-bisturi,dentistica-e-estetica-180/f-43-manequim,dentistica-e-estetica-180/matrizes-aco,dentistica-e-estetica-180/obturadores-e-restauradores-pr,dentistica-e-estetica-180/opacificadores,dentistica-e-estetica-180/fotopolimerizadores,dentistica-e-estetica-180/piercings,dentistica-e-estetica-180/pinceis,dentistica-e-estetica-180/pinceis-microaplicadores,dentistica-e-estetica-180/pinos,dentistica-e-estetica-180/profilaxia,dentistica-e-estetica-180/protetores-gengivais,dentistica-e-estetica-180/removedores-de-mancha,dentistica-e-estetica-180/resinas,dentistica-e-estetica-180/resinas-flow,dentistica-e-estetica-180/resinas-pinturas,dentistica-e-estetica-180/selantes,dentistica-e-estetica-180/tiras-de-poliester,dentistica-e-estetica-180/verniz,brocas-e-broqueiros/acessorios,brocas-e-broqueiros/aco-ca,brocas-e-broqueiros/aco-pm,brocas-e-broqueiros/batt,brocas-e-broqueiros/broqueiros,brocas-e-broqueiros/carbide-ca,brocas-e-broqueiros/carbide-fg,brocas-e-broqueiros/carbide-pm,brocas-e-broqueiros/cirurgica-fg-25mm-haste-longa,brocas-e-broqueiros/cp-drill-endo,brocas-e-broqueiros/diamantada-ca,brocas-e-broqueiros/diamantada-fg,brocas-e-broqueiros/diamantada-pm,brocas-e-broqueiros/endo-z,brocas-e-broqueiros/gates,brocas-e-broqueiros/kits,brocas-e-broqueiros/la-axxess,brocas-e-broqueiros/largo-ponta-inativa,brocas-e-broqueiros/ln-remocao-de-pino,brocas-e-broqueiros/multilaminada-12-laminas-fg,brocas-e-broqueiros/multilaminadas-24-laminas-fg,brocas-e-broqueiros/multilaminada-30-laminas-fg,brocas-e-broqueiros/multilaminadas-para-amalgama,brocas-e-broqueiros/brocas-para-recortador-palato,brocas-e-broqueiros/peeso-ponta-ativa,brocas-e-broqueiros/perfurar-troquel-1-85mm-pin-pl,brocas-e-broqueiros/perfurar-troquel-1-95mm-pin-pl,brocas-e-broqueiros/pino-macro-lock-n-2-vermelho,brocas-e-broqueiros/transmetais,brocas-e-broqueiros/tungstenio-maxicut-minicut,brocas-e-broqueiros/vulcanite-de-aco-para-resina-a,brocas-e-broqueiros/zekrya,descartaveis-novo/abaixa-lingua-de-madeira,descartaveis-novo/afastador-de-labios-optragate,descartaveis-novo/agulhas-gengivais,descartaveis-novo/algodoes,descartaveis-novo/babadores,descartaveis-novo/bolsas-envelopes-para-esteri,descartaveis-novo/capa-para-seringa-triplice,descartaveis-novo/coletores-perfurocortantes,descartaveis-novo/h-45-contra-angulo-descartavel,descartaveis-novo/diques-de-borracha,descartaveis-novo/h-44-escova-para-antissepsia,descartaveis-novo/espelhos-com-cabo-descartavel,descartaveis-novo/fios-sutura,descartaveis-novo/fitas-para-autoclave,descartaveis-novo/gazes,descartaveis-novo/gorros-e-toucas,descartaveis-novo/guardanapos,descartaveis-novo/jalecos,descartaveis-novo/kit-cirurgico-pp30,descartaveis-novo/laminas-de-bisturi,descartaveis-novo/h-43-lenco-umidecido,descartaveis-novo/luvas-cirurgicas-estereis,descartaveis-novo/luvas-procedimento-latex,descartaveis-novo/luvas-procedimento-nitrilo,descartaveis-novo/luvas-procedimento-powder-free,descartaveis-novo/luvas-procedimento-vinil,descartaveis-novo/mascaras,descartaveis-novo/moldeiras-para-fluor,descartaveis-novo/papeis-toalha,descartaveis-novo/pinceis-microaplicadores,descartaveis-novo/pontas-para-aplicacao-de-silicone-de-adicao,descartaveis-novo/pontas-misturadoras-de-silicone-de-adicao,descartaveis-novo/pontas-para-aplicacao-de-ionom,descartaveis-novo/ponta-para-aplicacao-de-resina-bisacrilica,descartaveis-novo/prope,descartaveis-novo/rolos-para-esterilizacao,descartaveis-novo/sacos-para-lixo,descartaveis-novo/seringas-com-agulha,descartaveis-novo/sobre-luva,descartaveis-novo/stop-para-lima,descartaveis-novo/sugadores-cirurgicos-plasticos,descartaveis-novo/sugadores-endo-plasticos,descartaveis-novo/sugadores-plasticos,instrumentais/abaixa-lingua,instrumentais/abridores-de-boca,instrumentais/acessorios,instrumentais/afastadores,instrumentais/alavancas,instrumentais/alicates,instrumentais/alveolotomos,instrumentais/aplicadores-de-hidroxido-de-ca,instrumentais/arcos,instrumentais/brunidores,instrumentais/cabos-de-bisturi,instrumentais/cabos-de-espelho,instrumentais/calcadores,instrumentais/cinzeis,instrumentais/condensadores,instrumentais/cortantes,instrumentais/curetas,instrumentais/descoladores,instrumentais/destaca-periosteo,instrumentais/escavadores,instrumentais/esculpidores,instrumentais/espatula-gesso-alginato,instrumentais/espatula-ceramica,instrumentais/espatula-resina,instrumentais/especimetros,instrumentais/espelhos,instrumentais/extratores-tartaro,instrumentais/forceps,instrumentais/ganchos-barros,instrumentais/grampos,instrumentais/kits-clinicos,instrumentais/kit-irrigacao-endo,instrumentais/limas,instrumentais/localizadores-de-nervo,instrumentais/martelos,instrumentais/medidores-de-coroa-chu,instrumentais/medidores-de-proporcionalidade,instrumentais/paquimetros,instrumentais/pedras-de-afiar,instrumentais/perfuradores-dique,instrumentais/pincas,instrumentais/pontas-morse,instrumentais/ponteira-cavitron,instrumentais/porta-agulha,instrumentais/ver-mais,anestesicos-e-medicamentos-180/acessorios,anestesicos-e-medicamentos-180/anestesicos,anestesicos-e-medicamentos-180/medicamentos,compartimentos-e-suportes/almotolias,compartimentos-e-suportes/k-32-anel-dappen,compartimentos-e-suportes/bandejas,compartimentos-e-suportes/k-30-bolsa-para-aeb,compartimentos-e-suportes/k-33-bolsas-mochilas-sacolas,compartimentos-e-suportes/broqueiros,compartimentos-e-suportes/caixa-organizadora-para-trabalho-de-protese,compartimentos-e-suportes/caixas-orto,compartimentos-e-suportes/capsulas-petry,compartimentos-e-suportes/cartoes-rx,compartimentos-e-suportes/coletores-de-lixo,compartimentos-e-suportes/cubas,compartimentos-e-suportes/estojos,compartimentos-e-suportes/gaveteiro-para-dentes,compartimentos-e-suportes/maletas,compartimentos-e-suportes/porta-algodao,compartimentos-e-suportes/porta-alicate,compartimentos-e-suportes/k-31-porta-dentes-deciduos,compartimentos-e-suportes/porta-elastico,compartimentos-e-suportes/porta-fio,compartimentos-e-suportes/porta-lima-endo,compartimentos-e-suportes/porta-luva,compartimentos-e-suportes/porta-resina,compartimentos-e-suportes/potes-dappen,compartimentos-e-suportes/potes-paladon,compartimentos-e-suportes/k-29-prendedor-de-guardanapos,compartimentos-e-suportes/protetor-de-escova-sanifill-com-3-unidades,compartimentos-e-suportes/refil-com-2-divisoes-para-bandeja-ad1-a,compartimentos-e-suportes/saboneteiras,compartimentos-e-suportes/sacos-para-lixo,compartimentos-e-suportes/suportes,compartimentos-e-suportes/tambores-de-gaze,compartimentos-e-suportes/toalheiros,diversos-novo/agulhas-de-sutura,diversos-novo/aparelhos-de-pressao-e-estetoscopios,diversos-novo/barra-de-erich,diversos-novo/l-29-bolsas-mochilas-sacolas,diversos-novo/bolsas-termicas,diversos-novo/protecao,diversos-novo/l-26-copos-e-gaarrafas,diversos-novo/cremes-para-fixar-protese-total,diversos-novo/l-23-curva-de-spee,diversos-novo/l-24-esponja-hemostatica,diversos-novo/esterilizacao,diversos-novo/fotografia,diversos-novo/gaveteiros-para-dentes,diversos-novo/higiene,diversos-novo/lapis-dermatografico,diversos-novo/limpeza,diversos-novo/lubrificantes-de-pecas-de-mao,diversos-novo/l-25-luva-para-seringa-carpule,diversos-novo/l-27-marcadores-de-pagina,diversos-novo/l-28-mini-marmita,diversos-novo/papelaria,diversos-novo/paquimetros,diversos-novo/piercings,diversos-novo/placas-de-vidro,diversos-novo/produtos-venda-troca,diversos-novo/profilaxia,diversos-novo/protecao-180,diversos-novo/radiografia,diversos-novo/vestuario -o suryadental-2017-03-13-17H34.csv





scrapy crawl farmadelivery -a category=medicamentos/genericos,medicamentos/refrigerados,medicamentos/tarjados/oncologia,medicamentos/tarjados/vida-sexual,medicamentos/venda-livre/alergia,medicamentos/venda-livre/alergia,medicamentos/venda-livre/azia-e-ma-digestao,medicamentos/venda-livre/colirios-e-lubrificantes-oftalmicos,medicamentos/venda-livre/dor,medicamentos/venda-livre/estresse,medicamentos/venda-livre/febre,medicamentos/venda-livre/genericos-otc,medicamentos/venda-livre/gripe,medicamentos/venda-livre/insonia,medicamentos/venda-livre/laxantes-e-reguladores,medicamentos/venda-livre/micoses,medicamentos/venda-livre/pastilhas,saude-e-bem-estar/vitaminas-e-minerais/antiidade-e-antioxidantes,saude-e-bem-estar/vitaminas-e-minerais/ferro,saude-e-bem-estar/vitaminas-e-minerais/ginseng,saude-e-bem-estar/vitaminas-e-minerais/omega-age,saude-e-bem-estar/vitaminas-e-minerais/polivitaminicos,saude-e-bem-estar/vitaminas-e-minerais/vitamina-a,saude-e-bem-estar/vitaminas-e-minerais/vitamina-b,saude-e-bem-estar/vitaminas-e-minerais/vitamina-c,saude-e-bem-estar/vitaminas-e-minerais/calcio,saude-e-bem-estar/vitaminas-e-minerais/vitamina-d,saude-e-bem-estar/vitaminas-e-minerais/vitamina-e,saude-e-bem-estar/vitaminas-e-minerais/vitaminak,saude-e-bem-estar/vitaminas-e-minerais/zinco,saude-e-bem-estar/alimentos-e-bebidas/adocantes,saude-e-bem-estar/alimentos-e-bebidas/balas,saude-e-bem-estar/alimentos-e-bebidas/chas-e-ervas,saude-e-bem-estar/alimentos-e-bebidas/cranberry,saude-e-bem-estar/alimentos-e-bebidas/gelatinas-e-pudins,saude-e-bem-estar/alimentos-e-bebidas/goji-berry,saude-e-bem-estar/dietas-alimentares/colageno-e-gelatina,saude-e-bem-estar/dietas-alimentares/diet,saude-e-bem-estar/dietas-alimentares/shakes-e-substitutos-de-refeicoes,saude-e-bem-estar/flora-intestinal/fibras,saude-e-bem-estar/flora-intestinal/prebioticos,saude-e-bem-estar/flora-intestinal/probioticos,saude-e-bem-estar/flora-intestinal/simbioticos,saude-e-bem-estar/nutricaoesportiva/bcaa,saude-e-bem-estar/nutricaoesportiva/creatina,saude-e-bem-estar/nutricaoesportiva/energeticos,saude-e-bem-estar/nutricaoesportiva/glutamina,saude-e-bem-estar/nutricaoesportiva/lcarnitina,saude-e-bem-estar/nutricaoesportiva/termogenicos,saude-e-bem-estar/nutricaoesportiva/wheyprotein,saude-e-bem-estar/nutricosmeticos/cabelos,saude-e-bem-estar/nutricosmeticos/celulite,saude-e-bem-estar/nutricosmeticos/emagrecedor,saude-e-bem-estar/nutricosmeticos/imedeenn,saude-e-bem-estar/nutricosmeticos/antioxidante,saude-e-bem-estar/nutricosmeticos/ativador-de-bronzeado,saude-e-bem-estar/beltnutrition,mamaes-e-bebes/mustela/kits-cha-de-bebe,mamaes-e-bebes/alimentacao-infantil/alimentos-e-suplementos,mamaes-e-bebes/alimentacao-infantil/leites-e-formulas-infantis,mamaes-e-bebes/alimentacao-infantil/acessorios-infantis,mamaes-e-bebes/baba-eletronica-e-cameras,mamaes-e-bebes/cadeiras-para-automovel,mamaes-e-bebes/carrinhos-de-passeio,mamaes-e-bebes/higiene-infantil-e-cuidados/cuidados-infantil-corpo,mamaes-e-bebes/higiene-infantil-e-cuidados/higiene-bucal,mamaes-e-bebes/higiene-infantil-e-cuidados/hora-do-banho,mamaes-e-bebes/chupetas-e-mamadeiras,mamaes-e-bebes/gestantes-e-mamaes/amamentacao,mamaes-e-bebes/gestantes-e-mamaes/hidratantes,mamaes-e-bebes/gestantes-e-mamaes/vitaminas-para-gestantes,mamaes-e-bebes/gestantes-e-mamaes/tratamento-antiestrias,mamaes-e-bebes/gestantes-e-mamaes/protetor-de-seios,mamaes-e-bebes/protecao-solar,mamaes-e-bebes/troca-de-fralda/fraldas,mamaes-e-bebes/troca-de-fralda/lencos-umedecidos,aparelhos-e-testes/pressao-arterial,aparelhos-e-testes/beleza-cuidados/chapinhas-pranchas,aparelhos-e-testes/beleza-cuidados/secadores-de-cabelo,aparelhos-e-testes/inaladores,aparelhos-e-testes/purificador-de-ar,aparelhos-e-testes/saude-e-bem-estar,aparelhos-e-testes/testes,aparelhos-e-testes/umidificadores,diabetes/accu-chek/accu-chek-active,diabetes/accu-chek/accu-chek-advantage,diabetes/accu-chek/accu-chek-fastclix,diabetes/accu-chek/accu-chek-go,diabetes/accu-chek/accu-chek-performa,diabetes/accu-chek/accu-chek-performa,diabetes/accu-chek/accu-chek-softclix,diabetes/accu-chek/accu-chek-saf-t-pro,diabetes/accu-chek/accutrend,diabetes/accu-chek/coaguchek-xs,diabetes/accu-chek/gerenciamento-de-dados,diabetes/accu-chek/results-lancetas-accuchek,diabetes/accu-chek/accu-chek-monitores,diabetes/aparelhos-para-glicemia,diabetes/agulhas,diabetes/canetas-aplicadoras,diabetes/lancetas-e-lancetadores,diabetes/nutricao,diabetes/tiras-para-teste,perfumaria/repelentes,perfumaria/protetores-solares/base-corretiva,perfumaria/protetores-solares/fps-15-ate-fps-30,perfumaria/protetores-solares/fps-35-ate-fps-60,perfumaria/protetores-solares/fps-65-ate-fps-100,perfumaria/dermocosmeticos/cuidados-para-o-rosto,perfumaria/dermocosmeticos/pes,perfumaria/dermocosmeticos/cuidados-para-o-corpo,perfumaria/dermocosmeticos/cuidados-para-os-cabelos,perfumaria/dermocosmeticos/labios,perfumaria/higiene-bucal/fio-fita-dental,perfumaria/higiene-bucal/creme-gel-dental,perfumaria/higiene-bucal/antiseptico,perfumaria/higiene-bucal/escova-dental,perfumaria/higiene-bucal/fio-fita-dental,perfumaria/higiene-bucal/proteses-dentarias,perfumaria/cuidados-pessoais/creme-e-espuma-de-barbear,perfumaria/cuidados-pessoais/colonias-e-perfumes,perfumaria/cuidados-pessoais/cuidados-com-os-cabelos,perfumaria/cuidados-pessoais/cuidados-para-as-maos-e-unhas,perfumaria/cuidados-pessoais/cremes-para-os-pes,perfumaria/cuidados-pessoais/depilatorios,perfumaria/cuidados-pessoais/desodorantes,perfumaria/cuidados-pessoais/gestantes,perfumaria/cuidados-pessoais/hastes-flexiveis,perfumaria/cuidados-pessoais/hidratantes,perfumaria/cuidados-pessoais/lencos-de-papel,perfumaria/cuidados-pessoais/oleo-corporal,perfumaria/cuidados-pessoais/redutores-de-celulite,perfumaria/maquiagem-e-beleza/tinturas-e-coloracao,perfumaria/produtos-intimos/absorventes-e-protetores-diarios,perfumaria/produtos-intimos/gel-lubrificante-intimo,perfumaria/produtos-intimos/hidratantes-intimos,perfumaria/produtos-intimos/higiene-intima,perfumaria/produtos-intimos/massageador-intimo,perfumaria/produtos-intimos/preservativos-e-lubrificantes-intimos,perfumaria/algodao,perfumaria/curativos/luvas-e-mascaras,perfumaria/curativos/primeiros-socorros-e-curativos,outlet/medicamentos-outlet,outlet/suplementos-outlet,outlet/perfumaria-outlet -o farmadelivery-2018-03-14T16H33.csv

Notas:

Produto existe em mais de uma categoria, porem o sistema filtra URLs já scrapeadas
Então o que será feito? Repitir o produto para manter as multiplas categorias em quele pertence?

O banco de dados tabular não é mais indicado para catalogo de produtos já que 