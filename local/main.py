import datetime
from urllib.request import Request, urlopen
import urllib.parse
from random import randint
import time
import os
from concurrent.futures import ThreadPoolExecutor

scrapers = [
'https://asia-northeast1-miqbooking.cloudfunctions.net/scrape-asia-northeast1',
'https://asia-southeast1-miqbooking.cloudfunctions.net/scrape-asia-southeast1',
'https://australia-southeast1-miqbooking.cloudfunctions.net/scrape-australia-southeast1',
'https://europe-west2-miqbooking.cloudfunctions.net/scrape-europe-west2',
'https://europe-west3-miqbooking.cloudfunctions.net/scrape-europe-west3',
'https://europe-west6-miqbooking.cloudfunctions.net/scrape-europe-west6',
#'https://southamerica-east1-miqbooking.cloudfunctions.net/scrape-southamerica-east1', #SLOW
'https://us-central1-miqbooking.cloudfunctions.net/scrape-us-central1',
'https://us-east1-miqbooking.cloudfunctions.net/scrape-us-east1',
'https://us-west2-miqbooking.cloudfunctions.net/scrape-us-west2',
'https://asia-east1-miqbooking.cloudfunctions.net/scrape-asia-east1',
'https://asia-southeast2-miqbooking.cloudfunctions.net/scrape-asia-southeast2'
]

user_agents = [
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:70.0) Gecko/20100101 Firefox/70.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
'Mozilla/5.0 (iPhone; CPU iPhone OS 13_1_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.1 Mobile/15E148 Safari/604.1'
]

def make_request(scraper, agent):
    start_time = datetime.datetime.now()
    req = Request(scraper, headers={'User-Agent': agent})
    response = urlopen(req).read().decode("utf-8")
    end_time = datetime.datetime.now()
    print('Pinging from ' +scraper +' T:' + str((end_time-start_time).total_seconds()) +' seconds')
    print(response)
    if 'None' not in response:
        os.system('open -a Safari https://allocation.miq.govt.nz/portal/organisation/5f377e18-43bc-4d0e-a0d3-79be3a2324ec/event/MIQ-DEFAULT-EVENT/accommodation/arrival-date#step-2')
        quit()

def main():
    currs = ThreadPoolExecutor(max_workers=3)
    while True:
        agent = user_agents[randint(0, len(user_agents)-1)]
        scraper = scrapers[randint(0, len(scrapers)-1)]
        currs.submit(make_request, scraper, agent)

if __name__ == '__main__':
    main()