import json

class Adaptor(object):
    @classmethod
    def matches_uri(klass, provider_uri):
        return bool(klass.URI_REGEX.match(provider_uri))
    
    def make_uri(self, **kwargs):
        '''Utility method for creating a URI from a format string
        and keyword arguments.'''
        return self.REQUEST_STRING.format(**kwargs)
    
    def get_json(self, query, **kwargs):
        '''Utility method that returns JSON for a query.'''
        return json.dumps(self.get(query),
                          indent = 4 if kwargs.get('pretty', False) == True else None)