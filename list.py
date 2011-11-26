import webapp2
import json

import adaptors
import config

class ListActionHandler(webapp2.RequestHandler):
    '''Handles the LIST action of the API'''
    
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        
        self.response.out.write(adaptors.list_json())