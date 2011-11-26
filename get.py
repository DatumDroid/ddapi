import webapp2
import json

import adaptors
import config

class GetActionHandler(webapp2.RequestHandler):
    '''Handles the GET action of the API'''
    
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        
        if (not self.request.GET.has_key('provider')) or (not self.request.GET.has_key('q')):
            self.response.status_int = 400
            return
        provider = self.request.GET['provider']
        query = self.request.GET['q']
        p_token = self.request.GET.get('p_token', '')
        format = self.request.GET.get('format', 'json')
        pretty = bool(self.request.GET.get('pretty', False))
        
        if format == 'json':
            self.response.out.write(adaptors.get_json(provider, query,
                                                      p_token=p_token,
                                                      pretty=pretty))
        else:
            self.response.status = '405 Format not supported'
            return