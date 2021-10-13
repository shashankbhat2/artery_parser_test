import json
from postmark_inbound import PostmarkInbound
import re
from datetime import datetime
from switchcase import switch


class TestEmailParsers:
    def __init__(self, json_object):
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

    def runParser(self, name):
        for case in switch(name):
            if case("Cult Fit"):
                return self.parseCultFit()
                break
            if case("Aktiv Health"):
                return self.parseAktivHealth()
                break
        else:
            return "Not a valid email to Parse"

    def parseCultFit(self):
        text = self.getEmailTextBody()
        consultation_string = str(re.findall(
            r'consultation .* \d{1,2}:\d{2}.*[AM|PM]', text)[0])
        site = self.inbound.sender()['Name']
        date_string = str(re.findall(
            r'\d{2}-[A-Z]\w*', consultation_string)[0])
        date = re.sub(r'\-', ' ', date_string) + \
            ' ' + str(datetime.today().year)
        time = str(re.findall(r'\d{1,2}:\d{2}', consultation_string)[0])
        link = str(re.findall(
            r'https://orion.curefit.co.*[a-zA-Z0-9_.+-]', text)[0])
        self.consultation_time.append(
            str(datetime.strptime(time, '%H:%M').time()))
        self.consultation['date'] = str(
            datetime.strptime(date, '%d %b %Y').date())
        self.consultation['time'] = self.consultation_time
        self.consultation['link'] = link
        self.consultation['site'] = site
        self.consultation['doctorEmail'] = self.getEmailReciever()
        return self.consultation

    def parseAktivHealth(self):
        text = self.getEmailTextBody()
        site = self.inbound.sender()['Name']
        date = re.findall(r'Date : .*[0-9]', text)
        day = re.findall(r'Day : .*[a-zA-Z]', text)
        time = re.findall(
            r'Appointment Time \(From & To\) : .*[0-9AM|PM]', text)
        link = re.findall(
            r'https://teams.microsoft.com.*[a-zA-Z0-9_.+-]', text)
        consult_time = re.sub(
            r'Appointment Time \(From & To\) :', '', time[0]).strip()
        consultation_date = re.sub(r'Date : ', '', date[0])
        consultation_day = re.sub(r'Day : ', '', day[0])
        consultation_link = link[0]
        from_time = re.sub(r' - .*[0-9AM|PM]', '', consult_time)
        to_time_string = re.sub(r'[0-9].* - ', '', consult_time)
        to_time = re.sub(r'[AM|PM]', '', to_time_string).strip()
        self.consultation_time.append(
            str(datetime.strptime(from_time, '%H.%M').time()))
        self.consultation_time.append(
            str(datetime.strptime(to_time, '%H.%M').time()))
        self.consultation['site'] = site
        self.consultation['day'] = str(consultation_day)
        self.consultation['date'] = datetime.strptime(
            consultation_date, '%d-%m-%Y')
        self.consultation['link'] = str(consultation_link)
        self.consultation['time'] = self.consultation_time
        self.consultation['doctorEmail'] = self.getEmailReciever()
        return self.consultation
