# -*- coding: utf-8 -*-

import json
import requests
import logging; logger = logging.getLogger(__name__)
from bs4 import BeautifulSoup, Comment


class ImproveHTML(object):

    estadao_media_url = 'http://mdw-mm.estadao.com.br/middlewareAgile/rest/conteudo?tipo_midia={tipo}&idAgile={id}&produto=estadao'

    def __call__(self, value, loader_context):
        spider_name = loader_context.get('spider_name')
        html = BeautifulSoup(value, 'html.parser')

        if spider_name is 'cartacapital':
            try:
                selector = '.image-inline'
                for el in html.select(selector):
                    fg = html.new_tag('figure')
                    fg.append(html.new_tag('img', src=el.select('img')[0]['data-src']))
                    fc = html.new_tag('figcaption')
                    fc.string = el.select('.image-caption')[0].string
                    fg.append(fc)

                    el.replace_with(fg)
            except Exception as e:
                logger.error('Failed to replace "%s" selector from %s:\n%s',
                    selector, spider_name, e)

            try:
                selector = '.tile-rights'
                for i, el in enumerate(html.select(selector)):
                    fg = html.new_tag('figure')
                    img = html.select('.canvasImg img')[i]
                    fg.append(html.new_tag('img', src=img['data-src']))
                    fc = html.new_tag('figcaption')
                    fc.string = el.select('span')[0].string
                    fg.append(fc)

                    el.replace_with(fg)
                    img.parent.decompose()
            except Exception as e:
                logger.error('Failed to replace "%s" selector from %s:\n%s',
                    selector, spider_name, e)

        if spider_name is 'veja':
            try:
                selector = '.featured-image'
                for el in html.select(selector):
                    fg = html.new_tag('figure')
                    fg.append(html.new_tag('img', src=el.select('img')[0]['data-src']))
                    fc = html.new_tag('figcaption')
                    fc.string = el.select('p')[0].string
                    fg.append(fc)

                    el.replace_with(fg)
            except Exception as e:
                logger.error('Failed to replace "%s" selector from %s:\n%s',
                    selector, spider_name, e)

            try:
                selector = 'p span iframe[src*="https://www.youtubel.com/embed"]'
                for el in html.select(selector):
                    video_id = el['data-lazy-src'].split('/')[4]
                    fm = html.new_tag('iframe', src='https://www.youtubel.com/embed/%s?rel=0' % video_id,
                        width='1280', height='720', frameborder='0', allowfullscreen='true')
            except Exception as e:
                logger.error('Failed to replace "%s" selector from %s:\n%s',
                    selector, spider_name, e)

        if spider_name is 'g1':
            try:
                selector = '[data-block-type="backstage-photo"]'
                for el in html.select(selector):
                    fg = html.new_tag('figure')
                    img_src = el.select_one('img.content-media__image').get('data-src')
                    fg.append(html.new_tag('img', src=img_src))
                    fc = html.new_tag('figcaption')
                    fc.string = el.select_one('.content-media__description__caption').get_text()
                    fg.append(fc)

                    el.replace_with(fg)
            except Exception as e:
                logger.error('Failed to replace "%s" selector from %s:\n%s',
                    selector, spider_name, e)

            try:
                selector = '[data-block-type="backstage-video"]'
                for el in html.select(selector):
                    video_id = el.select('[data-video-id]')[0]['data-video-id']
                    fg = html.new_tag('figure')
                    fg.append(html.new_tag('img', src='https://s02.video.glbimg.com/x720/%s.jpg' % video_id))
                    fc = html.new_tag('figcaption')
                    fc.string = el.select('[itemprop="caption"]')[0].get_text()
                    fg.append(fc)
                    a = html.new_tag('a', href='https://globoplay.globo.com/v/%s/' % video_id)
                    a.append(fg)

                    el.replace_with(a)
            except Exception as e:
                logger.error('Failed to replace "%s" selector from %s:\n%s',
                    selector, spider_name, e)

        if spider_name is 'estadao':
            try:
                selector = '[data-config]'
                for el in html.select(selector):
                    media_doc = json.loads(el['data-config'])
                    media_url =  self.estadao_media_url if not loader_context.get('media_img_url') else loader_context.get('media_img_url')
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
            except Exception as e:
                logger.error('Failed to replace "%s" selector from %s:\n%s', selector, spider_name, e)

            # for el in html.select('.documento'):
            #     [e.decompose() for eLin el.select('span')]
            #     el.select('h3')[0].name = 'strong'

        if spider_name is 'folhadesp':
            try:
                selector = '.gallery'
                for el in html.select(selector):
                    href = el.select_one('a')['href'].rsplit('#')[0]
                    result = requests.get(''.join((href, '.json'))).json()

                    section = html.new_tag('section')
                    h1 = html.new_tag('h1')
                    h1.string = result['gallery']['title']
                    section.append(h1)
                    h2 = html.new_tag('h2')
                    h2.string = result['gallery']['description']
                    section.append(h2)

                    for image in result['images']:
                        fg = html.new_tag('figure')

                        img = html.new_tag('img', src=image['image_gallery'])
                        fg.append(img)
                        fc = html.new_tag('figcaption')
                        fc.string = image['legend']
                        small = html.new_tag('small')
                        small.string = image['author']
                        fc.insert(1, small)
                        fg.append(fc)

                        section.append(fg)

                    el.replace_with(section)
            except Exception as e:
                logger.error('Failed to replace "%s" selector from %s:\n%s',
                    selector, spider_name, e)

        if spider_name is 'atarde':
            # try:
            #     selector = 'p'
            #     for el in html.select(selector):
            #         text=el.get_text()
            #         el.replace_with(text)
            # except Exception as e:
            #     logger.error('Failed to replace "%s" selector from %s:\n%s',
            #         selector, spider_name, e)
            # try:
            #     selector = 'figure'
            #     for el in html.select(selector):
            #         text=el.get_text()
            #         el.replace_with('')
            #     selector = 'aside'
            #     for el in html.select(selector):
            #         text=el.get_text()
            #         el.replace_with('')
            try:
                selector = 'a'
                for el in html.select(selector):
                    text=el.get_text()
                    el.replace_with(text)
                selector = 'aside'
                for el in html.select(selector):
                    el.decompose()

            except Exception as e:
                logger.error('Failed to replace "%s" selector from %s:\n%s',
                    selector, spider_name, e)

        if spider_name is 'correiobraziliense':
            try:

                selector = 'section'
                for el in html.select(selector):
                    fg = html.new_tag('figure')
                    print('oiiii')
                    images = el.select('img')
                    if not(len(images) ==0):
                        for img in images:
                            fg.append(html.new_tag('img', src=img['src']))
                        el.replace_with(fg)


                # selector = '.news__image'
                # for el in html.select(selector):
                #     # el.unwrap()
                #     el.decompose()

                selector = 'div'
                for el in html.select(selector):
                    el.name = 'p'

                selector = 'br'
                for el in html.select(selector):
                    el.decompose()

                selector = 'h3'
                for el in html.select(selector):
                    el.name = 'h2'
                selector = 'p'
                for el in html.select(selector):
                    if el.get_text() == '':
                        el.decompose()
            except Exception as e:
                logger.error('Failed to replace "%s" selector from %s:\n%s',
                    selector, spider_name, e)

        if spider_name is 'correiopopular':
            try:
                selector = '#foto_auto'
                for el in html.select(selector):
                    fg = html.new_tag('figure')
                    images = el.select('img')
                    if not(len(images) ==0):
                        for img in images:
                            fg.append(html.new_tag('img', src=img['src']))
                        el.replace_with(fg)
                    # print(src)
                    # el.replace_with(src)

                selector = '.fe-content'
                for el in html.select(selector):
                    text=el.get_text()
                    el.replace_with(text)
            except Exception as e:
                logger.error('Failed to replace "%s" selector from %s:\n%s',
                    selector, spider_name, e)

                ######----FALTA TERMINAR----######
        if spider_name is 'diariodepernambuco':
            try:
                selector = 'table'
                for el in html.select(selector):
                    fg = html.new_tag('figure')
                    images = el.select('img')
                    if not(len(images) ==0):
                        for img in images:
                            fg.append(html.new_tag('img', src=img['src']))
                        el.replace_with(fg)
                    # print(src)
                    # el.replace_with(src)

                selector = 'a'
                for el in html.select(selector):
                    el.decompose()
                selector = 'div'
                for el in html.select(selector):
                    el.unwrap()

            except Exception as e:
                logger.error('Failed to replace "%s" selector from %s:\n%s',
                    selector, spider_name, e)

        if spider_name is 'estadodeminas':
            try:
                #Caso imagens em galeria
                selector = 'section'
                for el in html.select(selector):
                    images = el.select('img')
                    img_src=''
                    for img in images:
                        img_src=img_src+img['src']+'\n'
                    el.replace_with(img_src)
                #Se não, caso uma imagem de capa
                # selector = 'figure'
                # for el in html.select(selector):
                #     img_src = el.select('img')[0]['src']
                #     el.replace_with(img_src)

                selector = 'a'
                for el in html.select(selector):
                    el.decompose()
                selector = 'meta'
                for el in html.select(selector):
                    el.decompose()
            except Exception as e:
                logger.error('Failed to replace "%s" selector from %s:\n%s',
                    selector, spider_name, e)

        if spider_name is 'jornaldecampinas':
            try:
                selector = 'i'
                for el in html.select(selector):
                    if (len(el.contents))==0:
                        el.decompose()
                selector = 'a'
                for el in html.select(selector):
                    el.decompose()
                selector = 'ul'
                for el in html.select(selector):
                    el.decompose()
                selector = 'u'
                for el in html.select(selector):
                    el.unwrap()
                selector = 'img'
                for el in html.select(selector):
                    fg = html.new_tag('figure')
                    fg.append(html.new_tag('img', src=img['src']))
                    img_src = el['src']
                    el.replace_with(fg)
                selector = 'h2'
                for el in html.select(selector):
                    el.decompose()
                selector = 'h3'
                for el in html.select(selector):
                    el.decompose()
                selector = 'span'
                for el in html.select(selector):
                    text = el.get_text()
                    if text=='':
                        el.decompose()
                    else:
                        el.replace_with(text)
                selector = 'p'
                for el in html.select(selector):
                    text = el.get_text()
                    if text=='':
                        el.decompose()
                    # else:
                    #     el.replace_with(text)
                selector = 'table'
                for el in html.select(selector):
                    ems=el.select('em')
                    text=''
                    for em in ems:
                        text=text+em.get_text()
                    el.replace_with(text)
            except Exception as e:
                logger.error('Failed to replace "%s" selector from %s:\n%s',
                    selector, spider_name, e)
        if spider_name is 'novaescola':
            try:
                selector = 'div'
                for el in html.select(selector):
                    el.unwrap()
                # selector = 'img'
                # for el in html.select(selector):
                #     el.attrs.remove('caption')
                selector = 'a'
                for el in html.select(selector):
                    print('novaescola a')
                    # print(el.text())
                    el.replace_with(el.get_text())

            except Exception as e:
                logger.error('Failed to replace "%s" selector from %s:\n%s',
                    selector, spider_name, e)
        if spider_name is 'valor':
            try:
                selector = 'a'
                for el in html.select(selector):
                    print('novaescola a')
                    # print(el.text())
                    el.replace_with(el.get_text())
            except Exception as e:
                logger.error('Failed to replace "%s" selector from %s:\n%s',
                    selector, spider_name, e)

        # all spiders
        try:
            selector = 'div.wp-caption'
            for el in html.select(selector):
                fg = html.new_tag('figure')
                fg.append(html.new_tag('img', src=el.select('img')[0]['src']))
                fc = html.new_tag('figcaption')
                fc.string = el.select('.wp-caption-text')[0].string
                fg.append(fc)

                el.replace_with(fg)
        except Exception as e:
            logger.error('Failed to replace "%s" selector from %s:\n%s',
                selector, spider_name, e)

        try:
            selector = 'p iframe[data-lazy-src*="https://www.youtubel.com/embed"]'
            for el in html.select(selector):
                # TODO: Use Regex?
                video_id = el['data-lazy-src'].split('/')[4]
                fm = html.new_tag('iframe', src='https://www.youtubel.com/embed/%s?rel=0' % video_id,
                    width='1280', height='720', frameborder='0', allowfullscreen='true')

                el.parent.replace_with(fm)
        except Exception as e:
            logger.error('Failed to replace "%s" selector from %s:\n%s',
                selector, spider_name, e)

        el_to_uwrap = loader_context.get('el_to_uwrap')
        if not el_to_uwrap:
            el_to_uwrap = [
                '.article-content',
                '#cke_pastebin',
                'center',
                '.content',
                '#content-core',
                '.content-text',
                '.content-intertitle',
                '[data-block-type=unstyled]',
                '[itemprop="articleBody"]',
                'main',
                '#mobile1stparagraph',
                'p span',
                'p em span',
                'span',
                '.td-post-content',
                '.td-post-featured-image',
                '#textstructured',
                '.video-container',
            ]

        [el.unwrap() for el in html.select(', '.join(el_to_uwrap))]

        el_to_decompose = loader_context.get('el_to_decompose')
        if not el_to_decompose:
            el_to_decompose = {
                'geral': [
                    '.advertising',
                    '#column-middle',
                    '.content-ads',
                    '.content-head',
                    '.content-know-more',
                    '.content-share-bar',
                    '.comments',
                    '#comments',
                    '#comentarios',
                    '.clear',
                    '[data-block-type="related-articles"]',
                    '#liveblog-container',
                    '.mc-side-item__container',
                    '.mc-show-later',
                    '.publicidade-content',
                    '#taboola-below-article-thumbnails',
                    '.tags',
                    '.tags-container',
                    '.read-more',
                    '.specialContainer',
                    '.widget-news',
                    'applet',
                    'base',
                    'basefont',
                    'bgsound',
                    'blink',
                    'body',
                    'button',
                    'dir',
                    'embed',
                    'fieldset',
                    'form',
                    # 'frame',
                    'frameset',
                    'head',
                    'html',
                    'iframe',
                    'ilayer',
                    'input',
                    'isindex',
                    'label',
                    'layer',
                    'legend',
                    'link',
                    'marquee',
                    'menu',
                    # 'meta',
                    'figure meta',
                    'noframes',
                    'noscript',
                    'object',
                    'optgroup',
                    'option',
                    'param',
                    'plaintext',
                    '#respond',
                    'script',
                    'select',
                    'style',
                    'textarea',
                    'xml',
                ]
            }

        [el.decompose() for el in html.select(', '.join(el_to_decompose['geral']))]
        [el.decompose() for el in html.select('div') \
            if len(el.get_text()) == 0 or el.get_text() == '&nbsp;']
        [el.decompose() for el in html.select('p') \
            if len(el.get_text()) == 0 or el.get_text() == '&nbsp;']

        [el.decompose() for el in html.select('span') \
            if len(el.contents) == 0]

        # TODO: B4S bug
        [el.previous_element.decompose() for el in html.select('p + br + p')]

        attrs_to_remove = loader_context.get('attrs_to_remove')
        if not attrs_to_remove:
            attrs_to_remove = [
                'alt',
                'caption',
                'cellpadding',
                'cellspacing',
                'class',
                'data-block-type',
                'data-sizes',
                'data-track-category',
                'data-track-links',
                'data-width',
                'itemtype',
                'itemscope',
                'itemprop',
                'height',
                'rel',
                'sizes',
                # TODO: What do with srcset? Get the largest image?
                # 'srcset',
                'style',
                'title',
                'type',
                'valign',
                'width',

            ]

        for t in html.find_all(True):
            for a in attrs_to_remove:
                if t.has_attr(a): del t[a]
                else: pass

        for el in html.select('td p s'):
            el.parent.parent.string = el.string

        # TODO: What do with more than one strong in p?
        # for el in html.select('p > strong'):
        #     h2 = html.new_tag('h2')
        #     h2.string = el.string
        #     el.parent.replace_with(h2)

        [c.extract() for c in html.findAll(text=lambda text:isinstance(text, Comment))]

        html_new = html.prettify()

        return html_new