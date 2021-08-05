from flask import Flask
import os
import datetime
from urllib.request import Request, urlopen

app = Flask(__name__)

@app.route('/trigger', methods=['GET'])
def trigger_scrape():
    print("Starting scrape at:" +str(datetime.datetime.now()))
    url = 'https://miqscrape-2nqqxkgl5q-ts.a.run.app/scrape'
    agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:70.0) Gecko/20100101 Firefox/70.0'
    req = Request(url, headers={'User-Agent': agent})
    html_bytes = urlopen(req).read()
    return "Scrapy Scrapy"

@app.route('/', methods=['GET'])
def receive_message():
    print("Received Message at:" +str(datetime.datetime.now()))
    return "Hello, world!"
    #os.system('open -a Safari https://allocation.miq.govt.nz/portal/organisation/5f377e18-43bc-4d0e-a0d3-79be3a2324ec/event/MIQ-DEFAULT-EVENT/accommodation/arrival-date#step-2')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
