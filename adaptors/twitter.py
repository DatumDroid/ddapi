from google.appengine.api import urlfetch
import urllib
import json
import re
import logging
import adaptor

class TwitterAdaptor(adaptor.Adaptor):
    '''Adaptor for Twitter'''
    
    NAME = 'Twitter'
    URI = 'Twitter.com'
    URI_REGEX = re.compile(r'^twitter\.com$')
    API_VERSION = 1
    FORMAT = 'json'
    MAX = 50
    REQUEST_STRING = r'http://search.twitter.com/search.{format}?q={query}&rpp={rpp}&page={page}'
    
    def _convert_dict(self, **kwargs):
        '''Converts a set of Twitter specific stuff to a dict.'''
        
        ATTRIB_MAP = {
            'title': 'text',
            'desc': 'from_user',
            'link': 'source',
            'when': 'created_at',
            'image': 'profile_image_url'
        }
        
        return {attrib: kwargs.get(ATTRIB_MAP[attrib]) for attrib in ATTRIB_MAP}
    
    def get(self, query, **kwargs):
        '''Searches and returns appropriate results for given query as a dict.'''
        result = urlfetch.fetch(super(self.__class__, self).make_uri(
            rpp=kwargs.get('count', 10),
            page=kwargs.get('page', 1),
            format=TwitterAdaptor.FORMAT,
            query=urllib.quote_plus(query)))
        
        if result.status_code == 200:
            #The request succeeded; parse and convert to a dict
            articles = [self._convert_dict(**article) for article in json.loads(result.content)['results']]
            return {
                'displaytype': 'articles',
                'articles': articles,
            }
