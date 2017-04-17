# -*- coding: utf-8 -*-

import re
import logging
from bs4 import BeautifulSoup, Comment

logger = logging.getLogger(__name__)

class CleanHTML(object):

    def __call__(self, value, context={}):
        html = BeautifulSoup(value, 'html.parser')
        
        # veja
        for e in html.select('.featured-image'):
            fg = html.new_tag('figure')
            fg.append(html.new_tag('img', src=e.select('img')[0]['data-src']))
            fc = html.new_tag('figcaption')
            fc.string = e.select('p')[0].string
            fg.append(fc)
            
            e.replace_with(fg)
            
        for e in html.select('p span iframe[src*="https://www.youtube.com/embed"]'):    
            video_id = e['data-lazy-src'].split('/')[4]
            fm = html.new_tag('iframe', src='https://www.youtube.com/embed/%s?rel=0' % video_id,
                width='1280', height='720', frameborder='0', allowfullscreen='true')
        
        # g1
        for e in html.select('[data-block-type="backstage-photo"]'):
            fg = html.new_tag('figure')
            fg.append(html.new_tag('img', src=e.select('img.content-media__image')[0]['data-src']))
            fc = html.new_tag('figcaption')
            fc.string = e.select('img.content-media__image')[0]['alt']
            fg.append(fc)
            
            e.replace_with(fg)
        
        for e in html.select('[data-block-type="backstage-video"]'):
            video_id = e.select('[data-video-id]')[0]['data-video-id']
            fg = html.new_tag('figure')
            fg.append(html.new_tag('img', src='https://s02.video.glbimg.com/x720/%s.jpg' % video_id))
            fc = html.new_tag('figcaption')
            fc.string = e.select('[itemprop="caption"]')[0]['content']
            fg.append(fc)
            a = html.new_tag('a', href='https://globoplay.globo.com/v/%s/' % video_id)
            a.append(fg)
            
            e.replace_with(a)
        
        # cartacapital
        for e in html.select('p iframe[data-lazy-src*="https://www.youtube.com/embed"]'):
            # TODO: Use Regex?
            video_id = e['data-lazy-src'].split('/')[4]
            fm = html.new_tag('iframe', src='https://www.youtube.com/embed/%s?rel=0' % video_id,
                width='1280', height='720', frameborder='0', allowfullscreen='true')
            
            e.parent.replace_with(fm)
        
        # All
        el_to_uwrap = [ 
            'main', 
            '#mobile1stparagraph',  
            '.content', 
            '.content-text', 
            '.article-content', 
            '.content-intertitle', 
            '.td-post-content', 
            '.td-post-featured-image', 
            '[itemprop="articleBody"]', 
        ] if not context.get('el_to_uwrap') else context.get('el_to_uwrap')
        [e.unwrap() for e in html.select(','.join(el_to_uwrap))]
            
        el_to_decompose = {
            'geral': [
                'style', 
                'script', 
                '#liveblog-container', 
                '.content-head', 
                '.content-share-bar', 
                '[data-block-type="related-articles"]', 
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
        [t.decompose() for t in html.select(','.join(el_to_decompose['geral']))]
        [t.decompose() for t in html.select(','.join(el_to_decompose['empty'])) if t.is_empty_element]
        
        # TODO: B4S bug
        [e.previous_element.decompose() for e in html.select('p + br + p')]
        
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
        for t in html.find_all():
            for a in attrs_to_remove:
                if t.has_attr(a): del t[a] 
                else: pass
                
        
        for e in html.select('td p s'):
            e.parent.parent.string = e.string
        
        for comments in html.findAll(text=lambda text:isinstance(text, Comment)):
            comments.extract()
        
        value = html.prettify()
        # print(value)
        return value