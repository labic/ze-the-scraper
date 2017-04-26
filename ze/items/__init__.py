from scrapy import Item, Field
from scrapy.loader import ItemLoader as ScrapyItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose
from ze.processors.article import ArticleProcessor
from ze.processors.common import CommonProcessor
from ze.processors.html import CleanHTML

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


class ThingItem(Item):
    
    additionalType = Field(
        output_processor=TakeFirst(),
    )
    alternateName = Field(
        output_processor=TakeFirst(),
    )
    description = Field(
        output_processor=TakeFirst(),
    )
    disambiguatingDescription = Field(
        output_processor=TakeFirst(),
    )
    identifier = Field()
    image = Field()
    mainEntityOfPage = Field()
    name = Field(
        output_processor=TakeFirst(),
    )
    potentialAction = Field(
        output_processor=TakeFirst(),
    )
    sameAs = Field()
    url = Field(
        output_processor=TakeFirst(),
    )

class CreativeWorkItem(ThingItem):
    about = Field()
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
        input_processor=MapCompose(
            ArticleProcessor.process_authors
        )
    )
    award = Field()
    character = Field()
    citation = Field()
    comment = Field()
    commentCount = Field(
        output_processor=TakeFirst(),
    )
    contentLocation = Field()
    contentRating = Field()
    contributor = Field()
    copyrightHolder = Field()
    copyrightYear = Field()
    creator = Field()
    dateCreated = Field()
    dateModified = Field(
        input_processor=MapCompose(
            CommonProcessor.process_date_time
        ),
        output_processor=TakeFirst(),
    )
    datePublished = Field(
        input_processor=MapCompose(
            CommonProcessor.process_date_time
        ),
        output_processor=TakeFirst(),
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
    interactionStatistic = Field()
    interactivityType = Field()
    isAccessibleForFree = Field()
    isBasedOn = Field()
    isFamilyFriendly = Field()
    isPartOf = Field()
    keywords = Field(
        input_processor=MapCompose(
            ArticleProcessor.process_keywords
        )
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