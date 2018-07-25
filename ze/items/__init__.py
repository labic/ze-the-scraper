# -*- coding: utf-8 -*-
from datetime import datetime, timezone

from w3lib.html import remove_tags
from scrapy import Item, Field
from scrapy.loader import ItemLoader as ScrapyItemLoader
from scrapy.loader.processors import Join, TakeFirst, MapCompose, Compose

from ..processors.common import *
from ..processors.schema import AuthorParse, KeywordsParse

# from .thing.product import ProductItem


class ItemLoader(ScrapyItemLoader):

    def get_collected_values(self, field_name):
        return (self._values[field_name]
                if field_name in self._values
                else self._values.default_factory())

    def add_fallback_css(self, field_name, css, *processors, **kw):
        if not any(self.get_collected_values(field_name)):
            self.add_css(field_name, css, *processors, **kw)

    def add_fallback_xpath(self, field_name, css, *processors, **kw):
        if not any(self.get_collected_values(field_name)):
            self.add_xpath(field_name, css, *processors, **kw)

    def load_item(self):
        item = self.item
        
        for field_name in tuple(self._values):
            default_value = self.item.fields[field_name].get('default')
            value = self.get_output_value(field_name)
            
            if value is not None:
                item[field_name] = value
            elif not item.get(field_name) and default_value:
                item[field_name] = default_value
        
        # item['dateCreated'] = datetime.now(timezone.utc)
        
        return item


class BaseItem(Item):
    
    meta = Field()


class ThingItem(BaseItem):
    
    additionalType = Field(
        output_processor=TakeFirst(),
    )
    alternateName = Field(
        output_processor=TakeFirst(),
    )
    description = Field(
        input_processor=MapCompose(ScapeString()),
        # output_processor=MapCompose(TakeFirst()),
        # input_processor =MapCompose(TakeFirst()),
        schemas={
            'avro': {
                'name': 'description',
                'type': ('null', 'string'),
            }, 
        }
    )
    disambiguatingDescription = Field(
        output_processor=TakeFirst(),
    )
    identifier = Field(
        output_processor=TakeFirst(),
    )
    image = Field(
        input_processor=MapCompose(ValidURL()),
        schemas={
            'avro': {
                'name': 'image',
                'type': ('null', 'string'), 
            }, 
        }
    )
    mainEntityOfPage = Field(
        output_processor=TakeFirst(),
    )
    name = Field(
        required=True,
        input_processor=MapCompose(CleanString()),
        output_processor=TakeFirst(),
        schemas={
            'avro': {
                'name': 'name',
                'type': ('null', 'string'), 
            }, 
        }
    )
    potentialAction = Field(
        output_processor=TakeFirst(),
    )
    sameAs = Field(
        output_processor=TakeFirst(),
        schemas = {
            'avro': {
                'name': 'sameAs',
                'type': ('null', 'string'),
                'mode': 'repeated',
            }, 
        }
    )
    url = Field(
        output_processor=Compose(FormatString(), TakeFirst()),
        schemas={
            'avro': {
                'name': 'url',
                'type': ('null', 'string'), 
            }, 
        }
    )


