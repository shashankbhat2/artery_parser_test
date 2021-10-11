from flask import Flask, request
from email_parser_test import TestEmailParsers

app = Flask(__name__)


@app.route('/')
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/parser', methods=['GET', 'POST'])
def parseEmails():
    data = request.data
    response = "Email Parsed"
    parser = TestEmailParsers(data)
    name = parser.getEmailSenderName()
    if name['Name'] == "Cult Fit":
        parsedEmail = parser.parseCareFit()
        return (parsedEmail, 200, None)
    else:
        response = "Could'nt Parse Email"
        return (response, 400, None)


if __name__ == "__main__":
    app.run()

