from .intagible import Intagible

from scrapy import Field
from scrapy.loader.processors import TakeFirst, MapCompose

class ItemList(Intagible):
    
    itemListElement = Field()
    itemListOrder = Field()
    numberOfItems = Field()