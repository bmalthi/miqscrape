from flask import Flask
from urllib.request import Request, urlopen
import re
import os
from twilio.rest import Client

#Really Naughty
TWILIO_ACCOUNT_SID = 'AC4ff56a6d29868282b983c5b1b5816af5'
TWILIO_AUTH_TOKEN = '3fe5cba01d25c4a6889245a2087d54f1'

# pylint: disable=C0103
app = Flask(__name__)

@app.route('/scrape')
def scrape():
    url = 'https://allocation.miq.govt.nz/portal/'
    #TODO Rotate id
    agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:70.0) Gecko/20100101 Firefox/70.0'
    req = Request(url, headers={'User-Agent': agent})
    html_bytes = urlopen(req).read()
    html = html_bytes.decode("utf-8")
    #regex = r"<div class=\"no\" . aria-label=\"(\w+ \d+)\".+<\/div>"
    regex = r"<div (?!class=\"no\") . aria-label=\"(\w+ \d+)\".+<\/div>"
    test_str = html
    matches = re.finditer(regex, test_str, re.MULTILINE)
    dates = [match.group(1) for match in matches]
    if len(dates) > 0:
        s = 'Open Dates:<br>'
        for d in dates:
            s = s + d + '<br>'
        message('MIQDATE:\n'+str(dates))
        return s
    else:
        return 'No Open Dates'

@app.route('/message')
def message(txt='helloworld'):
    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)
    message = client.messages.create(
                                body=txt,
                                messaging_service_sid='MG79fefe795961065491623dd800fa88e0', 
                                to='+14157543502'
                            )
    return message.sid

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')