from flask import Flask, request
from email_parser_test import TestEmailParsers
import requests
app = Flask(__name__)


@app.route('/')
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/parser', methods=['GET', 'POST'])
def parseEmails():
    data = request.data
    response = "Email Parsed"
    parser = TestEmailParsers(data)
    name = parser.getEmailSenderName()['Name']
    consultation = parser.runParser(name)
    requests.post('http://localhost:3000/api/scheduler', data=consultation)
    return ("Success", 200, None)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=True)
