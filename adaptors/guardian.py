from google.appengine.api import urlfetch
import urllib
import json
import re
import logging
import adaptor

class GuardianAdaptor(adaptor.Adaptor):
    '''Adaptor for Guardian'''
    
    NAME = 'Guardian'
    URI = 'guardian.com'
    URI_REGEX = re.compile(r'^guardian\.com$')
    API_VERSION = 1
    API_KEY = 'cufazf7k84v6a2cazkujwcpc'
    MAX = 50
    FORMAT = 'json'
    REQUEST_STRING = r'http://content.guardianapis.com/search?order-by=newest&format={format}&q={query}&page-size={rpp}&api_key={api_key}'
    REQUEST_STRING += r'&page={page}'
    
    def _convert_dict(self, **kwargs):
        '''Converts a set of Guardian specific stuff to a dict.'''
        
        ATTRIB_MAP = {
            'title': 'webTitle',
            'desc': 'sectionName',
            'link': 'webUrl',
            'when': 'webPublicationDate'
        }
        
        return {attrib: kwargs.get(ATTRIB_MAP[attrib]) for attrib in ATTRIB_MAP}
    
    def get(self, query, **kwargs):
        '''Searches and returns appropriate results for given query as a dict.'''
        result = urlfetch.fetch(super(self.__class__, self).make_uri(
            format=GuardianAdaptor.FORMAT,
            query=urllib.quote_plus(query),
            rpp=kwargs.get('count', 10),
            page=kwargs.get('page', 1),
            api_key=GuardianAdaptor.API_KEY))
        
        if result.status_code == 200:
            #The request succeeded; parse and convert to a dict
            articles = [self._convert_dict(**article) for article in json.loads(result.content)['response']['results']]
            return {
                'displaytype': 'articles',
                'articles': articles,
            }
