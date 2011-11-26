from google.appengine.api import urlfetch
import urllib
import json
import re
import logging
import adaptor

class FeedzillaAdaptor(adaptor.Adaptor):
    '''Adaptor for Feedzilla'''
    
    NAME = 'Feedzilla'
    URI = 'feedzilla.com'
    URI_REGEX = re.compile(r'^api\.feedzilla\.com$')
    API_VERSION = 1
    FORMAT = 'json'
    REQUEST_STRING = r'http://api.feedzilla.com/v{version}/articles/search.{format}?q={query}'
    
    def _convert_dict(self, **kwargs):
        '''Converts a set of Feedzilla specific stuff to a dict.'''
        
        ATTRIB_MAP = {
            'title': 'title',
            'desc': 'summary',
            'link': 'url',
            'when': 'publish_date'
        }
        
        return {attrib: kwargs.get(ATTRIB_MAP[attrib]) for attrib in ATTRIB_MAP}
    
    def get(self, query):
        '''Searches and returns appropriate results for given query as a dict.'''
        result = urlfetch.fetch(super(self.__class__, self).make_uri(
            version=FeedzillaAdaptor.API_VERSION,
            format=FeedzillaAdaptor.FORMAT,
            query=urllib.quote_plus(query)))
        
        if result.status_code == 200:
            #The request succeeded; parse and convert to a dict
            articles = [self._convert_dict(**article) for article in json.loads(result.content)['articles']]
            return {
                'displaytype': 'articles',
                'articles': articles,
            }
