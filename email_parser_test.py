import json
from postmark_inbound import PostmarkInbound
import re
from datetime import datetime 

class TestEmailParsers:
    def __init__(self,json_object):
        self.json_object = json_object
        self.inbound = PostmarkInbound(json=self.json_object)
        self.consultation = {}
        self.consultation_time = []
        
    def getEmailSenderName(self):
        return self.inbound.sender()
    
    def getEmailTextBody(self):
        return self.inbound.text_body()

    def getEmailReciever(self):
        return self.inbound.to()[0]['Email']

    def parseCareFit(self):
        text = self.getEmailTextBody()
        consultation_string = str(re.findall(r'consultation .* \d{1,2}:\d{2}.*[AM|PM]', text)[0])
        site = self.inbound.sender()['Name']
        date_string = str(re.findall(r'\d{2}-[A-Z]\w*', consultation_string)[0])
        date = re.sub(r'\-', ' ', date_string) + ' ' + str(datetime.today().year)
        time = str(re.findall(r'\d{1,2}:\d{2}', consultation_string)[0]) 
        link = str(re.findall(r'https://orion.curefit.co.*[a-zA-Z0-9_.+-]', text)[0])
        self.consultation_time.append(str(datetime.strptime(time, '%H:%M').time()))
        self.consultation['date'] = datetime.strptime(date, '%d %b %Y')
        self.consultation['time'] = self.consultation_time
        self.consultation['link'] = link
        self.consultation['site'] = site
        self.consultation['doctorEmail'] = self.getEmailReciever()
        return self.consultation
