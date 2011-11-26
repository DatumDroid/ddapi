import config
import json

def get_json(provider, query, **kwargs):
    '''Delegates the GET action.'''
    
    for adaptor in config.ENABLED_ADAPTORS:
        if adaptor.matches_uri(provider):
            return adaptor().get_json(query, **kwargs)

def list_json():
    '''Returns a JSON list of all enabled adaptors'''
    
    return json.dumps({adaptor.NAME: adaptor.URI for adaptor in config.ENABLED_ADAPTORS})