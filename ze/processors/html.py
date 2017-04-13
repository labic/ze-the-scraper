# -*- coding: utf-8 -*-

import re
import logging
from bs4 import BeautifulSoup, Comment

logger = logging.getLogger(__name__)

class CleanHTML(object):

    def __call__(self, value, context=None):
        soup = BeautifulSoup(value, 'html.parser')
        print(soup.prettify())
        print('##############################################')
        print('##############################################')
        print('##############################################')
        
        # veja
        for e in soup.select('.featured-image'):
            f = soup.new_tag('figure')
            f.append(soup.new_tag('img', src=e.select('img')[0]['data-src']))
            fc = soup.new_tag('figcaption')
            fc.string = string=e.select('p')[0].string
            f.append(fc)
            
            e.replace_with(f)
        
        [e.unwrap() for e in soup.select('section.article-content')]
        
        [e.decompose() for e in soup.select('div.widget-news')]
        
        # g1
        for e in soup.select('[data-block-type="backstage-photo"]'):
            fg = soup.new_tag('figure')
            fg.append(soup.new_tag('img', src=e.select('img.content-media__image')[0]['data-src']))
            fc = soup.new_tag('figcaption')
            fc.string = e.select('img.content-media__image')[0]['alt']
            f.append(fc)
            
            e.replace_with(fg)
        
        for e in soup.select('[data-block-type="backstage-video"]'):
            video_id = e.select('[data-video-id]')[0]['data-video-id']
            fg = soup.new_tag('figure')
            fg.append(soup.new_tag('img', src='https://s02.video.glbimg.com/x720/%s.jpg' % video_id))
            fc = soup.new_tag('figcaption')
            fc.string = e.select('[itemprop="caption"]')[0]['content']
            f.append(fc)
            a = soup.new_tag('a', href='https://globoplay.globo.com/v/%s/' 
                % video_id)
            a.append(fg)
            
            e.replace_with(a)
        
        # cartacapital
        for e in soup.select('p iframe[data-lazy-src*="https://www.youtube.com/embed"]'):
            # TODO: Use Regex?
            video_id = e['data-lazy-src'].split('/')[4]
            fm = soup.new_tag('iframe', src='https://www.youtube.com/embed/%s?rel=0' % video_id,
                width='1280', height='720', frameborder='0', allowfullscreen='true')
            
            e.parent.replace_with(fm)
        
        # All
        [e.unwrap() for e in soup.select("""
            [itemprop="articleBody"], 
            main, 
            .content-text, 
            .content-intertitle, 
            .td-post-content, 
            .td-post-featured-image, 
            #mobile1stparagraph, 
            figure a""")]
        
        [e.decompose() for e in soup.select("""
            .content-head, 
            style, 
            .content-share-bar, 
            .mc-side-item__container, 
            .mc-show-later, 
            .content-share-bar, 
            .content-ads, 
            [id^="ad-"], 
            .comments""")]
        
        [e.decompose() for e in soup.select('p, div') if not e.contents]
        
        # TODO: B4S bug
        [e.previous_element.decompose() for e in soup.select('p + br + p')]
        
        for e in soup.select('*'):
            del e['class']
            del e['data-track-category']
            del e['data-track-links']
            del e['width']
            del e['height']
        
        for e in soup.select('img'):
            if e['alt'].strip(): del e['alt']
            del e['title']
        
        for comments in soup.findAll(text=lambda text:isinstance(text, Comment)):
            comments.extract()
        
        value = soup.prettify()
        print(value)
        return value