class CreativeWorkItem(ThingItem):
    about = Field(
        schemas={
            'avro': {
                'name': 'about',
                'type': ('null', 'string'), 
            }, 
        }
    )
    accessMode = Field()
    accessModeSufficient = Field()
    accessibilityAPI = Field()
    accessibilityControl = Field()
    accessibilityFeature = Field()
    accessibilityHazard = Field()
    accessibilitySummary = Field()
    accountablePerson = Field()
    aggregateRating = Field()
    alternativeHeadline = Field()
    associatedMedia = Field()
    audience = Field()
    audio = Field()
    author = Field(
        default=[{'type': None, 'name': None}], 
        input_processor=MapCompose(remove_tags, AuthorParse()), 
        schemas = {
            'avro': {
                'name': 'author',
                'type': ('null', 'record'), 
                'mode': 'repeated', 
                'fields': ({
                    'name': 'name', 
                    'type': 'string', 
                },{
                    'name': 'type', 
                    'type': 'string', 
                })
            }, 
            'datastore': {
                'type': 'arrayValue', 
                'values': {
                    'type': 'entityValue'
                }
            }
        }
    )
    award = Field()
    character = Field()
    citation = Field()
    comment = Field()
    commentCount = Field(
        output_processor = TakeFirst(),
        schemas={
            'avro': {
                'type': ('null', 'integer'), 
            }, 
        }
    )
    contentLocation = Field()
    contentRating = Field()
    contributor = Field()
    copyrightHolder = Field()
    copyrightYear = Field()
    creator = Field()
    # TODO: User array with multiple dates to chose the best
    dateCreated = Field(
        schemas = {
            'avro': {
                'type': ('null', 'timestamp'), 
            }, 
        }
    )
    # TODO: User array with multiple dates to chose the best
    dateModified = Field(
        input_processor=MapCompose(ParseDate('dateModified')),
        output_processor=TakeFirst(),
        schemas = {
            'avro': {
                'type': ('null', 'timestamp'), 
            }, 
        }
    )
    # TODO: User array with multiple dates to chose the best
    datePublished = Field(
        input_processor=MapCompose(ParseDate('datePublished')),
        output_processor=TakeFirst(),
        schemas={
            'avro': {
                'type': ('null', 'timestamp'),
            }
        }
    )
    discussionUrl = Field()
    editor = Field()
    educationalAlignment = Field()
    educationalUse = Field()
    encoding = Field()
    exampleOfWork = Field()
    fileFormat = Field()
    funder = Field()
    genre = Field()
    hasPart = Field()
    headline = Field()
    inLanguage = Field()
    interactionStatistic = Field(
        schemas={
            'avro': {
                'type': ('null', 'record'),
                'mode': 'repeated',
                'fields': [{ 
                        'name': 'interactionType',
                        'type': 'string',
                    },{
                        'name': 'userInteractionCount',
                        'type': 'integer',
                    },{ 
                        'name': 'type',
                        'type': 'string',
                    },{
                        'name': 'interactionService',
                        'type': ('null', 'record'),
                        'mode': 'repeated',
                        'fields': [{ 
                                'name': 'url',
                                'type': 'string',
                            },{ 
                                'name': 'name',
                                'type': 'string',
                            },{ 
                                'name': 'type',
                                'type': 'string',
                        }]
                }]
            }
        }
    )
    interactivityType = Field()
    isAccessibleForFree = Field()
    isBasedOn = Field()
    isFamilyFriendly = Field()
    isPartOf = Field()
    keywords = Field(
        output_processor=MapCompose(KeywordsParse()),
        schemas={
            'avro': {
                'type': ('null', 'string')
            }
        }
    )
    learningResourceType = Field()
    license = Field()
    locationCreated = Field()
    mainEntity = Field()
    material = Field()
    mentions = Field()
    offer = Field()
    position = Field()
    producer = Field()
    provider = Field()
    publication = Field()
    publisher = Field()
    publishingPrinciples = Field()
    recordedAt = Field()
    releasedEvent = Field()
    review = Field()
    schemaVersion = Field()
    sourceOrganization = Field()
    spatialCoverage = Field()
    sponsor = Field()
    temporalCoverage = Field()
    text = Field()
    thumbnailUrl = Field()
    timeRequired = Field()
    translator = Field()
    typicalAgeRange = Field()
    version = Field()
    video = Field()
    workExample = Field()


class ProductItem(ThingItem):
    
    gtin13 = Field(
        output_processor=TakeFirst(),
    )
    gtin14 = Field(
        output_processor=TakeFirst(),
    )
    brand = Field(
        input_processor=MapCompose(CleanString()),
        output_processor=TakeFirst(),
    )
    price = Field(
        output_processor=TakeFirst(),
    )
    category = Field(
        output_processor=TakeFirst(),
    )
    subcategory = Field(
        output_processor=TakeFirst(),
    )
    sku = Field(
        output_processor=TakeFirst(),
    )
    itemCondition = Field(
        output_processor=TakeFirst(),
    )
    mpn = Field(
        input_processor=MapCompose(CleanString()),
        output_processor=TakeFirst(),
    )
    brand = Field(
        input_processor=MapCompose(CleanString()),
        output_processor=TakeFirst(),
    )
    offers_priceCurrency = Field(
        output_processor=TakeFirst(),
    )
    offers_price = Field(
        output_processor=TakeFirst(),
    )
    offers_eligibleQuantity = Field(
        input_processor=MapCompose(CleanString()),
        output_processor=TakeFirst(),
    )
    offers_availability = Field(
        output_processor=TakeFirst(),
    )
    links = Field(
        output_processor=TakeFirst(),
    )
    composicao_new = Field(
        output_processor=TakeFirst(),
    )
    ingredientes = Field(
        output_processor=TakeFirst(),
    )
    beneficios = Field(
        output_processor=TakeFirst(),
    )
    tx_principal_indicacao = Field(
        output_processor=TakeFirst(),
    )
    tx_contra_indicacao = Field(
        output_processor=TakeFirst(),
    )
    seleciona_cores = Field(
        output_processor=TakeFirst(),
    )
    tipo = Field(
        output_processor=TakeFirst(),
    )
    seleciona_tipo_cabelos = Field(
        output_processor=TakeFirst(),
    )
    especificacoes = Field(
        output_processor=TakeFirst(),
    )
    inmetro = Field(
        output_processor=TakeFirst(),
    )
    selos_do_produto = Field(
        output_processor=TakeFirst(),
    )
    garantia_numero = Field(
        output_processor=TakeFirst(),
    )
    conteudo_embalagem = Field(
        output_processor=TakeFirst(),
    )
    voltagem = Field(
        output_processor=TakeFirst(),
    )
    nr_sac_facricante = Field(
        output_processor=TakeFirst(),
    )
    nr_ministerio_da_saude = Field(
        output_processor=TakeFirst(),
    )
    tx_msg_anvisa = Field(
        output_processor=TakeFirst(),
    )
    