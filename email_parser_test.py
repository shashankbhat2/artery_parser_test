import json
from postmark_inbound import PostmarkInbound
import re

class TestEmailParsers:
    def __init__(self,json_object):
        self.json_object = json_object
        self.inbound = PostmarkInbound(json=self.json_object)

    def getEmailSenderName(self):
        return self.inbound.sender()
    
    def getEmailTextBody(self):
        return self.inbound.text_body()
            
    def parseCareFit(self):
        text = self.getEmailTextBody()
        consultation = {}
        consultation_string = str(re.findall(r'consultation at .* \d{1,2}:\d{2}.*[AM|PM]', text)[0])
        site = self.inbound.sender()['Name']
        date = str(re.findall(r'\d{2}-[A-Z]\w*', consultation_string)[0])
        time = str(re.findall(r'\d{1,2}:\d{2}.*[AM|PM]', consultation_string)[0]) 
        link = str(re.findall(r'https://orion.curefit.co.*[a-zA-Z0-9_.+-]', text)[0])
        consultation['date'] = date
        consultation['time'] = time
        consultation['link'] = link
        consultation['site'] = site
        return consultation