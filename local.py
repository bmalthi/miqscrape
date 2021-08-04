from urllib.request import Request, urlopen
import os
import datetime

url = 'https://miqscrape.wl.r.appspot.com/scrape'
while True:
    agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:70.0) Gecko/20100101 Firefox/70.0 CRON'
    req = Request(url, headers={'User-Agent': agent})
    html_bytes = urlopen(req).read()
    response = html_bytes.decode("utf-8")
    print(datetime.datetime.now())
    print(response)
    if response[:10] == 'Open Dates': #need to check the date is good match
        os.system('open -a Safari https://allocation.miq.govt.nz/portal/organisation/5f377e18-43bc-4d0e-a0d3-79be3a2324ec/event/MIQ-DEFAULT-EVENT/accommodation/arrival-date#step-2')
        break