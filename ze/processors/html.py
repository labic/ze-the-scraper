# -*- coding: utf-8 -*-

import re
import logging
from bs4 import BeautifulSoup, Comment

logger = logging.getLogger(__name__)

class CleanHTML(object):

    def __call__(self, value, context=None):
        soup = BeautifulSoup(value, 'html.parser')
        
        # veja
        for e in soup.select('.featured-image'):
            fg = soup.new_tag('figure')
            fg.append(soup.new_tag('img', src=e.select('img')[0]['data-src']))
            fc = soup.new_tag('figcaption')
            fc.string = e.select('p')[0].string
            fg.append(fc)
            
            e.replace_with(fg)
            
        for e in soup.select('p span iframe[src*="https://www.youtube.com/embed"]'):    
            video_id = e['data-lazy-src'].split('/')[4]
            fm = soup.new_tag('iframe', src='https://www.youtube.com/embed/%s?rel=0' % video_id,
                width='1280', height='720', frameborder='0', allowfullscreen='true')
        
        # g1
        for e in soup.select('[data-block-type="backstage-photo"]'):
            fg = soup.new_tag('figure')
            fg.append(soup.new_tag('img', src=e.select('img.content-media__image')[0]['data-src']))
            fc = soup.new_tag('figcaption')
            fc.string = e.select('img.content-media__image')[0]['alt']
            fg.append(fc)
            
            e.replace_with(fg)
        
        for e in soup.select('[data-block-type="backstage-video"]'):
            video_id = e.select('[data-video-id]')[0]['data-video-id']
            fg = soup.new_tag('figure')
            fg.append(soup.new_tag('img', src='https://s02.video.glbimg.com/x720/%s.jpg' % video_id))
            fc = soup.new_tag('figcaption')
            fc.string = e.select('[itemprop="caption"]')[0]['content']
            fg.append(fc)
            a = soup.new_tag('a', href='https://globoplay.globo.com/v/%s/' % video_id)
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
        el_to_uwrap = [ 
            'main', 
            '#mobile1stparagraph',  
            '.content', 
            '.content-text', 
            '.article-content', 
            '.content-intertitle,', 
            '.td-post-content', 
            '.td-post-featured-image', 
            '[itemprop="articleBody"]', 
        ] if not context.get('el_to_uwrap') else context.get('el_to_uwrap')
        [e.unwrap() for e in soup.select(','.join(el_to_uwrap))]
            
        el_to_decompose = {
            'geral': [
                'style', 
                'script', 
                '#liveblog-container', 
                '.content-head', 
                '.content-share-bar', 
                '.mc-side-item__container', 
                '.mc-show-later', 
                '.content-share-bar', 
                '.content-ads', 
                '.comments', 
                '.tags', 
                '.widget-news', 
            ],
            'empty': ['p', 'div',]
        } if not context.get('el_to_decompose') else context.get('el_to_decompose')
        [e.decompose() for e in soup.select(','.join(el_to_decompose['geral']))]
        [e.decompose() for e in soup.select(','.join(el_to_decompose['empty']))]
        
        # TODO: B4S bug
        [e.previous_element.decompose() for e in soup.select('p + br + p')]
        
        attrs_to_remove = [
            'alt', 
            'title', 
            'class', 
            'data-track-category', 
            'data-track-links',
            'width', 
            'height', 
            'style', 
            'data-sizes', 
            'rel', 
            'data-width', 
            'type',
            'cellpadding', 
            'cellspacing', 
            'valign', 
        ] if not context.get('attrs_to_remove') else context.get('attrs_to_remove')
        for e in soup.select('*'):
            [e.pop(a, None) for a in attrs_to_remove]
        
        for e in soup.select('td p s'):
            e.parent.parent.string = e.string
        
        for comments in soup.findAll(text=lambda text:isinstance(text, Comment)):
            comments.extract()
        
        value = soup.prettify()
        # print(value)
        return value