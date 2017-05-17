# -*- coding: utf-8 -*-
import urllib.parse
import logging; logger = logging.getLogger(__name__)
import GoogleScraper

class SearchEngine(object):
    
    @staticmethod
    def search_for_urls(args={}):
        """
        args['config']['last_update']
            Applications: tbm=app
            Blogs: tbm=blg
            Books: tbm=bks
            Discussions: tbm=dsc
            Images: tbm=isch
            News: tbm=nws
            Patents: tbm=pts
            Places: tbm=plcs
            Recipes: tbm=rcp
            Shopping: tbm=shop
            Video: tbm=vid
        """ 
    
        def fix_urls(url):
            url = url.replace('/amp/', '') if '/amp/' in url else url
            url = url.replace('/amp.html', '') if '/amp.html' in url else url
            url = urllib.parse.urljoin('http://', url) if 'http://' not in url else url
            return url
        
        # TODO: implement quantity arg
        if args.get('engine', 'google') == 'google':
            config = {
                'use_own_ip': 'True',
                'keywords': [args['query']],
                'google_search_url': 'https://www.google.com/search?tbs=qdr:%s&' % args.get('last_update', 'w'),
                'num_results_per_page': args.get('results_per_page', 50),
                'num_pages_for_keyword': args.get('pages', 2),
                'num_workers': 1,
                'search_engines': ['google',],
                'search_type': 'normal',
                'scrape_method': 'http',
                'do_caching': False,
                'print_results': None,
            }
        else:
            raise NotImplementedError('Only Google serch engine is supported at momment')
        
        logger.debug('Google Search scrapping start with this configuration: {}'
                    .format(config))
        
        try:
            google_search = GoogleScraper.scrape_with_config(config)
            
            urls_without_fix = []
            urls = []
            for serp in google_search.serps:
                urls_without_fix= [r.link for r in serp.links]
                urls = [fix_urls(r.link) for r in serp.links]
            
            logger.debug('Google Search fixed links successfully extracted with query "{}": {:d} links extracted'.format(
                args['query'], len(urls)))
            logger.debug('Google Search links without fix successfully extracted with query "{}":\n{}'.format(
                args['query'], urls_without_fix))
            logger.debug('List of link extracted from Google Search with the query "{}":\n{}'.format(
                args['query'], urls))
            
            return urls
        except GoogleScraper.GoogleSearchError as e:
            logger.error(str(e))