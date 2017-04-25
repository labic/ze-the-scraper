# -*- coding: utf-8 -*-

import json
import requests
import logging
from bs4 import BeautifulSoup, Comment

logger = logging.getLogger(__name__)

class CleanHTML(object):
    
    estadao_media_url = 'http://mdw-mm.estadao.com.br/middlewareAgile/rest/conteudo?tipo_midia={tipo}&idAgile={id}&produto=estadao'
    
    def __call__(self, value, context={}):
        self.stats = context.get('crawler_stats')
        html = BeautifulSoup(value, 'html.parser')
        html_old = html.prettify()
        
        # cartacapital
        for el in html.select('.image-inline'):
            fg = html.new_tag('figure')
            fg.append(html.new_tag('img', src=el.select('img')[0]['data-src']))
            fc = html.new_tag('figcaption')
            fc.string = el.select('.image-caption')[0].string
            fg.append(fc)
            
            el.replace_with(fg)
        
        for i, el in enumerate(html.select('.tile-rights')):
            fg = html.new_tag('figure')
            img = html.select('.canvasImg img')[i]
            fg.append(html.new_tag('img', src=img['data-src']))
            fc = html.new_tag('figcaption')
            fc.string = el.select('span')[0].string
            fg.append(fc)
            
            el.replace_with(fg)
            img.parent.decompose()
        
        # veja
        for el in html.select('.featured-image'):
            fg = html.new_tag('figure')
            fg.append(html.new_tag('img', src=el.select('img')[0]['data-src']))
            fc = html.new_tag('figcaption')
            fc.string = el.select('p')[0].string
            fg.append(fc)
            
            el.replace_with(fg)
            
        for el in html.select('p span iframe[src*="https://www.youtubel.com/embed"]'):    
            video_id = el['data-lazy-src'].split('/')[4]
            fm = html.new_tag('iframe', src='https://www.youtubel.com/embed/%s?rel=0' % video_id,
                width='1280', height='720', frameborder='0', allowfullscreen='true')
        
        # g1
        for el in html.select('[data-block-type="backstage-photo"]'):
            fg = html.new_tag('figure')
            fg.append(html.new_tag('img', src=el.select('img.content-media__image')[0]['data-src']))
            fc = html.new_tag('figcaption')
            fc.string = el.select('img.content-media__image')[0]['alt']
            fg.append(fc)
            
            el.replace_with(fg)
        
        for el in html.select('[data-block-type="backstage-video"]'):
            video_id = el.select('[data-video-id]')[0]['data-video-id']
            fg = html.new_tag('figure')
            fg.append(html.new_tag('img', src='https://s02.video.glbimg.com/x720/%s.jpg' % video_id))
            fc = html.new_tag('figcaption')
            fc.string = el.select('[itemprop="caption"]')[0]['content']
            fg.append(fc)
            a = html.new_tag('a', href='https://globoplay.globo.com/v/%s/' % video_id)
            a.append(fg)
            
            el.replace_with(a)
        
        # estadao
        for el in html.select('[data-config]'):
            media_doc = json.loads(el['data-config'])
            media_url =  self.estadao_media_url if not context.get('media_img_url') else context.get('media_img_url')
            media_url = media_url.format(**media_doc)
            results = requests.get(media_url).json()['resultadoConteudo']['conteudos']
            
            img_src = ''
            for presset in results[0]['pressets']:
                if presset['class'] == 'full':
                    img_src = presset['file']
                    break
            
            fg = html.new_tag('figure')
            fg.append(html.new_tag('img', src=img_src))
            fc = html.new_tag('figcaption')
            fc.string = '{} '.format(results[0]['titulo'])
            s = html.new_tag('small', rel='credits') 
            s.string = results[0]['credito']
            fc.append(s)
            fg.append(fc)
            
            el.replace_with(fg)
        
        # for el in html.select('.documento'):
        #     [e.decompose() for eLin el.select('span')]
        #     el.select('h3')[0].name = 'strong'
        
        # All
        for el in html.select('.wp-caption'):
            fg = html.new_tag('figure')
            fg.append(html.new_tag('img', src=el.select('img')[0]['src']))
            fc = html.new_tag('figcaption')
            fc.string = el.select('.wp-caption-text')[0].string
            fg.append(fc)
            
            el.replace_with(fg)
        
        for el in html.select('p iframe[data-lazy-src*="https://www.youtubel.com/embed"]'):
            # TODO: Use Regex?
            video_id = el['data-lazy-src'].split('/')[4]
            fm = html.new_tag('iframe', src='https://www.youtubel.com/embed/%s?rel=0' % video_id,
                width='1280', height='720', frameborder='0', allowfullscreen='true')
            
            el.parent.replace_with(fm)
        
        el_to_uwrap = [ 
            'main', 
            'p span', 
            'p em span', 
            '#content-core', 
            '#mobile1stparagraph', 
            '#textstructured', 
            '.content', 
            '.content-text', 
            '.article-content', 
            '.content-intertitle', 
            '.td-post-content', 
            '.td-post-featured-image', 
            '.video-container', 
            '[data-block-type=unstyled]', 
            '[itemprop="articleBody"]', 
        ] if not context.get('el_to_uwrap') else context.get('el_to_uwrap')
        [el.unwrap() for el in html.select(','.join(el_to_uwrap))]
            
        el_to_decompose = {
            'geral': [
                'style', 
                'script', 
                '#column-middle', 
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
        [el.decompose() for el in html.select(','.join(el_to_decompose['geral']))]
        [el.decompose() for el in html.select(','.join(el_to_decompose['empty'])) if not el.contents]
        
        # TODO: B4S bug
        [el.previous_element.decompose() for el in html.select('p + br + p')]
        
        attrs_to_remove = [
            'alt', 
            'title', 
            'class', 
            'data-block-type', 
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
        
        for el in html.select('td p s'):
            el.parent.parent.string = el.string
        
        for el in html.select('p > strong'):
            h2 = html.new_tag('h2')
            h2.string = el.string
            el.parent.replace_with(h2)
        
        [c.extract() for c in html.findAll(text=lambda text:isinstance(text, Comment))]
        
        html_new = html.prettify()
        
        return html_new